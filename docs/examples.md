# Examples

This page provides practical examples of using the AWS Inventory Scanner for various use cases and scenarios.

## Basic Usage Examples

### Simple Full Account Scan

```bash
# Scan all regions and services with default settings
aws-inventory-scanner
```

This will:
- Scan all AWS regions
- Use default AWS credentials
- Save results to `./inventory/` directory
- Use 35 concurrent workers

### Regional Scan

```bash
# Scan specific regions only
aws-inventory-scanner --region us-east-1 --region us-west-2
```

### Profile-Based Scan

```bash
# Use a specific AWS profile
aws-inventory-scanner --profile production --verbose
```

## Advanced CLI Examples

### Multi-Environment Scanning

```bash
#!/bin/bash
# Script to scan multiple AWS environments

ENVIRONMENTS=("dev" "staging" "production")
REGIONS=("us-east-1" "us-west-2" "eu-west-1")

for env in "${ENVIRONMENTS[@]}"; do
    echo "Scanning $env environment..."
    
    # Create environment-specific output directory
    output_dir="./inventory-${env}-$(date +%Y%m%d)"
    
    # Scan with environment-specific profile
    aws-inventory-scanner \
        --profile "$env" \
        --output-dir "$output_dir" \
        --region us-east-1 \
        --region us-west-2 \
        --workers 25 \
        --verbose
        
    echo "Completed $env scan. Results in: $output_dir"
done
```

### Scheduled Scanning

```bash
#!/bin/bash
# Daily inventory scan script for cron

# Set up environment
export PATH="/usr/local/bin:$PATH"
cd /home/user/aws-inventory

# Create timestamped directory
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="./daily-scans/scan_$TIMESTAMP"

# Run scan
aws-inventory-scanner \
    --profile production \
    --output-dir "$OUTPUT_DIR" \
    --workers 30 \
    --verbose > "scan_$TIMESTAMP.log" 2>&1

# Compress old scans (keep last 7 days)
find ./daily-scans -name "scan_*" -type d -mtime +7 -exec tar -czf {}.tar.gz {} \; -exec rm -rf {} \;

# Send notification
if [ $? -eq 0 ]; then
    echo "AWS inventory scan completed successfully" | mail -s "Inventory Scan Success" admin@company.com
else
    echo "AWS inventory scan failed. Check logs." | mail -s "Inventory Scan Failed" admin@company.com
fi
```

Add to crontab:
```bash
# Run daily at 2 AM
0 2 * * * /path/to/inventory-scan.sh
```

## Python API Examples

### Basic Python Usage

```python
from aws_inventory_scanner import AWSInventoryScanner

# Simple scan
scanner = AWSInventoryScanner()
scanner.scan()

print("Scan completed. Check ./inventory/ directory for results.")
```

### Custom Configuration

```python
from aws_inventory_scanner import AWSInventoryScanner
import os
from datetime import datetime

# Create timestamped output directory
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"./scans/inventory_{timestamp}"

# Configure scanner
scanner = AWSInventoryScanner(
    regions=['us-east-1', 'us-west-2', 'eu-west-1'],
    output_dir=output_dir,
    workers=25
)

# Run scan with specific profile
try:
    scanner.scan(profile_name='production')
    print(f"Scan completed successfully. Results in: {output_dir}")
except Exception as e:
    print(f"Scan failed: {e}")
```

### Multi-Account Scanning

```python
from aws_inventory_scanner import AWSInventoryScanner
import os

def scan_multiple_accounts():
    """Scan multiple AWS accounts using different profiles."""
    
    accounts = {
        'production': ['us-east-1', 'us-west-2'],
        'development': ['us-east-1'],
        'staging': ['us-east-1', 'eu-west-1']
    }
    
    results = {}
    
    for profile, regions in accounts.items():
        print(f"Scanning account: {profile}")
        
        output_dir = f"./inventory-{profile}"
        scanner = AWSInventoryScanner(
            regions=regions,
            output_dir=output_dir,
            workers=20
        )
        
        try:
            scanner.scan(profile_name=profile)
            results[profile] = output_dir
            print(f"✓ {profile} scan completed")
        except Exception as e:
            print(f"✗ {profile} scan failed: {e}")
            results[profile] = None
    
    return results

# Run multi-account scan
scan_results = scan_multiple_accounts()
for account, result_dir in scan_results.items():
    if result_dir:
        print(f"{account}: {result_dir}")
    else:
        print(f"{account}: FAILED")
```

## Data Processing Examples

### Resource Counting and Analysis

```python
import json
import os
from collections import defaultdict, Counter

def analyze_inventory(inventory_dir):
    """Comprehensive analysis of AWS inventory."""
    
    # Initialize counters
    resource_counts = defaultdict(int)
    service_regions = defaultdict(set)
    account_resources = defaultdict(lambda: defaultdict(int))
    
    # Process all inventory files
    for filename in os.listdir(inventory_dir):
        if not filename.endswith('.json'):
            continue
            
        # Parse filename components
        parts = filename.replace('.json', '').split('-')
        if len(parts) < 5:
            continue
            
        account_id = parts[0]
        service = parts[1]
        region = parts[2]
        method = parts[3]
        key = parts[4]
        
        # Load resource data
        filepath = os.path.join(inventory_dir, filename)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                resource_count = len(data)
        except (json.JSONDecodeError, IOError):
            continue
            
        # Update counters
        resource_counts[service] += resource_count
        service_regions[service].add(region)
        account_resources[account_id][service] += resource_count
    
    # Generate report
    print("AWS Inventory Analysis Report")
    print("=" * 50)
    
    print(f"\nTotal Services Scanned: {len(resource_counts)}")
    print(f"Total Regions Covered: {len(set().union(*service_regions.values()))}")
    print(f"Total Accounts: {len(account_resources)}")
    
    print("\nTop 10 Services by Resource Count:")
    print("-" * 40)
    for service, count in Counter(resource_counts).most_common(10):
        regions = len(service_regions[service])
        print(f"{service:20} {count:6} resources ({regions} regions)")
    
    print("\nResources by Account:")
    print("-" * 30)
    for account_id, services in account_resources.items():
        total = sum(services.values())
        print(f"Account {account_id}: {total} total resources")
        for service, count in sorted(services.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {service:15} {count:6}")
    
    return {
        'resource_counts': dict(resource_counts),
        'service_regions': {k: list(v) for k, v in service_regions.items()},
        'account_resources': dict(account_resources)
    }

# Usage
analysis = analyze_inventory('./inventory')
```

### Security Analysis Example

```python
import json
import os

def security_analysis(inventory_dir):
    """Analyze security-related resources."""
    
    security_findings = {
        'public_instances': [],
        'open_security_groups': [],
        'unencrypted_volumes': [],
        'public_s3_buckets': [],
        'unused_security_groups': []
    }
    
    # Analyze EC2 instances
    for filename in os.listdir(inventory_dir):
        if 'ec2' in filename and 'describe_instances' in filename:
            filepath = os.path.join(inventory_dir, filename)
            with open(filepath, 'r') as f:
                reservations = json.load(f)
                
            for reservation in reservations:
                for instance in reservation.get('Instances', []):
                    # Check for public instances
                    if instance.get('PublicIpAddress'):
                        security_findings['public_instances'].append({
                            'instance_id': instance['InstanceId'],
                            'public_ip': instance['PublicIpAddress'],
                            'state': instance['State']['Name']
                        })
    
    # Analyze Security Groups
    for filename in os.listdir(inventory_dir):
        if 'ec2' in filename and 'describe_security_groups' in filename:
            filepath = os.path.join(inventory_dir, filename)
            with open(filepath, 'r') as f:
                security_groups = json.load(f)
                
            for sg in security_groups:
                # Check for overly permissive rules
                for rule in sg.get('IpPermissions', []):
                    for ip_range in rule.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            security_findings['open_security_groups'].append({
                                'group_id': sg['GroupId'],
                                'group_name': sg.get('GroupName', ''),
                                'protocol': rule.get('IpProtocol'),
                                'port_range': f"{rule.get('FromPort', 'All')}-{rule.get('ToPort', 'All')}"
                            })
    
    # Generate security report
    print("Security Analysis Report")
    print("=" * 30)
    
    print(f"\nPublic EC2 Instances: {len(security_findings['public_instances'])}")
    for instance in security_findings['public_instances'][:5]:  # Show first 5
        print(f"  {instance['instance_id']} - {instance['public_ip']} ({instance['state']})")
    
    print(f"\nOpen Security Groups: {len(security_findings['open_security_groups'])}")
    for sg in security_findings['open_security_groups'][:5]:  # Show first 5
        print(f"  {sg['group_id']} - {sg['protocol']}:{sg['port_range']}")
    
    return security_findings

# Usage
findings = security_analysis('./inventory')
```

### Cost Optimization Analysis

```python
import json
import os
from datetime import datetime, timedelta

def cost_optimization_analysis(inventory_dir):
    """Identify potential cost optimization opportunities."""
    
    opportunities = {
        'stopped_instances': [],
        'unattached_volumes': [],
        'old_snapshots': [],
        'unused_elastic_ips': [],
        'oversized_instances': []
    }
    
    # Analyze EC2 instances
    for filename in os.listdir(inventory_dir):
        if 'ec2' in filename and 'describe_instances' in filename:
            filepath = os.path.join(inventory_dir, filename)
            with open(filepath, 'r') as f:
                reservations = json.load(f)
                
            for reservation in reservations:
                for instance in reservation.get('Instances', []):
                    # Find stopped instances
                    if instance['State']['Name'] == 'stopped':
                        launch_time = datetime.fromisoformat(
                            instance['LaunchTime'].replace('Z', '+00:00')
                        )
                        stopped_days = (datetime.now(launch_time.tzinfo) - launch_time).days
                        
                        opportunities['stopped_instances'].append({
                            'instance_id': instance['InstanceId'],
                            'instance_type': instance['InstanceType'],
                            'stopped_days': stopped_days,
                            'launch_time': instance['LaunchTime']
                        })
    
    # Analyze EBS volumes
    for filename in os.listdir(inventory_dir):
        if 'ec2' in filename and 'describe_volumes' in filename:
            filepath = os.path.join(inventory_dir, filename)
            with open(filepath, 'r') as f:
                volumes = json.load(f)
                
            for volume in volumes:
                # Find unattached volumes
                if volume['State'] == 'available':
                    opportunities['unattached_volumes'].append({
                        'volume_id': volume['VolumeId'],
                        'size': volume['Size'],
                        'volume_type': volume['VolumeType'],
                        'create_time': volume['CreateTime']
                    })
    
    # Analyze Elastic IPs
    for filename in os.listdir(inventory_dir):
        if 'ec2' in filename and 'describe_addresses' in filename:
            filepath = os.path.join(inventory_dir, filename)
            with open(filepath, 'r') as f:
                addresses = json.load(f)
                
            for address in addresses:
                # Find unassociated Elastic IPs
                if 'InstanceId' not in address and 'NetworkInterfaceId' not in address:
                    opportunities['unused_elastic_ips'].append({
                        'allocation_id': address.get('AllocationId'),
                        'public_ip': address['PublicIp'],
                        'domain': address.get('Domain', 'classic')
                    })
    
    # Generate cost optimization report
    print("Cost Optimization Report")
    print("=" * 30)
    
    total_savings_potential = 0
    
    print(f"\nStopped Instances: {len(opportunities['stopped_instances'])}")
    for instance in opportunities['stopped_instances'][:5]:
        print(f"  {instance['instance_id']} ({instance['instance_type']}) - stopped {instance['stopped_days']} days")
    
    print(f"\nUnattached EBS Volumes: {len(opportunities['unattached_volumes'])}")
    total_unattached_gb = sum(vol['size'] for vol in opportunities['unattached_volumes'])
    estimated_monthly_cost = total_unattached_gb * 0.10  # Rough estimate
    print(f"  Total size: {total_unattached_gb} GB")
    print(f"  Estimated monthly cost: ${estimated_monthly_cost:.2f}")
    
    print(f"\nUnused Elastic IPs: {len(opportunities['unused_elastic_ips'])}")
    eip_monthly_cost = len(opportunities['unused_elastic_ips']) * 3.65  # $0.005/hour
    print(f"  Estimated monthly cost: ${eip_monthly_cost:.2f}")
    
    return opportunities

# Usage
cost_opportunities = cost_optimization_analysis('./inventory')
```

## Integration Examples

### Slack Notification Integration

```python
import json
import requests
from aws_inventory_scanner import AWSInventoryScanner

def scan_and_notify_slack(webhook_url, profile_name=None):
    """Scan AWS resources and send summary to Slack."""
    
    scanner = AWSInventoryScanner()
    
    try:
        # Run scan
        scanner.scan(profile_name=profile_name)
        
        # Analyze results
        resource_count = 0
        service_count = 0
        
        for filename in os.listdir(scanner.output_dir):
            if filename.endswith('.json'):
                service_count += 1
                filepath = os.path.join(scanner.output_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    resource_count += len(data)
        
        # Send Slack notification
        message = {
            "text": "AWS Inventory Scan Completed",
            "attachments": [
                {
                    "color": "good",
                    "fields": [
                        {
                            "title": "Total Resources",
                            "value": str(resource_count),
                            "short": True
                        },
                        {
                            "title": "Services Scanned",
                            "value": str(service_count),
                            "short": True
                        },
                        {
                            "title": "Profile",
                            "value": profile_name or "default",
                            "short": True
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        
        print("Scan completed and Slack notification sent")
        
    except Exception as e:
        # Send error notification
        error_message = {
            "text": "AWS Inventory Scan Failed",
            "attachments": [
                {
                    "color": "danger",
                    "fields": [
                        {
                            "title": "Error",
                            "value": str(e),
                            "short": False
                        }
                    ]
                }
            ]
        }
        
        requests.post(webhook_url, json=error_message)
        raise

# Usage
webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
scan_and_notify_slack(webhook_url, 'production')
```

### Database Storage Example

```python
import json
import sqlite3
import os
from datetime import datetime
from aws_inventory_scanner import AWSInventoryScanner

class InventoryDatabase:
    def __init__(self, db_path='aws_inventory.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                profile_name TEXT,
                total_resources INTEGER,
                total_services INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER,
                account_id TEXT,
                service TEXT,
                region TEXT,
                resource_type TEXT,
                resource_id TEXT,
                resource_data TEXT,
                FOREIGN KEY (scan_id) REFERENCES scans (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_scan_results(self, inventory_dir, profile_name=None):
        """Store scan results in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create scan record
        cursor.execute(
            'INSERT INTO scans (profile_name, total_resources, total_services) VALUES (?, 0, 0)',
            (profile_name,)
        )
        scan_id = cursor.lastrowid
        
        total_resources = 0
        total_services = 0
        
        # Process inventory files
        for filename in os.listdir(inventory_dir):
            if not filename.endswith('.json'):
                continue
                
            total_services += 1
            
            # Parse filename
            parts = filename.replace('.json', '').split('-')
            account_id = parts[0]
            service = parts[1]
            region = parts[2]
            resource_type = parts[4]
            
            # Load and store resources
            filepath = os.path.join(inventory_dir, filename)
            with open(filepath, 'r') as f:
                resources = json.load(f)
                
            for resource in resources:
                total_resources += 1
                resource_id = self.extract_resource_id(service, resource)
                
                cursor.execute('''
                    INSERT INTO resources 
                    (scan_id, account_id, service, region, resource_type, resource_id, resource_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (scan_id, account_id, service, region, resource_type, 
                      resource_id, json.dumps(resource)))
        
        # Update scan totals
        cursor.execute(
            'UPDATE scans SET total_resources = ?, total_services = ? WHERE id = ?',
            (total_resources, total_services, scan_id)
        )
        
        conn.commit()
        conn.close()
        
        return scan_id
    
    def extract_resource_id(self, service, resource):
        """Extract resource ID based on service type."""
        id_fields = {
            'ec2': ['InstanceId', 'VolumeId', 'GroupId', 'VpcId'],
            's3': ['Name'],
            'rds': ['DBInstanceIdentifier', 'DBClusterIdentifier'],
            'lambda': ['FunctionName'],
            'iam': ['UserName', 'RoleName', 'GroupName']
        }
        
        fields = id_fields.get(service, [])
        for field in fields:
            if field in resource:
                return resource[field]
        
        return f"unknown-{hash(str(resource)) % 10000}"
    
    def get_scan_history(self, limit=10):
        """Get recent scan history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, scan_date, profile_name, total_resources, total_services
            FROM scans
            ORDER BY scan_date DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results

# Usage example
def scan_to_database():
    """Complete example of scanning and storing in database."""
    
    # Initialize database
    db = InventoryDatabase()
    
    # Run scan
    scanner = AWSInventoryScanner(
        regions=['us-east-1', 'us-west-2'],
        output_dir='./temp-inventory'
    )
    
    profile_name = 'production'
    scanner.scan(profile_name=profile_name)
    
    # Store in database
    scan_id = db.store_scan_results('./temp-inventory', profile_name)
    
    print(f"Scan completed and stored with ID: {scan_id}")
    
    # Show recent scans
    print("\nRecent scans:")
    for scan in db.get_scan_history(5):
        print(f"  {scan[1]} - {scan[2]} - {scan[3]} resources, {scan[4]} services")
    
    # Cleanup temporary files
    import shutil
    shutil.rmtree('./temp-inventory')

# Run the example
scan_to_database()
```

## Monitoring and Alerting Examples

### CloudWatch Metrics Integration

```python
import boto3
import json
import os
from aws_inventory_scanner import AWSInventoryScanner
from datetime import datetime

def scan_with_cloudwatch_metrics(profile_name=None):
    """Scan AWS resources and send metrics to CloudWatch."""
    
    # Initialize CloudWatch client
    session = boto3.Session(profile_name=profile_name)
    cloudwatch = session.client('cloudwatch')
    
    # Run scan
    scanner = AWSInventoryScanner()
    start_time = datetime.now()
    
    try:
        scanner.scan(profile_name=profile_name)
        end_time = datetime.now()
        scan_duration = (end_time - start_time).total_seconds()
        
        # Analyze results
        metrics = analyze_scan_results(scanner.output_dir)
        
        # Send metrics to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='AWS/InventoryScanner',
            MetricData=[
                {
                    'MetricName': 'ScanDuration',
                    'Value': scan_duration,
                    'Unit': 'Seconds',
                    'Dimensions': [
                        {
                            'Name': 'Profile',
                            'Value': profile_name or 'default'
                        }
                    ]
                },
                {
                    'MetricName': 'TotalResources',
                    'Value': metrics['total_resources'],
                    'Unit': 'Count',
                    'Dimensions': [
                        {
                            'Name': 'Profile',
                            'Value': profile_name or 'default'
                        }
                    ]
                },
                {
                    'MetricName': 'ServicesScanned',
                    'Value': metrics['services_scanned'],
                    'Unit': 'Count',
                    'Dimensions': [
                        {
                            'Name': 'Profile',
                            'Value': profile_name or 'default'
                        }
                    ]
                }
            ]
        )
        
        print(f"Scan completed in {scan_duration:.2f} seconds")
        print(f"Metrics sent to CloudWatch")
        
    except Exception as e:
        # Send failure metric
        cloudwatch.put_metric_data(
            Namespace='AWS/InventoryScanner',
            MetricData=[
                {
                    'MetricName': 'ScanFailures',
                    'Value': 1,
                    'Unit': 'Count',
                    'Dimensions': [
                        {
                            'Name': 'Profile',
                            'Value': profile_name or 'default'
                        }
                    ]
                }
            ]
        )
        raise

def analyze_scan_results(inventory_dir):
    """Analyze scan results and return metrics."""
    total_resources = 0
    services_scanned = 0
    
    for filename in os.listdir(inventory_dir):
        if filename.endswith('.json'):
            services_scanned += 1
            filepath = os.path.join(inventory_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                total_resources += len(data)
    
    return {
        'total_resources': total_resources,
        'services_scanned': services_scanned
    }

# Usage
scan_with_cloudwatch_metrics('production')
```

These examples demonstrate the flexibility and power of the AWS Inventory Scanner for various use cases, from simple resource discovery to complex integration scenarios.
