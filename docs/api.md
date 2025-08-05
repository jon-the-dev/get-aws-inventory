# API Reference

This page provides detailed documentation for the AWS Inventory Scanner Python API, including class definitions, methods, and configuration options.

## AWSInventoryScanner Class

The main class for performing AWS resource inventory scans.

### Constructor

```python
AWSInventoryScanner(regions=None, output_dir="./inventory", workers=35)
```

Creates a new instance of the AWS Inventory Scanner.

#### Parameters

- **regions** (`list`, optional): List of AWS regions to scan. If `None`, scans all available regions.
- **output_dir** (`str`, optional): Directory to store inventory files. Defaults to `"./inventory"`.
- **workers** (`int`, optional): Number of concurrent workers for parallel processing. Defaults to `35`.

#### Example

```python
from aws_inventory_scanner import AWSInventoryScanner

# Default configuration
scanner = AWSInventoryScanner()

# Custom configuration
scanner = AWSInventoryScanner(
    regions=['us-east-1', 'us-west-2'],
    output_dir='./my-inventory',
    workers=25
)
```

### Methods

#### scan(profile_name=None)

Executes the AWS inventory scan across all configured services and regions.

##### Parameters

- **profile_name** (`str`, optional): AWS profile name to use for authentication. If `None`, uses default credentials.

##### Returns

- `None`: The method saves results to files and doesn't return data directly.

##### Raises

- `botocore.exceptions.BotoCoreError`: For AWS API-related errors
- `Exception`: For general errors during scanning

##### Example

```python
# Scan with default credentials
scanner.scan()

# Scan with specific AWS profile
scanner.scan(profile_name='production')
```

#### get_all_regions(cred_data)

Retrieves all available AWS regions.

##### Parameters

- **cred_data** (`dict`): AWS credentials dictionary containing `accessKeyId`, `secretAccessKey`, and `sessionToken`.

##### Returns

- `list`: List of AWS region names.

##### Example

```python
# This method is typically used internally
regions = scanner.get_all_regions(credentials)
print(regions)  # ['us-east-1', 'us-west-2', 'eu-west-1', ...]
```

## Configuration Options

### Service Definitions

The scanner uses predefined service configurations that specify which AWS services to scan and which API methods to use.

#### Paginated Services (All Regions)

Services that support pagination and are scanned in all regions:

```python
paginated_services = {
    "ec2": [
        ("describe_instances", "Reservations"),
        ("describe_security_groups", "SecurityGroups"),
        ("describe_vpcs", "Vpcs"),
        # ... more methods
    ],
    "s3": [
        ("list_buckets", "Buckets"),
    ],
    # ... more services
}
```

#### Paginated Services (US-East-1 Only)

Global services that are only scanned in the US-East-1 region:

```python
paginated_services_east = {
    "iam": [
        ("list_users", "Users"),
        ("list_roles", "Roles"),
        ("list_groups", "Groups"),
    ],
    "route53domains": [
        ("list_domains", "Domains")
    ],
}
```

#### Non-Paginated Services

Services that don't support pagination:

```python
non_paginated_services = {
    "apigatewayv2": ("get_apis", "Items"),
    "config": ("describe_configuration_recorders", "ConfigurationRecorders"),
    # ... more services
}
```

### AWS Client Configuration

The scanner uses a custom boto3 client configuration for optimal performance:

```python
config = Config(
    connect_timeout=5,           # Connection timeout in seconds
    max_pool_connections=100,    # Maximum connection pool size
    retries={
        "max_attempts": 5,       # Maximum retry attempts
        "mode": "adaptive"       # Adaptive retry mode
    }
)
```

## Advanced Usage

### Custom Service Configuration

You can extend the scanner by modifying the service definitions:

```python
from aws_inventory_scanner import AWSInventoryScanner

class CustomAWSScanner(AWSInventoryScanner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom service
        self.paginated_services["custom-service"] = [
            ("list_custom_resources", "Resources")
        ]
        
        # Modify existing service
        self.paginated_services["ec2"].append(
            ("describe_custom_attribute", "CustomAttributes")
        )
```

### Error Handling

The scanner includes comprehensive error handling:

```python
import logging
from aws_inventory_scanner import AWSInventoryScanner

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

scanner = AWSInventoryScanner()

try:
    scanner.scan(profile_name='my-profile')
except Exception as e:
    print(f"Scan failed: {e}")
    # Handle error appropriately
```

### Concurrent Processing

The scanner uses ThreadPoolExecutor for concurrent processing:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

# The scanner internally uses this pattern:
with ThreadPoolExecutor(max_workers=self.workers) as executor:
    futures = []
    
    # Submit tasks
    for service, methods in self.paginated_services.items():
        for region in regions:
            for method, key in methods:
                future = executor.submit(
                    self.process_service_region,
                    service, method, key, region, account_id, credentials
                )
                futures.append(future)
    
    # Process results
    for future in as_completed(futures):
        result = future.result()
        # Handle result
```

## Internal Methods

### process_service_region(service, method, key, region, aws_acct_id, cred_data)

Processes a single service in a specific region.

#### Parameters

- **service** (`str`): AWS service name
- **method** (`str`): API method to call
- **key** (`str`): Response key containing resources
- **region** (`str`): AWS region
- **aws_acct_id** (`str`): AWS account ID
- **cred_data** (`dict`): AWS credentials

#### Returns

- `tuple`: (service_name, resources_list)

### paginate_and_collect(client, method_name, key)

Handles paginated API calls.

#### Parameters

- **client**: Boto3 client instance
- **method_name** (`str`): API method name
- **key** (`str`): Response key containing resources

#### Returns

- `list`: Collected resources from all pages

### handle_non_paginated_service(client, method_name, key, params=None)

Handles non-paginated API calls with manual pagination.

#### Parameters

- **client**: Boto3 client instance
- **method_name** (`str`): API method name
- **key** (`str`): Response key containing resources
- **params** (`dict`, optional): Additional parameters

#### Returns

- `list`: Collected resources

### write_to_file(data, file_name)

Writes resource data to a JSON file.

#### Parameters

- **data**: Data to write
- **file_name** (`str`): Output file path

## Integration Examples

### Custom Processing Pipeline

```python
import json
import os
from aws_inventory_scanner import AWSInventoryScanner

class InventoryProcessor:
    def __init__(self, scanner_config=None):
        self.scanner = AWSInventoryScanner(**(scanner_config or {}))
        
    def scan_and_process(self, profile_name=None):
        """Scan AWS resources and process results."""
        
        # Run the scan
        self.scanner.scan(profile_name=profile_name)
        
        # Process results
        return self.process_results()
        
    def process_results(self):
        """Process scan results."""
        results = {}
        
        for filename in os.listdir(self.scanner.output_dir):
            if not filename.endswith('.json'):
                continue
                
            filepath = os.path.join(self.scanner.output_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Extract service and region from filename
            parts = filename.replace('.json', '').split('-')
            service = parts[1]
            region = parts[2]
            
            if service not in results:
                results[service] = {}
            if region not in results[service]:
                results[service][region] = []
                
            results[service][region].extend(data)
            
        return results

# Usage
processor = InventoryProcessor({
    'regions': ['us-east-1', 'us-west-2'],
    'workers': 20
})

results = processor.scan_and_process('production')
```

### Database Integration

```python
import json
import sqlite3
from aws_inventory_scanner import AWSInventoryScanner

class DatabaseInventory:
    def __init__(self, db_path='inventory.db'):
        self.db_path = db_path
        self.scanner = AWSInventoryScanner()
        self.init_database()
        
    def init_database(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY,
                account_id TEXT,
                service TEXT,
                region TEXT,
                resource_type TEXT,
                resource_id TEXT,
                data TEXT,
                scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def scan_to_database(self, profile_name=None):
        """Scan AWS resources and store in database."""
        
        # Run scan
        self.scanner.scan(profile_name=profile_name)
        
        # Import to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for filename in os.listdir(self.scanner.output_dir):
            if not filename.endswith('.json'):
                continue
                
            # Parse filename
            parts = filename.replace('.json', '').split('-')
            account_id = parts[0]
            service = parts[1]
            region = parts[2]
            resource_type = parts[4]
            
            # Load data
            filepath = os.path.join(self.scanner.output_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Insert resources
            for resource in data:
                resource_id = self.extract_resource_id(service, resource)
                
                cursor.execute('''
                    INSERT INTO resources 
                    (account_id, service, region, resource_type, resource_id, data)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (account_id, service, region, resource_type, 
                      resource_id, json.dumps(resource)))
        
        conn.commit()
        conn.close()
        
    def extract_resource_id(self, service, resource):
        """Extract resource ID based on service type."""
        id_mappings = {
            'ec2': lambda r: r.get('InstanceId', r.get('VolumeId', r.get('GroupId'))),
            's3': lambda r: r.get('Name'),
            'rds': lambda r: r.get('DBInstanceIdentifier', r.get('DBClusterIdentifier')),
            'lambda': lambda r: r.get('FunctionName'),
        }
        
        extractor = id_mappings.get(service, lambda r: str(hash(str(r)))[:16])
        return extractor(resource)

# Usage
db_inventory = DatabaseInventory()
db_inventory.scan_to_database('production')
```

## Error Handling and Logging

### Custom Logging Configuration

```python
import logging
from aws_inventory_scanner import AWSInventoryScanner

# Configure custom logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('inventory_scan.log'),
        logging.StreamHandler()
    ]
)

scanner = AWSInventoryScanner()
scanner.scan()
```

### Exception Handling

```python
from aws_inventory_scanner import AWSInventoryScanner
import botocore.exceptions

scanner = AWSInventoryScanner()

try:
    scanner.scan(profile_name='production')
except botocore.exceptions.NoCredentialsError:
    print("AWS credentials not found")
except botocore.exceptions.ClientError as e:
    print(f"AWS API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Tuning

### Worker Configuration

```python
import os
from aws_inventory_scanner import AWSInventoryScanner

# Adjust workers based on system resources
cpu_count = os.cpu_count()
optimal_workers = min(cpu_count * 4, 50)  # Cap at 50

scanner = AWSInventoryScanner(workers=optimal_workers)
```

### Memory Management

```python
import gc
from aws_inventory_scanner import AWSInventoryScanner

class MemoryEfficientScanner(AWSInventoryScanner):
    def write_to_file(self, data, file_name):
        """Override to add memory cleanup."""
        super().write_to_file(data, file_name)
        
        # Force garbage collection after large writes
        if len(str(data)) > 1000000:  # 1MB threshold
            gc.collect()
```

This API reference provides comprehensive documentation for integrating and extending the AWS Inventory Scanner in your applications.
