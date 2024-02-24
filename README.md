# File Validation

AWS File validation using lambda function using AI/ML model from Google's Magika Project.

For more details read [post](https://dmdhrumilmistry.gitbook.io/home/blog/secure-software-development/validating-file-content-types-to-avoid-malicious-file-hosting-using-ml-model)

## Usage

### Using Amazon ECR

> Note: use x86_64 arch instead of arm64 since arm64 arch machines doesn't completely support
> environment required by onnix
>
> Reference: https://github.com/microsoft/onnxruntime/issues/10038

#### Installation

* Star (⭐️) and Fork (⑂) this Repo 😎

* Update `bucket_policy` in `file_validation.py` according to your needs.

* Create ECR Private Registry and new container repo (let's say `file-validation`)

* Create new IAM Role Policy with restricted permissions for accessing bucket (`my-aws-buckkett`) and deleting (malicious) objects for `aws-s3-file-upload-validation` lambda function (which will be created later)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "GetAndDeleteBucketObject",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::my-aws-buckkett/*",
                "arn:aws:s3:::my-aws-buckkett/",
                "arn:aws:s3:::my-aws-buckkett"
            ]
        },
        {
            "Sid":"CreateLogGroupActionForLambda",
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-1:aws-account-number:*"
        },
        {
            "Sid":"CreateAndPushLogsFromLambda",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:aws-account-number:log-group:/aws/lambda/aws-s3-file-upload-validation:*"
            ]
        }
    ]
}
```

* Login to AWS docker

```bash
aws ecr get-login-password --region us-east-1 --profile profile-name | docker login --username AWS --password-stdin aws-acc-number.dkr.ecr.us-east-1.amazonaws.com
```

* Now build docker image and push to AWS ECR using below commands or Use [github action](./.github/workflows/build-ecr-image.yml)

```bash
docker buildx build -t aws-acc-number.dkr.ecr.us-east-1.amazonaws.com/file-validation:latest
docker push aws-acc-number.dkr.ecr.us-east-1.amazonaws.com/file-validation:latest
```

* Create `aws-s3-file-upload-validation` lambda function configure ECR image, IAM role policy, memory and timeout.

* Create s3 trigger event for object creation and link it to trigger lambda function

* Test Lambda function by uploading valid and invalid content type files.

### Using Zip (Might Not Work Properly)

* Build Zip

```bash
make all
```

* Upload zip to lambda function
