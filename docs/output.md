# Output Format

The AWS Inventory Scanner generates structured JSON output files containing detailed information about your AWS resources. This page explains the output format, file organization, and how to work with the results.

## Directory Structure

The scanner creates a hierarchical directory structure to organize the inventory results:

```
./inventory/
├── 123456789012-ec2-us-east-1-describe_instances-Reservations.json
├── 123456789012-ec2-us-east-1-describe_security_groups-SecurityGroups.json
├── 123456789012-ec2-us-east-1-describe_vpcs-Vpcs.json
├── 123456789012-s3-us-east-1-list_buckets-Buckets.json
├── 123456789012-rds-us-west-2-describe_db_instances-DBInstances.json
├── 123456789012-lambda-eu-west-1-list_functions-Functions.json
└── ...
```

## File Naming Convention

Each output file follows a consistent naming pattern:

```
{account_id}-{service}-{region}-{api_method}-{response_key}.json
```

### Components Explained

- **account_id**: Your 12-digit AWS account ID (e.g., `123456789012`)
- **service**: AWS service name (e.g., `ec2`, `s3`, `rds`, `lambda`)
- **region**: AWS region code (e.g., `us-east-1`, `us-west-2`, `eu-west-1`)
- **api_method**: AWS API method used to collect the data (e.g., `describe_instances`, `list_buckets`)
- **response_key**: The key in the API response containing the resource list (e.g., `Reservations`, `Buckets`)

### Example Filenames

```
123456789012-ec2-us-east-1-describe_instances-Reservations.json
123456789012-s3-us-east-1-list_buckets-Buckets.json
123456789012-rds-us-west-2-describe_db_instances-DBInstances.json
123456789012-iam-us-east-1-list_users-Users.json
```

## JSON File Structure

Each JSON file contains an array of resources returned by the corresponding AWS API call. The structure follows the AWS API response format exactly.

### Example: EC2 Instances

```json
[
    {
        "Groups": [],
        "Instances": [
            {
                "AmiLaunchIndex": 0,
                "ImageId": "ami-0abcdef1234567890",
                "InstanceId": "i-1234567890abcdef0",
                "InstanceType": "t3.micro",
                "KeyName": "my-key-pair",
                "LaunchTime": "2023-01-15T10:30:00.000Z",
                "Monitoring": {
                    "State": "disabled"
                },
                "Placement": {
                    "AvailabilityZone": "us-east-1a",
                    "GroupName": "",
                    "Tenancy": "default"
                },
                "PrivateDnsName": "ip-10-0-1-100.ec2.internal",
                "PrivateIpAddress": "10.0.1.100",
                "ProductCodes": [],
                "PublicDnsName": "",
                "State": {
                    "Code": 16,
                    "Name": "running"
                },
                "StateTransitionReason": "",
                "SubnetId": "subnet-12345678",
                "VpcId": "vpc-87654321",
                "Architecture": "x86_64",
                "BlockDeviceMappings": [
                    {
                        "DeviceName": "/dev/xvda",
                        "Ebs": {
                            "AttachTime": "2023-01-15T10:30:01.000Z",
                            "DeleteOnTermination": true,
                            "Status": "attached",
                            "VolumeId": "vol-1234567890abcdef0"
                        }
                    }
                ],
                "ClientToken": "",
                "EbsOptimized": false,
                "EnaSupport": true,
                "Hypervisor": "xen",
                "NetworkInterfaces": [
                    {
                        "Association": {
                            "IpOwnerId": "amazon",
                            "PublicDnsName": "",
                            "PublicIp": "54.123.45.67"
                        },
                        "Attachment": {
                            "AttachTime": "2023-01-15T10:30:00.000Z",
                            "AttachmentId": "eni-attach-1234567890abcdef0",
                            "DeleteOnTermination": true,
                            "DeviceIndex": 0,
                            "Status": "attached"
                        },
                        "Description": "",
                        "Groups": [
                            {
                                "GroupName": "default",
                                "GroupId": "sg-12345678"
                            }
                        ],
                        "Ipv6Addresses": [],
                        "MacAddress": "02:ab:cd:ef:12:34",
                        "NetworkInterfaceId": "eni-1234567890abcdef0",
                        "OwnerId": "123456789012",
                        "PrivateDnsName": "ip-10-0-1-100.ec2.internal",
                        "PrivateIpAddress": "10.0.1.100",
                        "PrivateIpAddresses": [
                            {
                                "Association": {
                                    "IpOwnerId": "amazon",
                                    "PublicDnsName": "",
                                    "PublicIp": "54.123.45.67"
                                },
                                "Primary": true,
                                "PrivateDnsName": "ip-10-0-1-100.ec2.internal",
                                "PrivateIpAddress": "10.0.1.100"
                            }
                        ],
                        "SourceDestCheck": true,
                        "Status": "in-use",
                        "SubnetId": "subnet-12345678",
                        "VpcId": "vpc-87654321"
                    }
                ],
                "RootDeviceName": "/dev/xvda",
                "RootDeviceType": "ebs",
                "SecurityGroups": [
                    {
                        "GroupName": "default",
                        "GroupId": "sg-12345678"
                    }
                ],
                "SourceDestCheck": true,
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "MyWebServer"
                    },
                    {
                        "Key": "Environment",
                        "Value": "Production"
                    }
                ],
                "VirtualizationType": "hvm"
            }
        ],
        "OwnerId": "123456789012",
        "RequesterId": "",
        "ReservationId": "r-1234567890abcdef0"
    }
]
```

### Example: S3 Buckets

```json
[
    {
        "Name": "my-application-logs",
        "CreationDate": "2023-01-10T14:30:00.000Z"
    },
    {
        "Name": "my-static-website",
        "CreationDate": "2023-02-15T09:15:00.000Z"
    },
    {
        "Name": "my-backup-bucket",
        "CreationDate": "2023-03-01T16:45:00.000Z"
    }
]
```

## Data Processing Examples

### Using jq for JSON Processing

The JSON output can be easily processed using `jq` or other JSON processing tools:

```bash
# Count total EC2 instances across all files
find inventory -name "*-ec2-*-describe_instances-*.json" -exec jq -r '.[].Instances | length' {} \; | awk '{sum += $1} END {print sum}'

# List all running EC2 instances
find inventory -name "*-ec2-*-describe_instances-*.json" -exec jq -r '.[].Instances[] | select(.State.Name == "running") | .InstanceId' {} \;

# Get all S3 bucket names
jq -r '.[].Name' inventory/*-s3-*-list_buckets-*.json

# Find instances with specific tags
find inventory -name "*-ec2-*-describe_instances-*.json" -exec jq -r '.[].Instances[] | select(.Tags[]? | select(.Key == "Environment" and .Value == "Production")) | .InstanceId' {} \;

# Count resources by service
ls inventory/*.json | cut -d'-' -f2 | sort | uniq -c
```

### Python Processing Example

```python
import json
import os
from collections import defaultdict

def analyze_inventory(inventory_dir):
    """Analyze AWS inventory results."""
    
    resource_counts = defaultdict(int)
    service_regions = defaultdict(set)
    
    for filename in os.listdir(inventory_dir):
        if not filename.endswith('.json'):
            continue
            
        # Parse filename
        parts = filename.replace('.json', '').split('-')
        if len(parts) >= 5:
            account_id = parts[0]
            service = parts[1]
            region = parts[2]
            method = parts[3]
            key = parts[4]
            
            # Load and count resources
            filepath = os.path.join(inventory_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                resource_count = len(data)
                
            resource_counts[service] += resource_count
            service_regions[service].add(region)
            
            print(f"{service:20} {region:15} {resource_count:5} resources")
    
    print("\nSummary by Service:")
    for service, count in sorted(resource_counts.items()):
        regions = len(service_regions[service])
        print(f"{service:20} {count:5} resources across {regions} regions")

# Usage
analyze_inventory('./inventory')
```

### Bash Processing Example

```bash
#!/bin/bash

# Script to summarize AWS inventory results

INVENTORY_DIR="./inventory"

echo "AWS Inventory Summary"
echo "===================="

# Count total files
total_files=$(ls ${INVENTORY_DIR}/*.json 2>/dev/null | wc -l)
echo "Total inventory files: $total_files"

# Count by service
echo -e "\nResources by Service:"
echo "--------------------"
for service in $(ls ${INVENTORY_DIR}/*.json | cut -d'-' -f2 | sort | uniq); do
    count=$(ls ${INVENTORY_DIR}/*-${service}-*.json | wc -l)
    echo "$service: $count files"
done

# Count by region
echo -e "\nFiles by Region:"
echo "---------------"
for region in $(ls ${INVENTORY_DIR}/*.json | cut -d'-' -f3 | sort | uniq); do
    count=$(ls ${INVENTORY_DIR}/*-${region}-*.json | wc -l)
    echo "$region: $count files"
done

# Find largest files
echo -e "\nLargest inventory files:"
echo "-----------------------"
ls -lh ${INVENTORY_DIR}/*.json | sort -k5 -hr | head -5
```

## File Size Considerations

### Typical File Sizes

- **Small services** (e.g., few Lambda functions): 1-10 KB
- **Medium services** (e.g., moderate EC2 usage): 10-100 KB  
- **Large services** (e.g., many resources): 100 KB - 1 MB
- **Very large services** (e.g., thousands of resources): 1-10 MB+

### Storage Requirements

For a typical AWS account:
- **Small account**: 10-50 MB total
- **Medium account**: 50-200 MB total
- **Large account**: 200 MB - 1 GB total
- **Enterprise account**: 1 GB+ total

## Error Handling in Output

### Missing Files

If a service is not available in a region or permissions are insufficient, no file will be created for that service/region combination.

### Empty Files

Services with no resources will create files containing an empty array:

```json
[]
```

### Error Information

Errors are logged to the console but do not appear in the JSON output files. Use the `--verbose` flag to see detailed error information.

## Working with Large Datasets

### Streaming Processing

For very large inventory files, consider streaming processing:

```python
import json

def process_large_inventory(filename):
    """Process large inventory files without loading everything into memory."""
    
    with open(filename, 'r') as f:
        data = json.load(f)
        
    # Process in chunks
    chunk_size = 100
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        # Process chunk
        for item in chunk:
            # Process individual resource
            pass
```

### Database Import

For complex analysis, consider importing the data into a database:

```sql
-- Example PostgreSQL schema for EC2 instances
CREATE TABLE ec2_instances (
    account_id VARCHAR(12),
    region VARCHAR(20),
    instance_id VARCHAR(20) PRIMARY KEY,
    instance_type VARCHAR(20),
    state VARCHAR(20),
    launch_time TIMESTAMP,
    vpc_id VARCHAR(20),
    subnet_id VARCHAR(20),
    private_ip INET,
    public_ip INET,
    tags JSONB,
    raw_data JSONB
);
```

## Best Practices

### File Management

1. **Regular cleanup**: Remove old inventory files to save disk space
2. **Compression**: Compress old inventory files for archival
3. **Versioning**: Keep timestamped directories for historical comparison
4. **Backup**: Backup important inventory snapshots

### Processing Efficiency

1. **Parallel processing**: Process multiple files concurrently
2. **Selective processing**: Only process files for services you need
3. **Caching**: Cache processed results to avoid recomputation
4. **Indexing**: Create indexes for frequently queried data

### Data Quality

1. **Validation**: Validate JSON structure before processing
2. **Completeness**: Check for missing expected files
3. **Consistency**: Verify data consistency across regions
4. **Freshness**: Track when inventory was last updated
