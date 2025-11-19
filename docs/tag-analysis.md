# Tag Analysis

The AWS Inventory Scanner includes a powerful tag analysis feature that helps you understand, audit, and maintain your AWS resource tagging strategy.

## Overview

The tag analyzer extracts and analyzes tags from all inventory files, providing insights into:

- **Tag Coverage**: Which resources have tags and which don't
- **Tag Distribution**: Most commonly used tag keys and values
- **Tag Compliance**: Resources missing required tags
- **Tag Inconsistencies**: Similar tag keys that might need standardization
- **Service Breakdown**: Tag coverage by AWS service

## Quick Start

### Generate Tag Reports from Existing Inventory

After running an inventory scan, generate tag reports:

```bash
aws-inventory-scanner --generate-tag-report
```

This creates three report files in your inventory directory:

- `tag-report-summary-YYYYMMDD_HHMMSS.json` - Summary statistics
- `tag-report-detailed-YYYYMMDD_HHMMSS.json` - Detailed analysis
- `tag-report-YYYYMMDD_HHMMSS.csv` - All tags in CSV format

### Specify Output Directory

```bash
aws-inventory-scanner --generate-tag-report --output-dir ./my-inventory
```

### Check Tag Compliance

Verify that resources have required tags:

```bash
aws-inventory-scanner --generate-tag-report \
  --required-tags Environment Owner CostCenter
```

This generates an additional compliance report showing which resources are missing required tags.

## Report Formats

### Summary Report

The summary report provides high-level statistics:

```json
{
  "generated_at": "2025-11-19T10:30:00Z",
  "summary": {
    "total_resources": 1547,
    "resources_with_tags": 1203,
    "resources_without_tags": 344,
    "tag_coverage_percent": 77.75,
    "unique_tag_keys": 47,
    "total_tag_entries": 5431
  },
  "tag_key_frequency": {
    "Name": 1203,
    "Environment": 987,
    "Owner": 856,
    "CostCenter": 654
  },
  "top_tag_values": {
    "Environment": {
      "production": 456,
      "staging": 312,
      "development": 219
    }
  },
  "service_breakdown": {
    "ec2": {
      "total": 450,
      "tagged": 425,
      "untagged": 25
    },
    "s3": {
      "total": 87,
      "tagged": 82,
      "untagged": 5
    }
  }
}
```

### Detailed Report

The detailed report includes:

**Untagged Resources:**
```json
{
  "untagged_resources": [
    {
      "service": "s3",
      "region": "us-east-1",
      "resource_type": "Buckets",
      "resource_id": "my-old-bucket"
    }
  ],
  "untagged_count": 344
}
```

**Tag Inconsistencies:**
```json
{
  "tag_inconsistencies": [
    {
      "similar_keys": ["Environment", "environment", "env"],
      "recommendation": "Standardize to one format",
      "pattern": "environment"
    }
  ]
}
```

**Resources by Tag Key:**
```json
{
  "resources_by_tag_key": {
    "Environment": {
      "count": 987,
      "unique_values": 3,
      "sample_resources": [
        {
          "service": "ec2",
          "region": "us-east-1",
          "resource_id": "i-1234567890abcdef0",
          "value": "production"
        }
      ]
    }
  }
}
```

### CSV Report

The CSV report contains all tags in a flat format, suitable for importing into spreadsheet applications or databases:

```csv
AccountID,Service,Region,ResourceType,ResourceID,TagKey,TagValue
123456789012,ec2,us-east-1,Reservations,i-1234567890abcdef0,Name,WebServer1
123456789012,ec2,us-east-1,Reservations,i-1234567890abcdef0,Environment,production
123456789012,s3,us-east-1,Buckets,my-bucket,CostCenter,Engineering
```

## Compliance Checking

### Required Tags

Specify required tags to generate a compliance report:

```bash
aws-inventory-scanner --generate-tag-report \
  --required-tags Name Environment Owner CostCenter Project
```

### Compliance Report

The compliance report shows:

```json
{
  "generated_at": "2025-11-19T10:30:00Z",
  "required_tags": ["Name", "Environment", "Owner", "CostCenter"],
  "total_resources": 1547,
  "compliant_resources": 856,
  "non_compliant_resources": 691,
  "compliance_percentage": 55.33,
  "non_compliant_details": [
    {
      "service": "ec2",
      "region": "us-east-1",
      "resource_id": "i-9876543210fedcba0",
      "missing_tags": ["Owner", "CostCenter"]
    }
  ]
}
```

## Python API

### Basic Usage

```python
from aws_inventory_scanner import TagAnalyzer

# Create analyzer
analyzer = TagAnalyzer(inventory_dir="./inventory")

# Extract tags from all files
tags_data = analyzer.extract_tags_from_directory()

# Generate reports
report_files = analyzer.generate_tag_report(tags_data)

print(f"Reports generated: {report_files}")
```

### Extract Tags from Single File

```python
result = analyzer.extract_tags_from_file(
    "./inventory/123456789012-ec2-us-east-1-describe_instances-Reservations.json"
)

for resource in result['resources']:
    print(f"Resource: {resource['resource_id']}")
    for tag in resource['tags']:
        print(f"  {tag['Key']}: {tag['Value']}")
```

### Find Missing Required Tags

```python
required_tags = ["Environment", "Owner", "CostCenter"]
missing = analyzer.find_missing_required_tags(tags_data, required_tags)

print(f"Found {len(missing)} resources missing required tags")
for resource in missing[:5]:
    print(f"{resource['service']}/{resource['resource_id']}: missing {resource['missing_tags']}")
```

### Generate Compliance Report

```python
compliance = analyzer.generate_compliance_report(
    tags_data,
    required_tags=["Name", "Environment", "Owner"],
    output_file="./compliance-report.json"
)

print(f"Compliance: {compliance['compliance_percentage']}%")
```

## Use Cases

### 1. Tag Coverage Audit

**Scenario**: You want to know what percentage of your AWS resources have tags.

```bash
aws-inventory-scanner --generate-tag-report
```

**Look for:**
- `summary.tag_coverage_percent` in the summary report
- `untagged_resources` in the detailed report

### 2. Cost Allocation Tag Validation

**Scenario**: Ensure all resources have CostCenter tags for billing purposes.

```bash
aws-inventory-scanner --generate-tag-report \
  --required-tags CostCenter
```

**Look for:**
- `compliance_percentage` in the compliance report
- Resources with missing CostCenter tag

### 3. Environment Segregation

**Scenario**: Verify all resources are properly tagged with Environment (production/staging/development).

```bash
aws-inventory-scanner --generate-tag-report
```

**Look for:**
- `top_tag_values.Environment` in the summary report
- Resources without Environment tag in untagged list

### 4. Tag Standardization

**Scenario**: Find and fix tag key inconsistencies (e.g., "environment" vs "Environment").

```bash
aws-inventory-scanner --generate-tag-report --verbose
```

**Look for:**
- `tag_inconsistencies` in the detailed report
- Similar keys that should be standardized

### 5. Security Tag Audit

**Scenario**: Ensure all resources have Owner tag for security accountability.

```bash
aws-inventory-scanner --generate-tag-report \
  --required-tags Owner
```

**Look for:**
- Resources missing Owner tag in compliance report
- Tag compliance percentage

## Tag Extraction Details

### Supported Tag Formats

The analyzer automatically detects and extracts tags in various AWS formats:

**Array Format (most common):**
```json
"Tags": [
  {"Key": "Name", "Value": "MyResource"},
  {"Key": "Environment", "Value": "production"}
]
```

**Dictionary Format:**
```json
"Tags": {
  "Name": "MyResource",
  "Environment": "production"
}
```

**Alternative Key Names:**
- `Tags`
- `TagList`
- `tags`
- `TagSet`
- `TagSpecifications`

### Resource Identification

The analyzer identifies resources using various ID fields:

- Generic: `ResourceId`, `Id`, `ARN`, `Name`
- EC2: `InstanceId`, `VolumeId`, `VpcId`, `SubnetId`, `GroupId`
- S3: `BucketName`
- RDS: `DBInstanceIdentifier`, `ClusterIdentifier`
- Lambda: `FunctionName`
- ELB: `LoadBalancerName`, `LoadBalancerArn`
- And many more...

If no standard field is found, it looks for any field ending with "Id" or "ID".

## Best Practices

### 1. Establish Tag Standards

Define a standard set of tags for your organization:

**Minimum Required Tags:**
- `Name` - Human-readable resource name
- `Environment` - production/staging/development/test
- `Owner` - Team or person responsible
- `CostCenter` - For billing allocation

**Recommended Tags:**
- `Project` - Project or application name
- `Compliance` - Compliance requirements (PCI, HIPAA, etc.)
- `BackupPolicy` - Backup schedule or policy
- `DataClassification` - public/internal/confidential/restricted

### 2. Use Consistent Tag Keys

Always use PascalCase for tag keys:
- ✅ `Environment`, `CostCenter`, `DataClassification`
- ❌ `environment`, `cost-center`, `data_classification`

### 3. Regular Audits

Schedule regular tag audits:

```bash
# Weekly audit script
#!/bin/bash
aws-inventory-scanner --region us-east-1 us-west-2
aws-inventory-scanner --generate-tag-report \
  --required-tags Name Environment Owner CostCenter
```

### 4. Remediation Workflow

1. **Generate report** to identify untagged resources
2. **Review CSV export** to find patterns
3. **Apply tags** using AWS CLI or console
4. **Re-run report** to verify compliance

### 5. Integration with CI/CD

Add tag compliance checks to your deployment pipelines:

```python
from aws_inventory_scanner import TagAnalyzer

analyzer = TagAnalyzer("./inventory")
tags_data = analyzer.extract_tags_from_directory()

required_tags = ["Environment", "Owner", "CostCenter"]
compliance = analyzer.generate_compliance_report(
    tags_data,
    required_tags
)

if compliance['compliance_percentage'] < 95:
    print(f"ERROR: Tag compliance is {compliance['compliance_percentage']}%")
    print(f"Required: 95% or higher")
    exit(1)
```

## Common Tag Patterns

### AWS Cost Allocation Tags

Enable these tags for cost allocation in AWS Cost Explorer:

```bash
aws-inventory-scanner --generate-tag-report \
  --required-tags CostCenter Project Environment
```

### AWS Backup Tags

For automated backups based on tags:

```bash
aws-inventory-scanner --generate-tag-report \
  --required-tags BackupPolicy
```

### Security and Compliance

```bash
aws-inventory-scanner --generate-tag-report \
  --required-tags DataClassification Compliance Owner
```

## Troubleshooting

### No Tags Found

**Issue**: Report shows 0 tags even though resources have tags.

**Solutions:**
1. Verify inventory files exist in the output directory
2. Check that inventory scan completed successfully
3. Ensure JSON files are valid (not .txt fallback files)
4. Some services may not include tags in their list/describe responses

### Incorrect Resource Identification

**Issue**: Resources show as "unknown" in reports.

**Solution**: The resource type may use a non-standard ID field. The analyzer tries common patterns, but some resources may need custom handling.

### Large Memory Usage

**Issue**: Tag analysis consumes too much memory with large inventories.

**Solution**: Process one service at a time by filtering JSON files:

```bash
# Process only EC2 tags
mkdir temp-ec2
cp *-ec2-*.json temp-ec2/
aws-inventory-scanner --generate-tag-report --output-dir temp-ec2
```

## Advanced Features

### Custom Tag Analysis

```python
from aws_inventory_scanner import TagAnalyzer

analyzer = TagAnalyzer("./inventory")
tags_data = analyzer.extract_tags_from_directory()

# Find resources with specific tag value
production_resources = [
    tag for tag in tags_data['tags']
    if tag['tag_key'] == 'Environment' and tag['tag_value'] == 'production'
]

print(f"Found {len(production_resources)} production resources")

# Find all unique tag keys
all_keys = set(tag['tag_key'] for tag in tags_data['tags'])
print(f"Unique tag keys: {sorted(all_keys)}")

# Count resources by service
from collections import Counter
service_counts = Counter(r['service'] for r in tags_data['resources'])
print(f"Resources by service: {service_counts}")
```

### Export to Database

```python
import sqlite3
from aws_inventory_scanner import TagAnalyzer

# Create database
conn = sqlite3.connect('aws_tags.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS resource_tags (
        account_id TEXT,
        service TEXT,
        region TEXT,
        resource_id TEXT,
        tag_key TEXT,
        tag_value TEXT,
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Load tag data
analyzer = TagAnalyzer("./inventory")
tags_data = analyzer.extract_tags_from_directory()

# Insert into database
for tag in tags_data['tags']:
    cursor.execute('''
        INSERT INTO resource_tags
        (account_id, service, region, resource_id, tag_key, tag_value)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        tag['account_id'],
        tag['service'],
        tag['region'],
        tag['resource_id'],
        tag['tag_key'],
        tag['tag_value']
    ))

conn.commit()
conn.close()
```

## See Also

- [Usage Guide](usage.md) - How to run inventory scans
- [Output Format](output.md) - Understanding inventory file format
- [API Reference](api.md) - Python API documentation
