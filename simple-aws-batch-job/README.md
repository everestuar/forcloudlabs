
Create job queue and compute environment: https://docs.aws.amazon.com/batch/latest/userguide/Batch_GetStarted.html

* Create Compute environment
* Create Job queue: Associates it to the compute environment
* Create Job definition: 
    * Set Execution role
    * Set Job role configuration
    * Specify "nobody" in Job role configuration

ecsTaskExecutionRole > AmazonECSTaskExecutionRolePolicy

Trust relationships:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "ecs-tasks.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }


Based on: https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/

ECR

    cd aws-batch-helpers-master/fetch-and-run
    docker build -t awsbatch/fetch_and_run .
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 580234752977.dkr.ecr.us-east-1.amazonaws.com
    docker tag awsbatch/fetch_and_run:latest 580234752977.dkr.ecr.us-east-1.amazonaws.com/awsbatch/fetch_and_run:latest
    docker push 580234752977.dkr.ecr.us-east-1.amazonaws.com/awsbatch/fetch_and_run:latest

* Create en S3 bucket to store sh script
* Copy sh script to the S3 bucket

        aws s3 cp myjob.sh s3://fetch-and-run-20220822/myjob.sh

* Create Job: 
    * Add Variables:
        * BATCH_FILE_S3_URL: s3://fetch-and-run-20220822/myjob.sh
        * BATCH_FILE_TYPE: script

* Inspect output on CloudWatch Logs
