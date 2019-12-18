import boto3
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

@click.group()
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

@instances.command('stop')
@click.option('--project', default=None,
        help="Only instances for project")
def stop_instances(project):
    "Stop EC2 instances"
    
    instances = return_instances(project)

    for i in instances:
        print("Stopping instances {0}...".format(i.id))
        i.stop()

    return      

@instances.command('start')
@click.option('--project', default=None,
        help="Only instances for project")
def start_instances(project):
    "Start EC2 instances"

    instances = return_instances(project)

    for i in instances:
        print("Starting instances {0}...".format(i.id))
        i.start()

    return




if __name__ == '__main__':
    instances()
    
    
    #list_instances() 
    #print(sys.argv)

