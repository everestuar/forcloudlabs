import json
import boto3
import urllib3

#Initialize boto client for AWS Backup
backup = boto3.client('backup')

def lambda_handler(event, context):
    #Print the incoming event
    print('Incoming Event:' + json.dumps(event))

    input_event = event

    #Determine job type based on event - backup completed vs restore completed
    job_type = event['detail-type'].split(' ')[0]

    #Print the job type
    print(job_type + ' job completed')

    try:
        if job_type == 'Backup':
            handleBackup(input_event)
        elif job_type == 'Restore':
            handleRestore(input_event)
    except Exception as e:
        print(str(e))
        return

def handleBackup(input_event):
    #Get backup job ID from incoming event
    backup_job_id = input_event['detail']['backupJobId']
    print('Backup job ID: ' + backup_job_id)

    #Get backup job details
    backup_info = backup.describe_backup_job(
                    BackupJobId=backup_job_id
                )
    recovery_point_arn = backup_info['RecoveryPointArn']
    iam_role_arn = backup_info['IamRoleArn']
    backup_vault_name = backup_info['BackupVaultName']
    print('Recovery point ARN: ' + recovery_point_arn)
    print('IAM role ARN: ' + iam_role_arn)
    print('Backup vault name: ' + backup_vault_name)

    #Get recovery point restore metadata
    print('Retrieving recovery point restore metadata')
    metadata = backup.get_recovery_point_restore_metadata(
        BackupVaultName=backup_vault_name,
        RecoveryPointArn=recovery_point_arn
    )

    #Set values for restore metadata
    print('Setting restore metadata values')
    metadata['RestoreMetadata']['CpuOptions'] = '{}'
    metadata['RestoreMetadata']['NetworkInterfaces'] = '[]'

    #API call to start the restore job
    print('Starting the restore job')
    restore_request = backup.start_restore_job(
            RecoveryPointArn=recovery_point_arn,
            IamRoleArn=iam_role_arn,
            Metadata=metadata['RestoreMetadata']
    )

    print(json.dumps(restore_request))

    return

def handleRestore(input_event):
    #Get restore job ID from incoming event
    restore_job_id = input_event['detail']['restoreJobId']
    print('Restore job ID: ' + restore_job_id)

    #Get restore job details
    restore_info = backup.describe_restore_job(
                    RestoreJobId=restore_job_id
                )

    print('Restore from the backup was successful')

    #Retrieve instance ID for the new instance from restore job details
    instance_id = input_event['detail']['createdResourceArn'].split(':')[5].split('/')[1]
    print('New instance created: ' + instance_id)

    print('Validating data recovery before deletion.')

    #validating data recovery

    #Get public IP of the new EC2 instance
    ec2 = boto3.client('ec2')
    instance_details = ec2.describe_instances(
                InstanceIds=[
                    instance_id
                ]
            )
    public_ip = instance_details['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print('Data recovery validation endpoint: ' + public_ip)

    #Validate data recovery by making HTTP GET request to public IP of the new EC2 instance
    http = urllib3.PoolManager()
    url = public_ip
    try:
        print('Sending HTTP GET request')
        resp = http.request('GET', url)
        print('Received response: ' + str(resp.status))

        #Verify if a valid response was received
        if resp.status == 200:
            print('Valid response received. Data recovery validated. Proceeding with deletion.')
            print('Deleting: ' + instance_id)

            #Delete new EC2 instance if valid response was received
            delete_request = ec2.terminate_instances(
                        InstanceIds=[
                            instance_id
                        ]
                    )
            print('Restore from ' + restore_info['RecoveryPointArn'] + ' was successful. Data recovery validation succeeded with HTTP ' + str(resp.status) + ' returned by the application. ' + 'The newly created resource ' + restore_info['CreatedResourceArn'] + ' has been cleaned up.')
        else:
            #Resource not deleted if invalid response received
            print('Invalid response received: HTTP ' + str(resp.status) + '. Data Validation FAILED. New resource ' + restore_info['CreatedResourceArn'] + ' has NOT been cleaned up.')
    except Exception as e:
        print('Error connecting to the application: ' + str(e))

    return
