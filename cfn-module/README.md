
Prerequisites:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install cloudformation-cli

Create new module:

    cd <directory>
    cfn init

    Initializing new project
    Do you want to develop a new resource(r) or a module(m) or a hook(h)?.
    >> m
    What's the name of your module type?
    (<Organization>::<Service>::<Name>::MODULE)
    >> MYORG::IAM::DynamoDBScannerPolicyV1::MODULE

Customize fragment

Update the json file created at the beginning, the file can be renamed to whatever fit best.

Deploy module:

    cfn submit

    Module fragment is valid.
    Successfully submitted type. Waiting for registration with token '806a6151-50f2-4d10-8a45-c5954310a5e7' to complete.
    Registration complete.
    {'ProgressStatus': 'COMPLETE', 'Description': 'Deployment is currently in DEPLOY_STAGE of status COMPLETED', 'TypeArn': 'arn:aws:cloudformation:us-east-1:501533612229:type/module/MYORG-IAM-DynamoDBScannerPolicyV1-MODULE', 'TypeVersionArn': 'arn:aws:cloudformation:us-east-1:501533612229:type/module/MYORG-IAM-DynamoDBScannerPolicyV1-MODULE/00000001', 'ResponseMetadata': {'RequestId': '5f239acd-775a-431f-a727-5c55e6a1eb40', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '5f239acd-775a-431f-a727-5c55e6a1eb40', 'content-type': 'text/xml', 'content-length': '713', 'date': 'Sun, 21 Aug 2022 23:19:58 GMT'}, 'RetryAttempts': 0}}

Test module:

Deploy test-dynamodb-table-iam-module.yaml from the AWS Console or the next command:

    aws cloudformation create-stack --stack-name test-dynamodb-table-iam-module --template-body file://test-dynamodb-table-iam-module.yaml --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM

That should create an IAM Policy like this one:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "dynamodb:Scan"
                ],
                "Resource": "arn:aws:dynamodb:us-east-1:501533612229:table/table1",
                "Effect": "Allow"
            }
        ]
    }    

Based on:
https://medium.com/contino-engineering/using-cloudformation-modules-to-improve-iam-least-privilege-c94c4dfecaca

Official repo/doc: https://github.com/aws-cloudformation/cloudformation-cli
