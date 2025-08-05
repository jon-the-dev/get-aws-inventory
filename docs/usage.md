# Usage Guide

## Command Line Interface

The AWS Inventory Scanner provides a comprehensive command-line interface for scanning AWS resources.

### Basic Usage

```bash
# Scan all regions with default settings
aws-inventory-scanner
```

This will:
- Scan all AWS regions
- Use default AWS credentials
- Save results to `./inventory/` directory
- Use 35 concurrent workers

### Command Line Options

#### Region Selection

```bash
# Scan specific regions
aws-inventory-scanner --region us-east-1 --region us-west-2

# Scan a single region
aws-inventory-scanner --region eu-west-1
```

#### AWS Profile

```bash
# Use a specific AWS profile
aws-inventory-scanner --profile my-aws-profile

# Use a profile with specific regions
aws-inventory-scanner --profile production --region us-east-1 --region us-west-2
```

#### Output Directory

```bash
# Specify custom output directory
aws-inventory-scanner --output-dir /path/to/my/inventory

# Use relative path
aws-inventory-scanner --output-dir ./my-scan-results
```

#### Concurrency Control

```bash
# Adjust number of concurrent workers (default: 35)
aws-inventory-scanner --workers 50

# Use fewer workers for rate limiting
aws-inventory-scanner --workers 10
```

#### Verbose Logging

```bash
# Enable verbose logging for debugging
aws-inventory-scanner --verbose

# Combine with other options
aws-inventory-scanner --verbose --region us-east-1 --workers 20
```

### Complete Example

```bash
# Comprehensive scan with custom settings
aws-inventory-scanner \
  --profile production \
  --region us-east-1 \
  --region us-west-2 \
  --region eu-west-1 \
  --output-dir ./production-inventory \
  --workers 25 \
  --verbose
```

## Python API

The scanner can also be used programmatically through its Python API.

### Basic Usage

```python
from aws_inventory_scanner import AWSInventoryScanner

# Create scanner with default settings
scanner = AWSInventoryScanner()

# Run the scan
scanner.scan()
```

### Advanced Configuration

```python
from aws_inventory_scanner import AWSInventoryScanner

# Create scanner with custom settings
scanner = AWSInventoryScanner(
    regions=['us-east-1', 'us-west-2', 'eu-west-1'],
    output_dir='./my-inventory',
    workers=25
)

# Run scan with specific AWS profile
scanner.scan(profile_name='my-aws-profile')
```

### Integration Example

```python
import os
from aws_inventory_scanner import AWSInventoryScanner

def scan_aws_resources():
    """Scan AWS resources and return results directory."""
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"./scans/scan_{timestamp}"
    
    # Configure scanner
    scanner = AWSInventoryScanner(
        regions=['us-east-1', 'us-west-2'],
        output_dir=output_dir,
        workers=30
    )
    
    try:
        # Run the scan
        scanner.scan(profile_name='production')
        print(f"Scan completed successfully. Results in: {output_dir}")
        return output_dir
    except Exception as e:
        print(f"Scan failed: {e}")
        return None

# Use the function
results_dir = scan_aws_resources()
if results_dir:
    # Process results
    for filename in os.listdir(results_dir):
        if filename.endswith('.json'):
            print(f"Found resource file: {filename}")
```

## Scanning Strategies

### Full Account Scan

For a comprehensive inventory of your entire AWS account:

```bash
aws-inventory-scanner --verbose
```

This scans all regions and all supported services.

### Regional Focus

For scanning specific regions (useful for regional deployments):

```bash
aws-inventory-scanner \
  --region us-east-1 \
  --region us-west-2 \
  --verbose
```

### Development vs Production

Use different profiles for different environments:

```bash
# Development environment
aws-inventory-scanner --profile dev --region us-west-2

# Production environment
aws-inventory-scanner --profile prod --workers 50
```

### Rate Limiting

If you encounter rate limiting issues:

```bash
# Reduce concurrent workers
aws-inventory-scanner --workers 10

# Focus on specific regions
aws-inventory-scanner --region us-east-1 --workers 15
```

## Output Management

### Directory Structure

The scanner creates a structured output directory:

```
./inventory/
├── 123456789012-ec2-us-east-1-describe_instances-Reservations.json
├── 123456789012-s3-us-east-1-list_buckets-Buckets.json
├── 123456789012-rds-us-west-2-describe_db_instances-DBInstances.json
└── ...
```

### File Naming Convention

Files are named using the pattern:
`{account_id}-{service}-{region}-{method}-{key}.json`

Where:
- `account_id`: Your AWS account ID
- `service`: AWS service name (e.g., ec2, s3, rds)
- `region`: AWS region (e.g., us-east-1, eu-west-1)
- `method`: API method used (e.g., describe_instances, list_buckets)
- `key`: Response key containing the resources

### Processing Results

You can process the JSON files using standard tools:

```bash
# Count total files
ls inventory/*.json | wc -l

# Find all EC2 instances
find inventory -name "*-ec2-*-describe_instances-*.json"

# Search for specific resources
grep -l "my-resource-name" inventory/*.json
```

## Best Practices

### Performance Optimization

1. **Use appropriate worker count**: Start with default (35) and adjust based on your needs
2. **Scan specific regions**: If you only use certain regions, specify them explicitly
3. **Use SSD storage**: Store results on fast storage for better I/O performance

### Security Considerations

1. **Use least privilege**: Only grant necessary read permissions
2. **Secure credentials**: Use IAM roles when possible, avoid hardcoded credentials
3. **Protect output**: Ensure inventory files are stored securely

### Operational Tips

1. **Regular scans**: Schedule regular scans to maintain up-to-date inventory
2. **Version control**: Consider versioning your inventory results
3. **Monitoring**: Monitor scan duration and success rates
4. **Cleanup**: Regularly clean up old inventory files

## Error Handling

The scanner includes robust error handling:

- **Network issues**: Automatic retries with exponential backoff
- **Permission errors**: Graceful handling of insufficient permissions
- **Rate limiting**: Built-in retry logic for API throttling
- **Service unavailability**: Continues scanning other services if one fails

### Common Error Scenarios

1. **Insufficient permissions**: Check your IAM policies
2. **Network connectivity**: Verify internet connection and AWS endpoint access
3. **Rate limiting**: Reduce worker count or add delays
4. **Disk space**: Ensure sufficient storage for results

See the [Troubleshooting](troubleshooting.md) guide for detailed error resolution.
