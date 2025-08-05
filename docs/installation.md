# Installation

## Requirements

* Python 3.8 or higher
* AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
* Appropriate AWS permissions to read resources

## Installation Methods

### From PyPI (Recommended)

The easiest way to install the AWS Inventory Scanner is from PyPI:

```bash
pip install aws-inventory-scanner
```

### From Source

If you want to install from source or contribute to the project:

```bash
git clone https://github.com/yourusername/aws-inventory-scanner.git
cd aws-inventory-scanner
pip install -e .
```

### Using Virtual Environment (Recommended)

It's recommended to use a virtual environment to avoid conflicts with other Python packages:

```bash
# Create virtual environment
python -m venv aws-scanner-env

# Activate virtual environment
# On Linux/macOS:
source aws-scanner-env/bin/activate
# On Windows:
aws-scanner-env\Scripts\activate

# Install the scanner
pip install aws-inventory-scanner
```

## AWS Credentials Setup

The scanner requires AWS credentials to access your AWS resources. You can configure credentials using any of the following methods:

### AWS CLI Configuration

```bash
aws configure
```

### Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### IAM Roles (for EC2 instances)

If running on an EC2 instance, you can use IAM roles for authentication.

### AWS Profiles

You can use named profiles for different AWS accounts:

```bash
aws configure --profile my-profile
```

Then use the profile with the scanner:

```bash
aws-inventory-scanner --profile my-profile
```

## AWS Permissions

The scanner requires read-only permissions for the AWS services you want to inventory. Here are the recommended permission approaches:

### Option 1: AWS Managed Policy (Easiest)

Attach the `ReadOnlyAccess` managed policy to your IAM user or role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "arn:aws:iam::aws:policy/ReadOnlyAccess"
            ],
            "Resource": "*"
        }
    ]
}
```

### Option 2: Custom Policy (More Restrictive)

Create a custom policy with only the permissions needed for the services you want to scan:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "acm:ListCertificates",
                "athena:ListDataCatalogs",
                "autoscaling:Describe*",
                "backup:List*",
                "cloudformation:DescribeStacks",
                "cloudfront:List*",
                "cloudtrail:DescribeTrails",
                "cloudwatch:DescribeAlarms",
                "codebuild:ListProjects",
                "codedeploy:List*",
                "config:Describe*",
                "config:List*",
                "dynamodb:List*",
                "ec2:Describe*",
                "ecr:DescribeRepositories",
                "ecs:List*",
                "efs:DescribeFileSystems",
                "eks:ListClusters",
                "elasticache:Describe*",
                "elasticbeanstalk:DescribeEnvironments",
                "elb:Describe*",
                "es:Describe*",
                "fsx:DescribeFileSystems",
                "glacier:ListVaults",
                "guardduty:ListDetectors",
                "iam:List*",
                "kms:ListKeys",
                "lambda:ListFunctions",
                "network-firewall:ListFirewalls",
                "rds:Describe*",
                "redshift:DescribeClusters",
                "route53:ListHostedZones",
                "route53domains:ListDomains",
                "s3:ListAllMyBuckets",
                "sagemaker:List*",
                "secretsmanager:ListSecrets",
                "sns:ListTopics",
                "sqs:ListQueues",
                "ssm:GetParametersByPath",
                "sts:GetCallerIdentity",
                "sts:GetSessionToken",
                "waf:ListWebACLs",
                "workspaces:DescribeWorkspaces"
            ],
            "Resource": "*"
        }
    ]
}
```

## Verification

After installation, verify that the scanner is working correctly:

```bash
# Check if the command is available
aws-inventory-scanner --help

# Test with a dry run (if available)
aws-inventory-scanner --region us-east-1 --verbose
```

## Troubleshooting Installation

### Common Issues

1. **Permission Denied**: Make sure you have the necessary permissions to install Python packages
2. **Python Version**: Ensure you're using Python 3.8 or higher
3. **AWS Credentials**: Verify your AWS credentials are properly configured

### Getting Help

If you encounter issues during installation:

1. Check the [Troubleshooting](troubleshooting.md) guide
2. Review the error messages carefully
3. Ensure all requirements are met
4. Try installing in a fresh virtual environment
