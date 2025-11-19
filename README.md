# AWS Inventory Scanner

A comprehensive AWS resource inventory scanner that discovers and catalogs AWS resources across all regions in your account.

## Features

* **Multi-region scanning**: Scans all AWS regions by default, with option to specify specific regions
* **Comprehensive coverage**: Supports 25+ AWS services including EC2, S3, RDS, Lambda, and more
* **Tag analysis & reporting**: NEW! Extract and analyze tags from inventory data with compliance checking
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

# Generate tag analysis report from existing inventory
aws-inventory-scanner --generate-tag-report

# Check tag compliance with required tags
aws-inventory-scanner --generate-tag-report \
  --required-tags Name Environment Owner CostCenter
```

### Tag Analysis

After scanning your AWS resources, you can generate comprehensive tag reports:

```bash
# Generate tag analysis reports (summary, detailed, and CSV)
aws-inventory-scanner --generate-tag-report

# Check compliance with required tags
aws-inventory-scanner --generate-tag-report \
  --required-tags Environment Owner CostCenter

# Analyze tags in specific directory
aws-inventory-scanner --generate-tag-report --output-dir /path/to/inventory
```

The tag analyzer generates three types of reports:

- **Summary Report**: Tag coverage statistics, most common tags, service breakdown
- **Detailed Report**: Untagged resources, tag inconsistencies, resources by tag
- **CSV Report**: All tags in spreadsheet format for analysis

See the [Tag Analysis Documentation](docs/tag-analysis.md) for detailed usage.

### Python API

```python
from aws_inventory_scanner import AWSInventoryScanner, TagAnalyzer

# Create scanner instance
scanner = AWSInventoryScanner(
    regions=['us-east-1', 'us-west-2'],  # Optional: specify regions
    output_dir='./my-inventory',         # Optional: output directory
    workers=35                           # Optional: number of workers
)

# Run the scan
scanner.scan(profile_name='my-aws-profile')  # Optional: AWS profile

# Analyze tags
analyzer = TagAnalyzer(inventory_dir='./my-inventory')
tags_data = analyzer.extract_tags_from_directory()
report_files = analyzer.generate_tag_report(tags_data)

# Check compliance
required_tags = ['Environment', 'Owner', 'CostCenter']
compliance = analyzer.generate_compliance_report(
    tags_data,
    required_tags,
    output_file='compliance-report.json'
)
print(f"Tag compliance: {compliance['compliance_percentage']}%")
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

## Documentation

- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [Tag Analysis Documentation](docs/tag-analysis.md) - NEW!
- [Supported Services](docs/services.md)
- [Output Format](docs/output.md)
- [API Reference](docs/api.md)
- [Implementation Guide](IMPLEMENTATION_GUIDE.md) - Guide for adding new services

## Changelog

### v0.2.0 (Planned)
- **NEW**: Tag analysis and reporting feature
  - Extract tags from all inventory files
  - Generate summary, detailed, and CSV reports
  - Tag compliance checking with required tags
  - Tag inconsistency detection
- **NEW**: Comprehensive guide for adding 50+ additional AWS services
- Enhanced documentation with tag analysis guide
- Added TagAnalyzer class to Python API

### v0.1.0
- Initial release
- Support for 25+ AWS services
- Multi-region scanning
- CLI interface
- Python API
