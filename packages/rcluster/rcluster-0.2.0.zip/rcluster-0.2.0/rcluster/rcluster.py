import os
import json
from time import sleep
from inspect import signature
from pprint import PrettyPrinter

from boto3 import session

import rcluster as rcl

from logging import getLogger
log = getLogger(__name__)


class RCluster:
    """RCluster class object

    Designed to organize the information for a boto3 connection to EC2, paramiko
    connections using a consistent SSH key, creation of EC2 instances using a
    consistent key, the creation and tracking of manager and worker nodes
    comprising an R PSOCK cluster, and networking those manager and worker
    nodes to access within an RStudio Server session.
    """

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name,
                 instance_conf, manager_runtime=None, worker_runtime=None,
                 key_path=None, ip_ref='public_ip_address', ver=rcl.__ver__,
                 purge=False):
        """Initialize the RCluster object.
        Keyword arguments:
        aws_access_key_id -- AWS access key provided to boto3.session.Session()
        aws_secret_access_key -- AWS secret access key provided to
            boto3.session.Session()
        region_name -- The accessibility region provided to
            boto3.session.Session()
        instance_conf -- Dictionary defining {'ami': '', 'type': ''} for
            instances (where 'ami' is the AMI ID for the instances and type is
            the instance type used); can also contain other parameters to
            boto3's EC2.ServiceResource.create_instances
        manager_runtime -- String containing shell runtime command for the
            manager instance
        worker_runtime -- String containing shell runtime command for the
            worker instance
        key_path -- The path to the key used to create EC2 instances and to
            connect to them using paramiko clients
        ip_ref -- Whether to provide the user with the public IP or private IP
        ver -- Designed to stamp Security Groups, Placement Groups, and keys
        """
        self._kwargs = list(signature(RCluster).parameters.keys())
        self._kwargs.remove('purge')
        self._config = {}
        self.ses = session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.ec2 = self.ses.resource('ec2')
        if purge:
            _ec2Purge(self.ec2, ver)

        if not key_path:
            self.key_name = ver
            key_path = rcl.setData('pem')
            kp = self.ec2.create_key_pair(KeyName=ver)
            with open(key_path, 'w') as out:
                out.write(kp.key_material)
        else:
            self.key_name = os.path.splitext(os.path.basename(key_path))[0]

        if 'SecurityGroups' not in instance_conf:
            sg = self.ec2.create_security_group(
                GroupName=ver,
                Description='22 and 8787 open, permissive internal traffic.'
            )
            instance_conf['SecurityGroups'] = [ver]
            sleep(1)  # Security group may not "exist" in time for next call
            sg.authorize_ingress(IpProtocol='tcp', FromPort=22, ToPort=22,
                                 CidrIp='0.0.0.0/0')
            sg.authorize_ingress(IpProtocol='tcp', FromPort=8787, ToPort=8787,
                                 CidrIp='0.0.0.0/0')
            sg.authorize_ingress(SourceSecurityGroupName=ver)

        if 'Placement' not in instance_conf:
            pg = self.ec2.create_placement_group(GroupName=ver,
                                                 Strategy='cluster')
            instance_conf['Placement'] = {'GroupName': ver}

        for key in self._kwargs:
            self.__setattr__(key, locals()[key])

    def __repr__(self):
        """Indicates RCluster and pretty prints the _config dictionary"""
        return 'RCluster class object\n' + PrettyPrinter().pformat(
            self._config)

    def __setattr__(self, key, value):
        """__setattr__ special method redefined to keep an updated version of
        the RCluster configuration options saved. Allows for easy exporting and
        duplication of an RCluster configuration (see RCluster.fromConfig() and
        RCluster.writeConfig()).
        """
        if '_config' in self.__dict__ and key in self._kwargs:
            log.info('Setting configuration attribute %s', key)
            self._config[key] = value
        super().__setattr__(key, value)

    def writeConfig(self, fn):
        """Write out RCluster configuration data as JSON.

        Keyword arguments:
        fn -- The filename to be written, will overwrite previous file
        """
        with open(fn, 'w') as out:
            json.dump(self._config, out, indent=2, sort_keys=True)

    def fromConfig(fn, **kwargs):
        """
        Use RCluster JSON configuration to create RCluster object.
        Prompts the user to input mandatory configuration values that are
        missing (i.e., AWS access credentials).

        Keyword arguments:
        fn -- The filename containing RCluster configuration data
        kwargs -- Alternate or supplement RCluster configuration; will override
            the content of fn
        """
        with open(fn, 'r') as out:
            dic = json.load(out)
        dic.update(kwargs)
        for key in sorted(dic):
            if dic[key] is None:
                dic[key] = input(key + ': ')
        return RCluster(**dic)

    def createInstances(self, n_instances, **kwargs):
        """Create EC2 instances using RCluster's configuration.

        Keyword arguments:
        n_instances -- The number of instances to be created
        kwargs -- arbitrary arguments to boto3 Session Resource
            ec2.create_instances; will supersede RCluster.instance_conf content
        """
        log.info('Creating %d instances.', n_instances)
        conf = self.instance_conf.copy()
        conf.update(kwargs)
        instances = self.ec2.create_instances(
            DryRun=False,
            MinCount=n_instances,
            MaxCount=n_instances,
            KeyName=self.key_name,
            **conf
        )
        instances[0].wait_until_running()
        sleep(5)
        for instance in instances:
            instance.create_tags(DryRun=False,
                                 Tags=[{'Key': 'rcluster', 'Value': self.ver}])
        ids = [instance.id for instance in instances]
        return list(self.ec2.instances.filter(InstanceIds=ids))

    def createCluster(self, n_workers=1, setup_pause=60, **kwargs):
        """Initialize the cluster.
        Launch a manager instance and n_workers worker instances, automating the
        configuration of their shared networking.

        Keyword arguments:
        n_workers -- Number of worker instances to launch (default 1)
        setup_pause -- Pause time to allow manager and workers to boot before
            attempting configuration steps (default 60)
        """
        log.info('Creating cluster of', n_workers, 'workers.')
        instances = self.createInstances(n_workers + 1, **kwargs)
        manager = instances[0]
        manager.create_tags(DryRun=False,
                            Tags=[{'Key': self.ver, 'Value': 'master'}])
        workers = instances[1:]
        sleep(setup_pause)
        self.manager_private = getattr(manager, 'private_ip_address')
        self.access_ip = getattr(manager, self.ip_ref)
        try:  # TODO: thread
            self.hostfile = ''
            for worker in workers:
                log.info('Configuring Worker %s', worker.instance_id)
                client = self.connect(worker)
                cpus = rcl.cpuCount(client)
                self.hostfile += (worker.private_ip_address + '\n') * cpus
                if self.worker_runtime:
                    rcl.pmkCmd(client,
                               self.worker_runtime.format(**self.__dict__))
            log.info('Configuring manager %s', manager.instance_id)
            client = self.connect(manager)
            cpus = rcl.cpuCount(client) - 1
            self.hostfile += (manager.private_ip_address + '\n') * cpus
            if self.manager_runtime:
                rcl.pmkCmd(client, self.manager_runtime.format(**self.__dict__))
        except Exception as err:
            log.error('Error during instance configuration: %s', err)
            raise err

    def connect(self, instance):
        """
        Create SSH connection to boto3.EC2.Instance as paramiko.client.

        Keyword arguments:
        instance -- A boto3.EC2.Instance object
        """
        host = getattr(instance, self.ip_ref)
        key_path = self.key_path
        return rcl.pmkConnect(host, key_path)

    def retrieveAccessIp(self):
        """
        Identify the master's access IP address (if a master has been defined).
        """
        master = list(self.ec2.instances.filter(
            DryRun=False,
            Filters=[
                {'Name': 'tag-key', 'Values': [self.ver]},
                {'Name': 'tag-value', 'Values': ['master']},
                {'Name': 'instance-state-name',
                 'Values': ['running', 'pending']}
            ]))
        if master:
            return getattr(master[0], self.ip_ref)
        else:
            log.info("No active rcluster found")

    def terminateInstances(self, ver=None):
        """
        Terminate EC2.Instance objects created by the current configuration
        file.
        """
        if not ver:
            ver = self.ver
        instances = self.ec2.instances.filter(
            DryRun=False,
            Filters=[
                {'Name': 'tag-key', 'Values': ['rcluster']},
                {'Name': 'tag-value', 'Values': [ver]},
                {'Name': 'instance-state-name',
                 'Values': ['running', 'pending']}
            ])
        if instances:
            [instance.terminate() for instance in instances]
        else:
            log.info("No instances terminated.")

    def createAmi(self, base=None, setup_fn=None, ver=None, update_image=True,
                  terminate=True, wait=True):
        """
        Create an AMI, returning the AMI ID.

        Keyword arguments:
        base -- boto3.EC2.Instance object or nothing; optional to allow for
            snapshotting
        setup_fn -- The shell script used to configure the instance; optional
            to allow for snapshotting
        ver -- Name of AMI, defaults to self.ver
        update_image -- Flag; whether to change the RCluster's instance_conf AMI
            ID to that of the new image
        terminate -- Flag; whether to terminate the instance used to build the
            AMI (useful for debugging)
        """
        if not base:
            log.info('Creating base instance for AMI generation.')
            base = self.createInstances(1, InstanceType='m4.large')[0]
            sleep(20)
        if setup_fn:
            client = self.connect(base)
            sftp_conn = client.open_sftp()
            sftp_conn.put(setup_fn, 'setup.sh')
            log.info('Setup script %s, running configuration.', setup_fn)
            rcl.pmkCmd(client, 'sudo bash setup.sh')
        if not ver:
            ver = self.ver
        log.info('Creating AMI %s', self.ver)
        image = base.create_image(
            DryRun=False,
            Name=ver,
            Description="RCluster AMI",
            NoReboot=False
        )
        base.wait_until_running()
        if wait:
            while 'available' not in self.ec2.Image(image.id).state:
                log.debug('Waiting for AMI %s to become available', image.id)
                sleep(20)
        if terminate:
            base.terminate()
        if update_image:
            self.instance_conf['ImageId'] = image.id
        return image.id


def _ec2Purge(ec2_res, ver):
    """
    Utility to clear an AWS account of previous RCluster settings (useful for
    development). Removes resources associated with a provided version:
    * Terminates instances with the tag key 'rcluster' and value `ver`
    * Deregisters AMI named `ver`
    * Deletes key-pair named `ver`
    * Deletes placement group named `ver`
    * Deletes security group named `ver`

    Keyword arguments:
    ec2_res: A boto3.EC2.ServiceResource
    ver: The "version" to delete
    """
    log.info('Purging %s configurations', ver)
    instances = ec2_res.instances.filter(
        DryRun=False,
        Filters=[
            {'Name': 'tag-key', 'Values': ['rcluster']},
            {'Name': 'tag-value', 'Values': [ver]},
            {'Name': 'instance-state-name',
             'Values': ['running', 'pending']}
        ])
    [instance.terminate() for instance in instances]
    images = ec2_res.images.filter(
        DryRun=False,
        Filters=[{'Name': 'name', 'Values': [ver]}]
    )
    [image.deregister() for image in images]
    key_pairs = ec2_res.key_pairs.filter(
        DryRun=False,
        Filters=[{'Name': 'key-name', 'Values': [ver]}]
    )
    [key_pair.delete() for key_pair in key_pairs]
    placement_groups = ec2_res.placement_groups.filter(
        DryRun=False,
        Filters=[{'Name': 'group-name', 'Values': [ver]}]
    )
    [placement_group.delete() for placement_group in placement_groups]
    security_groups = ec2_res.security_groups.filter(
        DryRun=False,
        Filters=[{'Name': 'group-name', 'Values': [ver]}]
    )
    [security_group.delete() for security_group in security_groups]
