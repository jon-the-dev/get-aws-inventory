# Implementation Guide: Adding New AWS Services

This guide provides step-by-step instructions for implementing the new boto3 services identified in `new_services_analysis.md`.

## Overview

Based on the analysis, we've identified **50+ additional services** and **100+ new methods** that can be added to expand the AWS Inventory Scanner's capabilities. This guide shows you how to implement them systematically.

## Prerequisites

1. **Development environment** set up (see DEVELOPMENT.md)
2. **AWS credentials** configured with appropriate permissions
3. **Test AWS account** for validation (recommended)

## Implementation Phases

We recommend implementing new services in phases to maintain quality and manageability:

### Phase 1: Critical Networking Services (Week 1)
**Impact**: High | **Complexity**: Low-Medium

These services provide the most value for infrastructure visibility:

1. EC2 Enhanced (15 new methods)
2. ELBv2 - Application/Network Load Balancers
3. CloudWatch Logs
4. VPC Lattice

### Phase 2: Security & Compliance (Week 2)
**Impact**: High | **Complexity**: Medium

Essential for security audits and compliance:

1. Security Hub
2. IAM Access Analyzer
3. Inspector v2
4. Macie

### Phase 3: Application Services (Week 3)
**Impact**: Medium | **Complexity**: Low

Common application infrastructure:

1. EventBridge
2. Step Functions
3. Lambda Enhanced
4. ECS/EKS Enhanced

### Phase 4: Data & Analytics (Week 4)
**Impact**: Medium | **Complexity**: Medium

Data platform services:

1. Glue
2. EMR
3. Kinesis (Streams, Firehose, Analytics)
4. MSK (Managed Kafka)

## Step-by-Step Implementation

### Step 1: Choose a Service to Add

Let's start with an example: **Adding ELBv2 (Application Load Balancers)**

### Step 2: Test Service in boto3

Create a test script to verify the service works:

```python
#!/usr/bin/env python3
"""Test script for ELBv2 service."""

import boto3

# Create client
client = boto3.client('elbv2', region_name='us-east-1')

# Test pagination support
print("Testing describe_load_balancers:")
print(f"Can paginate: {client.can_paginate('describe_load_balancers')}")

# Get paginator
if client.can_paginate('describe_load_balancers'):
    paginator = client.get_paginator('describe_load_balancers')
    for page in paginator.paginate():
        print(f"Found {len(page.get('LoadBalancers', []))} load balancers")

print("\nTesting describe_target_groups:")
print(f"Can paginate: {client.can_paginate('describe_target_groups')}")

# Test response structure
response = client.describe_load_balancers()
print(f"\nResponse keys: {response.keys()}")
```

Save as `test_elbv2.py` and run:

```bash
python test_elbv2.py
```

### Step 3: Identify Service Category

Based on the test, determine if the service:

1. **Supports pagination** → Add to `paginated_services`
2. **Requires manual pagination** → Add to `non_paginated_services`
3. **Is global/us-east-1 only** → Add to `paginated_services_east`

ELBv2 supports pagination, so it goes in `paginated_services`.

### Step 4: Add Service to scanner.py

Edit `aws_inventory_scanner/scanner.py`:

```python
self.paginated_services = {
    # ... existing services ...

    # Add ELBv2 (Application/Network Load Balancers)
    "elbv2": [
        ("describe_load_balancers", "LoadBalancers"),
        ("describe_target_groups", "TargetGroups"),
    ],

    # ... rest of services ...
}
```

**Important:** Add services in alphabetical order for maintainability.

### Step 5: Test the New Service

```bash
# Install in development mode
pip install -e .

# Test with single region
aws-inventory-scanner --region us-east-1 --verbose

# Check output
ls -lh inventory/*elbv2*
```

Expected output files:
```
123456789012-elbv2-us-east-1-describe_load_balancers-LoadBalancers.json
123456789012-elbv2-us-east-1-describe_target_groups-TargetGroups.json
```

### Step 6: Verify Output Content

```bash
# Check one of the output files
cat inventory/*elbv2*LoadBalancers.json | jq '.[0]'
```

Verify:
- ✅ JSON is valid
- ✅ Contains expected resource data
- ✅ Tags are present (if applicable)
- ✅ No error messages

### Step 7: Update Documentation

Edit `docs/services.md` to add the new service:

```markdown
### Network & Content Delivery

- **EC2** - Elastic Compute Cloud instances, VPCs, security groups, volumes
- **ELB** - Classic Load Balancers
- **ELBv2** - Application and Network Load Balancers (NEW)
  - Load balancers
  - Target groups
```

### Step 8: Commit Changes

```bash
git add aws_inventory_scanner/scanner.py docs/services.md
git commit -m "Add ELBv2 (Application/Network Load Balancers) support

- Added describe_load_balancers method
- Added describe_target_groups method
- Updated documentation with new service"
```

## Handling Special Cases

### Case 1: Services Requiring Parameters

Some services require parameters that depend on other resources.

**Example: ECS Services (requires cluster ARN)**

**Solution 1: Two-Step Scanning**

```python
# First, add a method to list parent resources
def get_ecs_clusters(self, cred_data, region):
    """Get all ECS cluster names."""
    client = boto3.client(
        "ecs",
        region_name=region,
        aws_access_key_id=cred_data["accessKeyId"],
        aws_secret_access_key=cred_data["secretAccessKey"],
        aws_session_token=cred_data["sessionToken"],
    )

    clusters = []
    paginator = client.get_paginator('list_clusters')
    for page in paginator.paginate():
        clusters.extend(page.get('clusterArns', []))

    return clusters

# Then, scan services for each cluster
def process_ecs_services(self, service, region, aws_acct_id, cred_data):
    """Process ECS services for all clusters."""
    clusters = self.get_ecs_clusters(cred_data, region)

    all_services = []
    for cluster in clusters:
        client = boto3.client(...)
        paginator = client.get_paginator('list_services')

        for page in paginator.paginate(cluster=cluster):
            all_services.extend(page.get('serviceArns', []))

    # Write to file
    file_name = f"{self.output_dir}/{aws_acct_id}-ecs-{region}-list_services-Services.json"
    self.write_to_file(all_services, file_name)
```

**Solution 2: Use Default Parameters**

For services like SSM `get_parameters_by_path`, provide sensible defaults:

```python
# Already implemented in scanner.py:188-214
if svc_name == "ssm" and method_name == "get_parameters_by_path":
    if "Path" not in params:
        params["Path"] = "/"
```

### Case 2: Services with Owner Filters

**Example: EC2 describe_snapshots (requires owner filter)**

```python
self.non_paginated_services = {
    # Add special handling
    "ec2-snapshots": ("describe_snapshots", "Snapshots"),
}

# In handle_non_paginated_service:
if svc_name == "ec2" and method_name == "describe_snapshots":
    params["OwnerIds"] = ["self"]  # Only get your snapshots
```

### Case 3: Global Services

**Example: CloudFront (global, accessed via us-east-1)**

```python
self.paginated_services_east = {
    # ... existing services ...
    "cloudfront": [  # Already present, showing as example
        ("list_distributions", "DistributionList"),
        ("list_cloud_front_origin_access_identities", "CloudFrontOriginAccessIdentityList"),
    ],
}
```

### Case 4: Services with Complex Responses

**Example: Organizations (requires RootId for OUs)**

```python
def get_organizational_units(self, cred_data):
    """Get all organizational units."""
    client = boto3.client(
        "organizations",
        region_name="us-east-1",
        aws_access_key_id=cred_data["accessKeyId"],
        aws_secret_access_key=cred_data["secretAccessKey"],
        aws_session_token=cred_data["sessionToken"],
    )

    # Get root ID first
    roots = client.list_roots()["Roots"]
    root_id = roots[0]["Id"]

    # Get OUs recursively
    all_ous = []
    paginator = client.get_paginator('list_organizational_units_for_parent')

    for page in paginator.paginate(ParentId=root_id):
        all_ous.extend(page.get('OrganizationalUnits', []))

    return all_ous
```

## Batch Implementation Template

Use this template to add multiple services at once:

```python
# In scanner.py, around line 56:

self.paginated_services = {
    # ... existing services ...

    # === PHASE 1: NETWORKING === (Added: 2025-11-19)
    "elbv2": [
        ("describe_load_balancers", "LoadBalancers"),
        ("describe_target_groups", "TargetGroups"),
    ],
    "globalaccelerator": [
        ("list_accelerators", "Accelerators"),
    ],
    "directconnect": [
        ("describe_connections", "connections"),
        ("describe_virtual_interfaces", "virtualInterfaces"),
    ],

    # === PHASE 2: SECURITY === (Added: 2025-11-19)
    "securityhub": [
        ("list_members", "Members"),
        ("describe_standards", "Standards"),
    ],
    "accessanalyzer": [
        ("list_analyzers", "analyzers"),
    ],
    "inspector2": [
        ("list_coverage", "coveredResources"),
    ],
    "macie2": [
        ("list_classification_jobs", "items"),
    ],

    # ... continue with remaining services ...
}
```

## Testing Checklist

For each new service, verify:

- [ ] Service is in correct dictionary (paginated vs non-paginated)
- [ ] Method name is spelled correctly
- [ ] Response key is correct (case-sensitive)
- [ ] Output files are created successfully
- [ ] JSON files contain expected data
- [ ] Tags are extracted if present
- [ ] No errors in verbose mode
- [ ] Works across multiple regions (if regional)
- [ ] Documentation is updated

## Common Issues and Solutions

### Issue 1: AccessDenied Errors

**Symptom:**
```
Error collecting elbv2 resources in us-east-1: AccessDenied
```

**Solution:**
Add required IAM permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "elasticloadbalancing:DescribeLoadBalancers",
    "elasticloadbalancing:DescribeTargetGroups"
  ],
  "Resource": "*"
}
```

### Issue 2: Wrong Response Key

**Symptom:**
Empty JSON files or files with `[]`

**Solution:**
Check the actual response structure:

```python
import boto3
client = boto3.client('service-name', region_name='us-east-1')
response = client.method_name()
print(response.keys())  # Find the correct key
```

### Issue 3: No Paginator Available

**Symptom:**
```
Error: Paginator not found for method_name
```

**Solution:**
Move service to `non_paginated_services`:

```python
self.non_paginated_services = {
    "service-name": ("method_name", "ResponseKey"),
}
```

### Issue 4: Rate Limiting

**Symptom:**
```
Error: Rate exceeded (Throttling)
```

**Solution:**
The scanner already has adaptive retry mode. For persistent issues:

```python
# Increase max_attempts in scanner.py:
self.config = Config(
    connect_timeout=5,
    max_pool_connections=100,
    retries={"max_attempts": 10, "mode": "adaptive"},  # Increased from 5
)
```

Or reduce concurrent workers:

```bash
aws-inventory-scanner --workers 10  # Default is 35
```

## Enhanced EC2 Implementation

EC2 is the most complex service to enhance. Here's the full implementation:

```python
"ec2": [
    # === EXISTING ===
    ("describe_instances", "Reservations"),
    ("describe_security_groups", "SecurityGroups"),
    ("describe_vpcs", "Vpcs"),
    ("describe_volumes", "Volumes"),
    ("describe_subnets", "Subnets"),
    ("describe_network_interfaces", "NetworkInterfaces"),

    # === NETWORKING (NEW) ===
    ("describe_vpc_endpoints", "VpcEndpoints"),
    ("describe_nat_gateways", "NatGateways"),
    ("describe_internet_gateways", "InternetGateways"),
    ("describe_route_tables", "RouteTables"),
    ("describe_vpc_peering_connections", "VpcPeeringConnections"),
    ("describe_network_acls", "NetworkAcls"),

    # === TRANSIT GATEWAY (NEW) ===
    ("describe_transit_gateways", "TransitGateways"),
    ("describe_transit_gateway_attachments", "TransitGatewayAttachments"),

    # === VPN (NEW) ===
    ("describe_vpn_connections", "VpnConnections"),
    ("describe_vpn_gateways", "VpnGateways"),
    ("describe_customer_gateways", "CustomerGateways"),

    # === STORAGE (NEW) ===
    ("describe_snapshots", "Snapshots"),  # Requires OwnerIds filter

    # === IMAGES & KEYS (NEW) ===
    ("describe_key_pairs", "KeyPairs"),
    ("describe_placement_groups", "PlacementGroups"),
],
```

**Special handling for snapshots:**

```python
# In handle_non_paginated_service or process_service_region:
if service == "ec2" and method == "describe_snapshots":
    # Add owner filter to only get account's snapshots
    response = client.describe_snapshots(OwnerIds=["self"])
```

## Validation Script

Create `scripts/validate_services.py`:

```python
#!/usr/bin/env python3
"""Validate that all added services work correctly."""

import boto3
import sys

def validate_service(service, method, expected_key):
    """Validate a single service method."""
    try:
        client = boto3.client(service, region_name='us-east-1')

        # Check pagination support
        can_paginate = client.can_paginate(method)

        # Try to call the method
        if can_paginate:
            paginator = client.get_paginator(method)
            for page in paginator.paginate():
                if expected_key not in page:
                    return False, f"Key '{expected_key}' not in response"
                break
        else:
            response = getattr(client, method)()
            if expected_key not in response:
                return False, f"Key '{expected_key}' not in response"

        return True, "OK"

    except Exception as e:
        return False, str(e)

# Services to validate
services_to_validate = [
    ("elbv2", "describe_load_balancers", "LoadBalancers"),
    ("elbv2", "describe_target_groups", "TargetGroups"),
    ("securityhub", "list_members", "Members"),
    # Add more...
]

print("Validating services...")
failed = []

for service, method, key in services_to_validate:
    success, message = validate_service(service, method, key)
    status = "✓" if success else "✗"
    print(f"{status} {service}.{method} → {key}: {message}")

    if not success:
        failed.append((service, method, message))

if failed:
    print(f"\n❌ {len(failed)} service(s) failed validation")
    sys.exit(1)
else:
    print(f"\n✅ All services validated successfully")
    sys.exit(0)
```

Run validation:

```bash
python scripts/validate_services.py
```

## Performance Considerations

### Reducing Scan Time

When adding many services, scan time increases. Optimize with:

**1. Service Filtering**

Add ability to filter services:

```python
parser.add_argument(
    "--services",
    nargs="+",
    help="List of services to scan (default: all)"
)

# In scan() method:
if args.services:
    services_to_scan = {
        k: v for k, v in self.paginated_services.items()
        if k in args.services
    }
else:
    services_to_scan = self.paginated_services
```

**2. Region Filtering**

Already supported via `--region` argument.

**3. Parallel Execution**

Current default: 35 workers. Can increase for faster scans:

```bash
aws-inventory-scanner --workers 50
```

**4. Skip Existing Files**

Already implemented (scanner.py:232-234).

## Documentation Updates

For each phase of implementation, update:

### 1. docs/services.md

```markdown
## Supported Services

The scanner currently supports **75** AWS services (as of 2025-11-19):

### Compute
- **EC2** - Enhanced with 15+ additional methods for VPCs, Transit Gateways, VPN, etc.
- **Lambda** - Enhanced with layers and event source mappings
- **ECS** - Enhanced with services and task definitions
- **EKS** - Enhanced with node groups and Fargate profiles
...
```

### 2. README.md

Update the services count and add highlights:

```markdown
## Features

- ✅ Scans **75+ AWS services** across all regions
- ✅ **NEW:** Comprehensive tag analysis and compliance reporting
- ✅ **NEW:** Enhanced EC2 networking inventory (VPCs, Transit Gateways, VPN)
```

### 3. CHANGELOG

Add version entry:

```markdown
## [0.2.0] - 2025-11-19

### Added
- Tag analysis and reporting feature
  - Extract tags from all inventory files
  - Generate summary, detailed, and CSV reports
  - Tag compliance checking with required tags
  - Tag inconsistency detection
- 50+ new AWS services and 100+ new API methods
  - Enhanced EC2 with comprehensive networking inventory
  - ELBv2 (Application/Network Load Balancers)
  - Security Hub, IAM Access Analyzer, Inspector v2, Macie
  - EventBridge, Step Functions, Lambda enhancements
  - And many more...

### Changed
- Updated to version 0.2.0 for major feature release
```

## Release Process

After implementing new services:

### 1. Update Version

```bash
# In pyproject.toml line 7:
version = "0.2.0"

# In aws_inventory_scanner/__init__.py line 3:
__version__ = "0.2.0"
```

### 2. Run Pre-commit Hooks

```bash
pre-commit run --all-files
```

### 3. Test End-to-End

```bash
# Full scan
aws-inventory-scanner --region us-east-1 --verbose

# Tag analysis
aws-inventory-scanner --generate-tag-report

# Compliance check
aws-inventory-scanner --generate-tag-report \
  --required-tags Name Environment Owner
```

### 4. Build and Test Package

```bash
python -m build
python -m twine check dist/*
```

### 5. Create Git Tag

```bash
git tag -a v0.2.0 -m "Version 0.2.0: Tag analysis and 50+ new services"
git push origin v0.2.0
```

## Maintenance

### Adding More Services Later

The scanner is designed for easy extension. To add more services:

1. Test with boto3
2. Add to appropriate dictionary in scanner.py
3. Test locally
4. Update documentation
5. Commit with descriptive message

### Deprecation Handling

If AWS deprecates a service:

1. Add comment in scanner.py:
```python
# "old-service": [  # DEPRECATED: AWS retired this service on 2025-XX-XX
#     ("list_method", "Items"),
# ],
```

2. Update docs/services.md
3. Note in CHANGELOG

## Getting Help

If you encounter issues while implementing:

1. Check boto3 documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/
2. Review existing similar services in scanner.py
3. Test with boto3 CLI first: `aws SERVICE-NAME method-name`
4. Check CloudTrail for permission errors
5. Open an issue on GitHub with details

## Summary

Following this guide, you can systematically add all 50+ identified services to the AWS Inventory Scanner. Start with Phase 1 (critical networking services) and progressively add more based on your needs.

**Key Points:**
- ✅ Test each service with boto3 before adding
- ✅ Choose correct service category (paginated vs non-paginated)
- ✅ Verify output files are created correctly
- ✅ Update documentation for each addition
- ✅ Commit with descriptive messages
- ✅ Use phased approach for manageability

Good luck with your implementation!
