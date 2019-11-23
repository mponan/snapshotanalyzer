#import part - imports functions/modules needed for the project
import boto3
import click

#initialised variables for the Project
session = boto3.Session(profile_name = 'shotty')
ec2 = session.resource('ec2')

#filters the isntances
def filter_instances(project):
    #create a blank list
    instances = []

    #checks if the project value is true
    if project:
        #this is another dictionary, that checks out the project and tag from EC2 console
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        #gets the project/tag and assign to variable instances
        instances = ec2.instances.filter(Filters=filters)
    else:
        #returns all instances if project parameter used is not available
        instances = ec2.instances.all()

    return instances

#click functions - wraps the functions
@click.group()
def instances():
    """Commands for instances"""

###########################################
#beginning of the 'list' command
###########################################

@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

#function definition for the script
#must define the project/tag name to run the function
def list_instances(project):
    #python text list_instances
    "List EC2 Instances"

    instances = filter_instances(project)

    #gets all the instances and return to the screen
    for i in instances:
        #gets the tag value for each of the instances
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name,
        tags.get('Projects', '<no project>')
        )))

    return

###########################################
#beginning of the 'stop' command
###########################################

@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

def stop_instances(project):
        #python text list_instances
        "Stop EC2 Instances"

        instances = filter_instances(project)

        for i in instances:
            print("Stopping {0}...".format(i.id))
            i.stop()

        return

###########################################
#beginning of the 'start' command
###########################################

@instances.command('start')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")

def stop_instances(project):
        #python text list_instances
        "Stop EC2 Instances"

        instances = filter_instances(project)

        for i in instances:
            print("Starting {0}...".format(i.id))
            i.start()

        return

if __name__ == '__main__':
    instances()
