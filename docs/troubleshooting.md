# Troubleshooting

This guide helps you resolve common issues when using the AWS Inventory Scanner.

## Common Issues and Solutions

### Installation Issues

#### Issue: `pip install aws-inventory-scanner` fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement aws-inventory-scanner
```

**Solutions:**
1. **Check Python version:**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **Upgrade pip:**
   ```bash
   pip install --upgrade pip
   ```

3. **Install from source:**
   ```bash
   git clone https://github.com/yourusername/aws-inventory-scanner.git
   cd aws-inventory-scanner
   pip install -e .
   ```

#### Issue: Permission denied during installation

**Symptoms:**
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solutions:**
1. **Use virtual environment (recommended):**
   ```bash
   python -m venv aws-scanner-env
   source aws-scanner-env/bin/activate  # Linux/macOS
   # or
   aws-scanner-env\Scripts\activate     # Windows
   pip install aws-inventory-scanner
   ```

2. **Install for user only:**
   ```bash
   pip install --user aws-inventory-scanner
   ```

### Authentication Issues

#### Issue: No AWS credentials found

**Symptoms:**
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**Solutions:**
1. **Configure AWS CLI:**
   ```bash
   aws configure
   ```

2. **Set environment variables:**
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

3. **Use IAM roles (for EC2 instances):**
   - Attach an IAM role with appropriate permissions to your EC2 instance

4. **Verify credentials:**
   ```bash
   aws sts get-caller-identity
   ```

#### Issue: Access denied errors

**Symptoms:**
```
botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the ListBuckets operation
```

**Solutions:**
1. **Check IAM permissions:**
   - Ensure your user/role has the necessary read permissions
   - Consider using the `ReadOnlyAccess` managed policy for testing

2. **Test specific service access:**
   ```bash
   aws ec2 describe-instances --region us-east-1
   aws s3 ls
   ```

3. **Use minimal permissions policy:**
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "ec2:Describe*",
                   "s3:List*",
                   "rds:Describe*",
                   "iam:List*",
                   "sts:GetCallerIdentity"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

### Runtime Issues

#### Issue: Scanner hangs or runs very slowly

**Symptoms:**
- Scanner appears to freeze
- Very slow progress
- High CPU usage

**Solutions:**
1. **Reduce worker count:**
   ```bash
   aws-inventory-scanner --workers 10
   ```

2. **Scan specific regions:**
   ```bash
   aws-inventory-scanner --region us-east-1
   ```

3. **Enable verbose logging to identify bottlenecks:**
   ```bash
   aws-inventory-scanner --verbose
   ```

4. **Check network connectivity:**
   ```bash
   ping ec2.us-east-1.amazonaws.com
   ```

#### Issue: Rate limiting errors

**Symptoms:**
```
botocore.exceptions.ClientError: An error occurred (Throttling) when calling the DescribeInstances operation: Rate exceeded
```

**Solutions:**
1. **Reduce concurrent workers:**
   ```bash
   aws-inventory-scanner --workers 5
   ```

2. **Add delays between requests (modify scanner):**
   ```python
   import time
   from aws_inventory_scanner import AWSInventoryScanner
   
   class SlowScanner(AWSInventoryScanner):
       def process_service_region(self, *args, **kwargs):
           time.sleep(0.1)  # Add 100ms delay
           return super().process_service_region(*args, **kwargs)
   ```

3. **Use exponential backoff (built-in retry logic should handle this)**

#### Issue: Out of memory errors

**Symptoms:**
```
MemoryError: Unable to allocate memory
```

**Solutions:**
1. **Scan fewer regions at once:**
   ```bash
   aws-inventory-scanner --region us-east-1
   ```

2. **Reduce worker count:**
   ```bash
   aws-inventory-scanner --workers 10
   ```

3. **Monitor memory usage:**
   ```bash
   # Linux/macOS
   top -p $(pgrep -f aws-inventory-scanner)
   
   # Or use htop for better visualization
   htop
   ```

### Output Issues

#### Issue: Empty or missing output files

**Symptoms:**
- No files created in output directory
- Files exist but are empty (`[]`)

**Solutions:**
1. **Check permissions on output directory:**
   ```bash
   ls -la ./inventory/
   mkdir -p ./inventory
   chmod 755 ./inventory
   ```

2. **Verify AWS resources exist:**
   ```bash
   aws ec2 describe-instances --region us-east-1
   ```

3. **Check for errors in verbose mode:**
   ```bash
   aws-inventory-scanner --verbose
   ```

4. **Verify account has resources:**
   - Empty files are normal if no resources exist for that service/region

#### Issue: JSON parsing errors when processing output

**Symptoms:**
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solutions:**
1. **Check file integrity:**
   ```bash
   # Verify JSON files are valid
   find inventory -name "*.json" -exec python -m json.tool {} \; > /dev/null
   ```

2. **Look for truncated files:**
   ```bash
   # Find files that don't end with ']'
   find inventory -name "*.json" -exec sh -c 'tail -c 1 "$1" | grep -v "]"' _ {} \;
   ```

3. **Re-run scan for corrupted files:**
   ```bash
   # Remove corrupted files and re-scan
   rm inventory/corrupted-file.json
   aws-inventory-scanner
   ```

### Network Issues

#### Issue: Connection timeouts

**Symptoms:**
```
botocore.exceptions.ConnectTimeoutError: Connect timeout on endpoint URL
```

**Solutions:**
1. **Check internet connectivity:**
   ```bash
   ping aws.amazon.com
   curl -I https://ec2.us-east-1.amazonaws.com
   ```

2. **Configure proxy if needed:**
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ```

3. **Increase timeout values:**
   ```python
   from botocore.client import Config
   from aws_inventory_scanner import AWSInventoryScanner
   
   class TimeoutScanner(AWSInventoryScanner):
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.config = Config(
               connect_timeout=30,  # Increase from default 5
               read_timeout=30,
               retries={'max_attempts': 10}
           )
   ```

#### Issue: SSL certificate errors

**Symptoms:**
```
botocore.exceptions.SSLError: SSL validation failed
```

**Solutions:**
1. **Update certificates:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update && sudo apt-get install ca-certificates
   
   # CentOS/RHEL
   sudo yum update ca-certificates
   
   # macOS
   brew install ca-certificates
   ```

2. **Disable SSL verification (not recommended for production):**
   ```bash
   export AWS_CA_BUNDLE=""
   ```

### Performance Issues

#### Issue: Scan takes too long

**Symptoms:**
- Scan runs for hours without completing
- Progress appears very slow

**Solutions:**
1. **Optimize worker count:**
   ```bash
   # Start with CPU count * 2
   aws-inventory-scanner --workers $(nproc --all)
   ```

2. **Profile the scan:**
   ```python
   import cProfile
   from aws_inventory_scanner import AWSInventoryScanner
   
   def profile_scan():
       scanner = AWSInventoryScanner()
       scanner.scan()
   
   cProfile.run('profile_scan()', 'scan_profile.prof')
   ```

3. **Scan incrementally:**
   ```bash
   # Scan one region at a time
   for region in us-east-1 us-west-2 eu-west-1; do
       aws-inventory-scanner --region $region --output-dir inventory-$region
   done
   ```

4. **Use SSD storage:**
   - Ensure output directory is on fast storage (SSD)

### Service-Specific Issues

#### Issue: IAM resources not found

**Symptoms:**
- No IAM users, roles, or groups in output
- IAM files are empty

**Solutions:**
1. **IAM is global - only scanned in us-east-1:**
   ```bash
   aws-inventory-scanner --region us-east-1
   ```

2. **Check IAM permissions:**
   ```bash
   aws iam list-users
   aws iam list-roles
   ```

#### Issue: S3 buckets missing from some regions

**Symptoms:**
- S3 buckets only appear in one region file

**Solutions:**
1. **S3 is global but listed in us-east-1:**
   - This is expected behavior
   - All buckets appear in the us-east-1 S3 file regardless of their actual region

2. **Verify bucket access:**
   ```bash
   aws s3 ls
   ```

#### Issue: Some services return no data

**Symptoms:**
- Certain services consistently return empty results
- Services work with AWS CLI but not with scanner

**Solutions:**
1. **Check service availability in region:**
   ```bash
   aws ec2 describe-regions --query 'Regions[?RegionName==`us-east-1`]'
   ```

2. **Verify service is supported:**
   - Check the [Supported Services](services.md) documentation
   - Some services may not be available in all regions

3. **Test service manually:**
   ```bash
   aws lambda list-functions --region us-east-1
   ```

## Debugging Techniques

### Enable Debug Logging

```bash
# Maximum verbosity
aws-inventory-scanner --verbose

# Python logging
export PYTHONPATH=/path/to/aws-inventory-scanner
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from aws_inventory_scanner import AWSInventoryScanner
scanner = AWSInventoryScanner()
scanner.scan()
"
```

### Monitor Resource Usage

```bash
# Monitor during scan
watch -n 1 'ps aux | grep aws-inventory-scanner'

# Monitor disk usage
watch -n 5 'du -sh ./inventory'

# Monitor network usage
sudo nethogs  # Linux
nettop        # macOS
```

### Test Individual Services

```python
import boto3
from botocore.client import Config

# Test specific service/region combination
config = Config(retries={'max_attempts': 5, 'mode': 'adaptive'})
client = boto3.client('ec2', region_name='us-east-1', config=config)

try:
    response = client.describe_instances()
    print(f"Found {len(response['Reservations'])} reservations")
except Exception as e:
    print(f"Error: {e}")
```

### Validate Output Files

```bash
#!/bin/bash
# Validate all JSON files

echo "Validating JSON files..."
invalid_files=0

for file in inventory/*.json; do
    if ! python -m json.tool "$file" > /dev/null 2>&1; then
        echo "Invalid JSON: $file"
        invalid_files=$((invalid_files + 1))
    fi
done

if [ $invalid_files -eq 0 ]; then
    echo "All JSON files are valid"
else
    echo "Found $invalid_files invalid JSON files"
fi
```

## Getting Help

### Log Collection

When reporting issues, collect the following information:

```bash
# System information
uname -a
python --version
pip show aws-inventory-scanner

# AWS configuration
aws configure list
aws sts get-caller-identity

# Run with verbose logging
aws-inventory-scanner --verbose > scan.log 2>&1

# Check output
ls -la inventory/
head -n 20 inventory/*.json
```

### Common Log Messages

#### Normal Messages
```
INFO - Starting AWS inventory scan for account 123456789012
INFO - Scanning regions: ['us-east-1', 'us-west-2']
INFO - Collected 5 ec2 resources in us-east-1 using describe_instances/Reservations
```

#### Warning Messages
```
DEBUG - Error collecting describe_instances/Reservations: An error occurred (UnauthorizedOperation)
DEBUG - 123456789012-lambda-us-west-2-list_functions-Functions.json already exists. Skipping.
```

#### Error Messages
```
ERROR - Error writing to file: [Errno 28] No space left on device
ERROR - Scan failed: An error occurred (AccessDenied) when calling the GetSessionToken operation
```

### Support Resources

1. **Check the documentation:**
   - [Installation Guide](installation.md)
   - [Usage Guide](usage.md)
   - [API Reference](api.md)

2. **Search existing issues:**
   - GitHub Issues (if available)
   - Stack Overflow with tag `aws-inventory-scanner`

3. **Create a minimal reproduction case:**
   ```bash
   aws-inventory-scanner --region us-east-1 --workers 1 --verbose
   ```

4. **Provide system information:**
   - Operating system and version
   - Python version
   - AWS CLI version
   - Scanner version

Remember to remove sensitive information (account IDs, resource names, etc.) from logs before sharing them.
