# AWS Inventory Scanner

A comprehensive AWS resource inventory scanner that discovers and catalogs AWS resources across all regions in your account.

## Overview

The AWS Inventory Scanner is a powerful tool designed to help you discover, catalog, and inventory AWS resources across your entire AWS account. It provides comprehensive coverage of 25+ AWS services and can scan all regions concurrently for fast and efficient resource discovery.

## Key Features

* **Multi-region scanning**: Scans all AWS regions by default, with option to specify specific regions
* **Comprehensive coverage**: Supports 25+ AWS services including EC2, S3, RDS, Lambda, and more
* **Concurrent processing**: Uses multithreading for fast, efficient scanning
* **JSON output**: Saves detailed resource information in structured JSON format
* **CLI interface**: Easy-to-use command-line interface with flexible options
* **AWS profile support**: Works with AWS CLI profiles and IAM roles
* **Python API**: Programmatic access for integration with other tools

## Quick Start

### Installation

```bash
pip install aws-inventory-scanner
```

### Basic Usage

```bash
# Scan all regions with default settings
aws-inventory-scanner

# Scan specific regions
aws-inventory-scanner --region us-east-1 --region us-west-2

# Use specific AWS profile
aws-inventory-scanner --profile my-aws-profile
```

## Use Cases

* **Cloud Asset Management**: Maintain an up-to-date inventory of all AWS resources
* **Security Auditing**: Identify resources that may not comply with security policies
* **Cost Optimization**: Discover unused or underutilized resources
* **Compliance Reporting**: Generate reports for compliance and governance requirements
* **Migration Planning**: Catalog existing resources before migration projects
* **Disaster Recovery**: Maintain resource inventories for DR planning

## Architecture

The scanner uses a multi-threaded architecture to efficiently scan multiple AWS services and regions concurrently. It leverages the AWS SDK for Python (boto3) and implements proper error handling and retry logic for reliable operation.

## Next Steps

* [Installation Guide](installation.md) - Detailed installation instructions
* [Usage Guide](usage.md) - Comprehensive usage examples
* [Supported Services](services.md) - Complete list of supported AWS services
* [API Reference](api.md) - Python API documentation
