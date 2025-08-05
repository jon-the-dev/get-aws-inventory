# AWS Inventory Scanner

A comprehensive AWS resource inventory scanner that discovers and catalogs AWS resources across all regions in your account.

## Features

* **Multi-region scanning**: Scans all AWS regions by default, with option to specify specific regions
* **Comprehensive coverage**: Supports 25+ AWS services including EC2, S3, RDS, Lambda, and more
* **Concurrent processing**: Uses multithreading for fast, efficient scanning
* **JSON output**: Saves detailed resource information in structured JSON format
* **CLI interface**: Easy-to-use command-line interface with flexible options
* **AWS profile support**: Works with AWS CLI profiles and IAM roles

## Installation

### From PyPI (recommended)

```bash
pip install aws-inventory-scanner
```

### From source

```bash
git clone https://github.com/yourusername/aws-inventory-scanner.git
cd aws-inventory-scanner
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Scan all regions (default)
aws-inventory-scanner

# Scan specific regions
aws-inventory-scanner --region us-east-1 --region us-west-2

# Use specific AWS profile
aws-inventory-scanner --profile my-aws-profile

# Specify output directory
aws-inventory-scanner --output-dir /path/to/output

# Adjust number of concurrent workers
aws-inventory-scanner --workers 50

# Enable verbose logging
aws-inventory-scanner --verbose
```

### Python API

```python
from aws_inventory_scanner import AWSInventoryScanner

# Create scanner instance
scanner = AWSInventoryScanner(
    regions=['us-east-1', 'us-west-2'],  # Optional: specify regions
    output_dir='./my-inventory',         # Optional: output directory
    workers=35                           # Optional: number of workers
)

# Run the scan
scanner.scan(profile_name='my-aws-profile')  # Optional: AWS profile
```

## Supported AWS Services

The scanner currently supports the following AWS services:

- **Compute**: EC2, Lambda, ECS, EKS, Elastic Beanstalk
- **Storage**: S3, EFS, FSx, Glacier
- **Database**: RDS, DynamoDB, ElastiCache, Redshift
- **Networking**: VPC, ELB, CloudFront, Route53
- **Security**: IAM, Secrets Manager, GuardDuty, WAF
- **Management**: CloudFormation, CloudWatch, Config, Backup
- **Developer Tools**: CodeBuild, CodeDeploy
- **Analytics**: Athena
- **Machine Learning**: SageMaker
- **And more...

## Output Format

The scanner creates JSON files for each service and region combination:

```
./inventory/
├── 123456789012-ec2-us-east-1-describe_instances-Reservations.json
├── 123456789012-s3-us-east-1-list_buckets-Buckets.json
├── 123456789012-rds-us-west-2-describe_db_instances-DBInstances.json
└── ...
```

Each file contains detailed resource information in JSON format, making it easy to process with other tools or scripts.

## Requirements

- Python 3.8 or higher
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- Appropriate AWS permissions to read resources

## AWS Permissions

The scanner requires read-only permissions for the AWS services you want to inventory. Consider using the `ReadOnlyAccess` managed policy or create a custom policy with specific read permissions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v0.1.0
- Initial release
- Support for 25+ AWS services
- Multi-region scanning
- CLI interface
- Python API
