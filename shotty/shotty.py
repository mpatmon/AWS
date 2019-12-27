import boto3
import botocore
#import sys
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def return_instances(project):
    instances = []

    if project:
       print(project + ' instances')
       filters = [{'Name':'tag:Projet', 'Values':[project]}]
       instances = ec2.instances.filter(Filters=filters)
    else:
        print('All instances !')
        instances = ec2.instances.all()

    return instances

def snapshot_pending(volume):
    snapshots - list(volume.snapshots.all())
    return snapshots and snapshots[0].state == 'pending'

@click.group()
def cli():
    """Shotty manages vms"""


@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""
@snapshots.command('list')
@click.option('--project', default=None,
        help="Only snapshotss for project (tag Project:<name>)")
@click.option('--all', 'list_all', default=False, is_flag=True,
              help="List all snapshots for each volume, not just the most recent")
def list_snapshotss(project, list_all):
    "List EC2 snapshots"

    instances = return_instances(project)
    
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                        s.id,
                        v.id,
                        s.state,
                        s.progress,
                        s.start_time.strftime("%c")
                        
                    )))
                if s.state == 'completed' and not list_all: break
    return

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
        help="Only instances for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 volumes"

    instances = return_instances(project)
    
    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                i.id,
                v.id,
                str(v.size) + "GiB",
                v.state
                )))
    return

@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,
        help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"

    instances = return_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or []}
        print(','.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))
    return


@instances.command('snapshot',
                   help="Create snapshots of all volumes")
@click.option('--project', default=None,
        help="Only snapshotss for project (tag Project:<name>)")
def create_snapshots(project):
    """Create snapshots for EC2 instances"""

instances = return_instances(project)

for i in instances:
    print("Stopping {0}...".format(v.id))
    i.stop()
    i.wait_until_stopped()
    for v in i.volumes.all():
        if snapshot_pending(v):
            print("Skipping. ...Snapshot is already pending")
            continue
        print("Creating snapshot of {0}".format(v.id))
        v.create_snapshots(Description="Created by Melvin P. DXC")
    print("Starting {0}...".format(i.id))
    i.start()   
    i.wait_until_running()
    print("Complete!!!")
    return



@instances.command('stop')
@click.option('--project', default=None,
        help="Only instances for project")
def stop_instances(project):
    "Stop EC2 instances"
    
    instances = return_instances(project)

    for i in instances:
        print("Stopping instances {0}...".format(i.id))
        try:
            i.stop()
        except:
            print("Failed to stop instance {0}".format(i.id) + str(e))
            continue

    return      

@instances.command('start')
@click.option('--project', default=None,
        help="Only instances for project")
def start_instances(project):
    "Start EC2 instances"

    instances = return_instances(project)

    for i in instances:
        print("Starting instances {0}...".format(i.id))
        
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print(" Failed to start instance {0}".format(i.id) + str(e))
            continue

    return

@instances.command('terminate')
@click.option('--project', default=None,
        help="Only terminate instances for project")
def terminate_instances(project):
    "Terminate EC2 instances"
    
    instances = return_instances(project)
    
    for i in instances:
        print("Terminating instance {0} ".format(i.id) )
        try:
            i.terminate()
        except:
            print("Failed to terminate instance.")
        
    return


if __name__ == '__main__':
    cli()
    
    
    #list_instances() 
    #print(sys.argv)

