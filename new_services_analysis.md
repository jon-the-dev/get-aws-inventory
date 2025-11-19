# New boto3 Services Analysis for AWS Inventory Scanner

## Executive Summary

Based on analysis of the current scanner (25+ services, ~80 methods), there are **50+ additional high-value services** and **100+ new methods** that can be added to expand inventory capabilities.

## Currently Supported Services (25)
- ACM, Athena, Auto Scaling, Backup, CloudFormation, CloudFront, CloudTrail, CloudWatch, CodeBuild, CodeDeploy
- Config, DynamoDB, EC2, ECR, ECS, EFS, EKS, ElastiCache, Elastic Beanstalk, ELB
- Elasticsearch, FSx, Glacier, GuardDuty, IAM, KMS, Lambda, Network Firewall
- RDS, Redshift, Route53, Route53 Domains, S3, SageMaker, Secrets Manager
- SNS, SQS, SSM, WAF, WorkSpaces

## High-Priority New Services to Add

### 1. Compute & Containers (7 services)
**AWS Batch** - Batch computing jobs
```python
"batch": [
    ("describe_job_queues", "jobQueues"),
    ("describe_compute_environments", "computeEnvironments"),
    ("list_jobs", "jobSummaryList"),  # requires jobQueue parameter
]
```

**App Runner** - Container web applications
```python
"apprunner": [
    ("list_services", "ServiceSummaryList"),
    ("list_connections", "ConnectionSummaryList"),
]
```

**Lightsail** - VPS instances
```python
"lightsail": [
    ("get_instances", "instances"),
    ("get_load_balancers", "loadBalancers"),
    ("get_databases", "databases"),
]
```

**ECS (Enhanced)** - Currently only lists clusters
```python
"ecs": [
    ("list_clusters", "clusterArns"),  # EXISTING
    ("list_services", "serviceArns"),  # NEW - requires cluster parameter
    ("list_task_definitions", "taskDefinitionArns"),  # NEW
    ("list_container_instances", "containerInstanceArns"),  # NEW - requires cluster
]
```

**EKS (Enhanced)** - Currently only lists clusters
```python
"eks": [
    ("list_clusters", "clusters"),  # EXISTING
    ("list_nodegroups", "nodegroups"),  # NEW - requires cluster parameter
    ("list_fargate_profiles", "fargateProfileNames"),  # NEW - requires cluster
    ("list_addons", "addons"),  # NEW - requires cluster
]
```

**Lambda (Enhanced)** - Add layers and event sources
```python
"lambda": [
    ("list_functions", "Functions"),  # EXISTING
    ("list_layers", "Layers"),  # NEW
    ("list_event_source_mappings", "EventSourceMappings"),  # NEW
]
```

### 2. Networking (10 services/enhancements)
**EC2 (Enhanced)** - Many networking resources missing
```python
"ec2": [
    # EXISTING
    ("describe_instances", "Reservations"),
    ("describe_security_groups", "SecurityGroups"),
    ("describe_vpcs", "Vpcs"),
    ("describe_volumes", "Volumes"),
    ("describe_subnets", "Subnets"),
    ("describe_network_interfaces", "NetworkInterfaces"),
    # NEW - Critical networking components
    ("describe_vpc_endpoints", "VpcEndpoints"),
    ("describe_nat_gateways", "NatGateways"),
    ("describe_internet_gateways", "InternetGateways"),
    ("describe_route_tables", "RouteTables"),
    ("describe_vpc_peering_connections", "VpcPeeringConnections"),
    ("describe_transit_gateways", "TransitGateways"),
    ("describe_transit_gateway_attachments", "TransitGatewayAttachments"),
    ("describe_vpn_connections", "VpnConnections"),
    ("describe_vpn_gateways", "VpnGateways"),
    ("describe_customer_gateways", "CustomerGateways"),
    ("describe_network_acls", "NetworkAcls"),
    ("describe_snapshots", "Snapshots"),  # EBS snapshots
    ("describe_images", "Images"),  # AMIs owned by account
    ("describe_key_pairs", "KeyPairs"),
    ("describe_placement_groups", "PlacementGroups"),
]
```

**ELB v2 (Application/Network Load Balancers)** - Currently only has Classic ELB
```python
"elbv2": [
    ("describe_load_balancers", "LoadBalancers"),
    ("describe_target_groups", "TargetGroups"),
    ("describe_listeners", "Listeners"),  # requires LoadBalancerArn
]
```

**Global Accelerator** - Edge networking
```python
"globalaccelerator": [
    ("list_accelerators", "Accelerators"),
    ("list_listeners", "Listeners"),  # requires AcceleratorArn
]
```

**Direct Connect** - Dedicated network connections
```python
"directconnect": [
    ("describe_connections", "connections"),
    ("describe_virtual_gateways", "virtualGateways"),
    ("describe_virtual_interfaces", "virtualInterfaces"),
]
```

**VPC Lattice** - New service-to-service networking
```python
"vpc-lattice": [
    ("list_services", "items"),
    ("list_service_networks", "items"),
    ("list_target_groups", "items"),
]
```

### 3. Security & Identity (8 services)
**Security Hub** - Security findings aggregation
```python
"securityhub": [
    ("list_members", "Members"),
    ("describe_standards", "Standards"),
    ("get_findings", "Findings"),  # May need pagination handling
]
```

**IAM Access Analyzer** - IAM policy analysis
```python
"accessanalyzer": [
    ("list_analyzers", "analyzers"),
    ("list_findings", "findings"),  # requires analyzerArn
]
```

**Inspector v2** - Vulnerability management
```python
"inspector2": [
    ("list_findings", "findings"),
    ("list_coverage", "coveredResources"),
]
```

**Macie** - Data security and privacy
```python
"macie2": [
    ("list_classification_jobs", "items"),
    ("list_findings", "findingIds"),
    ("get_buckets", "buckets"),
]
```

**RAM (Resource Access Manager)** - Resource sharing
```python
"ram": [
    ("get_resource_shares", "resourceShares"),
    ("list_resources", "resources"),
]
```

**Cognito** - User authentication
```python
"cognito-idp": [
    ("list_user_pools", "UserPools"),
    ("list_identity_providers", "Providers"),  # requires UserPoolId
]
"cognito-identity": [
    ("list_identity_pools", "IdentityPools"),
]
```

**Certificate Manager Private CA** - Private certificates
```python
"acm-pca": [
    ("list_certificate_authorities", "CertificateAuthorities"),
]
```

### 4. Databases (6 services/enhancements)
**DynamoDB (Enhanced)** - Add streams, global tables
```python
"dynamodb": [
    ("list_tables", "TableNames"),  # EXISTING
    ("list_backups", "BackupSummaries"),  # EXISTING
    ("list_global_tables", "GlobalTables"),  # NEW
]
```

**DocumentDB** - MongoDB-compatible database
```python
"docdb": [
    ("describe_db_clusters", "DBClusters"),
    ("describe_db_instances", "DBInstances"),
]
```

**Neptune** - Graph database
```python
"neptune": [
    ("describe_db_clusters", "DBClusters"),
    ("describe_db_instances", "DBInstances"),
]
```

**Timestream** - Time-series database
```python
"timestream-write": [
    ("list_databases", "Databases"),
    ("list_tables", "Tables"),  # requires DatabaseName
]
```

**RDS (Enhanced)** - Add proxies and parameter groups
```python
"rds": [
    # EXISTING
    ("describe_db_instances", "DBInstances"),
    ("describe_db_snapshots", "DBSnapshots"),
    ("describe_db_subnet_groups", "DBSubnetGroups"),
    ("describe_db_clusters", "DBClusters"),
    # NEW
    ("describe_db_proxies", "DBProxies"),
    ("describe_db_parameter_groups", "DBParameterGroups"),
    ("describe_event_subscriptions", "EventSubscriptionsList"),
]
```

**ElastiCache (Enhanced)** - Add replication groups
```python
"elasticache": [
    ("describe_cache_clusters", "CacheClusters"),  # EXISTING
    ("describe_replication_groups", "ReplicationGroups"),  # NEW
    ("describe_cache_parameter_groups", "CacheParameterGroups"),  # NEW
]
```

### 5. Analytics & Data (7 services)
**EMR** - Big data processing
```python
"emr": [
    ("list_clusters", "Clusters"),
    ("list_studios", "Studios"),
]
```

**Kinesis Data Streams**
```python
"kinesis": [
    ("list_streams", "StreamNames"),
    ("list_stream_consumers", "Consumers"),  # requires StreamARN
]
```

**Kinesis Firehose**
```python
"firehose": [
    ("list_delivery_streams", "DeliveryStreamNames"),
]
```

**Kinesis Analytics**
```python
"kinesisanalyticsv2": [
    ("list_applications", "ApplicationSummaries"),
]
```

**MSK (Managed Kafka)**
```python
"kafka": [
    ("list_clusters", "ClusterInfoList"),
    ("list_configurations", "Configurations"),
]
```

**Glue** - ETL and data catalog
```python
"glue": [
    ("get_databases", "DatabaseList"),
    ("get_tables", "TableList"),  # requires DatabaseName
    ("get_crawlers", "Crawlers"),
    ("list_jobs", "JobNames"),
]
```

**Data Pipeline**
```python
"datapipeline": [
    ("list_pipelines", "pipelineIdList"),
]
```

### 6. Application Integration (6 services)
**EventBridge** - Event bus
```python
"events": [
    ("list_event_buses", "EventBuses"),
    ("list_rules", "Rules"),
    ("list_connections", "Connections"),
]
```

**Step Functions** - Workflow orchestration
```python
"stepfunctions": [
    ("list_state_machines", "stateMachines"),
    ("list_activities", "activities"),
]
```

**AppSync** - GraphQL APIs
```python
"appsync": [
    ("list_graphql_apis", "graphqlApis"),
]
```

**MQ** - Managed message brokers
```python
"mq": [
    ("list_brokers", "BrokerSummaries"),
]
```

**SES** - Email service
```python
"sesv2": [
    ("list_email_identities", "EmailIdentities"),
    ("list_configuration_sets", "ConfigurationSets"),
]
```

**API Gateway (Enhanced)** - REST APIs (v2 already has HTTP APIs)
```python
"apigateway": [
    ("get_rest_apis", "items"),
    ("get_domain_names", "items"),
]
```

### 7. Management & Governance (6 services)
**CloudWatch Logs**
```python
"logs": [
    ("describe_log_groups", "logGroups"),
    ("describe_metric_filters", "metricFilters"),
]
```

**Organizations** - Multi-account management
```python
"organizations": [
    ("list_accounts", "Accounts"),
    ("list_organizational_units_for_parent", "OrganizationalUnits"),  # requires ParentId
    ("list_policies", "Policies"),  # requires Filter
]
```

**Service Catalog**
```python
"servicecatalog": [
    ("list_portfolios", "PortfolioDetails"),
    ("search_products", "ProductViewSummaries"),
]
```

**Systems Manager (Enhanced)**
```python
"ssm": [
    ("get_parameters_by_path", "Parameters"),  # EXISTING
    ("describe_instance_information", "InstanceInformationList"),  # NEW
    ("list_documents", "DocumentIdentifiers"),  # NEW
    ("describe_maintenance_windows", "WindowIdentities"),  # NEW
    ("list_associations", "Associations"),  # NEW
]
```

**Resource Groups**
```python
"resource-groups": [
    ("list_groups", "GroupIdentifiers"),
]
```

**Application Auto Scaling** - Auto scaling for non-EC2 resources
```python
"application-autoscaling": [
    ("describe_scalable_targets", "ScalableTargets"),
    ("describe_scaling_policies", "ScalingPolicies"),
]
```

### 8. Developer Tools (5 services)
**CodePipeline**
```python
"codepipeline": [
    ("list_pipelines", "pipelines"),
    ("list_webhooks", "webhooks"),
]
```

**CodeCommit**
```python
"codecommit": [
    ("list_repositories", "repositories"),
]
```

**CodeArtifact** - Artifact repository
```python
"codeartifact": [
    ("list_repositories", "repositories"),
    ("list_domains", "domains"),
]
```

**Cloud9** - IDE environments
```python
"cloud9": [
    ("list_environments", "environmentIds"),
]
```

**X-Ray** - Distributed tracing
```python
"xray": [
    ("get_groups", "Groups"),
    ("get_sampling_rules", "SamplingRuleRecords"),
]
```

### 9. Storage (3 services/enhancements)
**S3 (Enhanced)** - Add access points and batch operations
```python
"s3": [
    ("list_buckets", "Buckets"),  # EXISTING
]
"s3control": [
    ("list_access_points", "AccessPointList"),
    ("list_jobs", "Jobs"),  # S3 Batch Operations
]
```

**Storage Gateway**
```python
"storagegateway": [
    ("list_gateways", "Gateways"),
    ("list_volumes", "VolumeInfos"),
]
```

**Backup (Enhanced)** - Add protected resources
```python
"backup": [
    # EXISTING
    ("list_backup_plans", "BackupPlansList"),
    ("list_backup_vaults", "BackupVaultList"),
    ("list_backup_jobs", "BackupJobs"),
    # NEW
    ("list_protected_resources", "Results"),
    ("list_recovery_points_by_backup_vault", "RecoveryPoints"),  # requires BackupVaultName
]
```

### 10. Other Important Services (5 services)
**CloudWatch (Enhanced)** - Add dashboards and composite alarms
```python
"cloudwatch": [
    ("describe_alarms", "MetricAlarms"),  # EXISTING
    ("list_dashboards", "DashboardEntries"),  # NEW
    ("describe_alarms_for_metric", "MetricAlarms"),  # NEW - requires dimensions
]
```

**Transfer Family** - SFTP/FTPS file transfers
```python
"transfer": [
    ("list_servers", "Servers"),
    ("list_users", "Users"),  # requires ServerId
]
```

**App Mesh** - Service mesh
```python
"appmesh": [
    ("list_meshes", "meshes"),
    ("list_virtual_services", "virtualServices"),  # requires meshName
]
```

**GameLift** - Game server hosting
```python
"gamelift": [
    ("list_fleets", "FleetIds"),
    ("describe_fleet_attributes", "FleetAttributes"),
]
```

**IoT Core**
```python
"iot": [
    ("list_things", "things"),
    ("list_policies", "policies"),
    ("list_certificates", "certificates"),
]
```

## Tag Report Feature Requirements

### Key Observations
Most AWS resources support tags in these formats:
1. **Tags array**: `[{"Key": "Name", "Value": "MyResource"}]`
2. **Tags dict**: `{"Name": "MyResource"}`
3. **TagList**: Similar to Tags array

### Proposed Tag Report Features

#### 1. Tag Extraction Module
Create a new file: `aws_inventory_scanner/tag_analyzer.py`

**Functions:**
- `extract_tags_from_file(file_path)` - Extract tags from a single JSON file
- `extract_tags_from_directory(directory)` - Extract tags from all inventory files
- `generate_tag_report(tags_data)` - Create comprehensive tag report
- `find_untagged_resources(directory)` - List resources without tags
- `find_tag_inconsistencies(directory)` - Find tag key variations (e.g., "Environment" vs "environment")

#### 2. Tag Report Output Formats

**Summary Report** (`tags-summary.json`):
```json
{
  "scan_date": "2025-11-19T10:30:00Z",
  "total_resources_scanned": 1547,
  "resources_with_tags": 1203,
  "resources_without_tags": 344,
  "unique_tag_keys": 47,
  "tag_key_frequency": {
    "Name": 1203,
    "Environment": 987,
    "Owner": 856,
    "CostCenter": 654
  },
  "tag_value_frequency": {
    "Environment": {
      "production": 456,
      "staging": 312,
      "development": 219
    }
  }
}
```

**Detailed Report** (`tags-detailed.json`):
```json
{
  "tag_keys": {
    "Environment": {
      "count": 987,
      "values": ["production", "staging", "development"],
      "resources": [
        {
          "service": "ec2",
          "region": "us-east-1",
          "resource_id": "i-1234567890abcdef0",
          "value": "production"
        }
      ]
    }
  },
  "untagged_resources": [
    {
      "service": "s3",
      "region": "us-east-1",
      "resource_id": "my-bucket-name",
      "file": "123456789012-s3-us-east-1-list_buckets-Buckets.json"
    }
  ],
  "tag_inconsistencies": [
    {
      "similar_keys": ["Environment", "environment", "env"],
      "recommendation": "Standardize to 'Environment'",
      "affected_resources": 47
    }
  ]
}
```

**CSV Report** (`tags-report.csv`):
```csv
Service,Region,ResourceID,TagKey,TagValue,ResourceType
ec2,us-east-1,i-1234567890abcdef0,Name,WebServer1,Instance
ec2,us-east-1,i-1234567890abcdef0,Environment,production,Instance
s3,us-east-1,my-bucket,CostCenter,Engineering,Bucket
```

#### 3. CLI Integration
Add to scanner.py:
```python
parser.add_argument(
    "--generate-tag-report",
    action="store_true",
    help="Generate tag report from existing inventory files"
)
parser.add_argument(
    "--tag-report-format",
    choices=["json", "csv", "both"],
    default="both",
    help="Tag report output format"
)
```

#### 4. Tag Analysis Features
- **Tag Coverage**: Percentage of resources with required tags
- **Tag Compliance**: Check against required tag keys (configurable)
- **Cost Allocation Tags**: Identify resources missing cost center tags
- **Orphaned Resources**: Resources without Owner tag
- **Environment Segregation**: Verify environment tags are consistent

## Implementation Priority

### Phase 1: Critical Services (High ROI)
1. EC2 enhancements (networking resources) - 15 new methods
2. ELBv2 (ALB/NLB) - 3 methods
3. CloudWatch Logs - 2 methods
4. IAM Access Analyzer - 2 methods
5. Security Hub - 3 methods

### Phase 2: Common Services
6. EventBridge - 3 methods
7. Step Functions - 2 methods
8. Lambda enhancements - 2 methods
9. ECS/EKS enhancements - 5 methods
10. Glue - 4 methods

### Phase 3: Tag Report Feature
11. Implement tag_analyzer.py
12. Add CLI integration
13. Create report templates

### Phase 4: Additional Services
14. Remaining 30+ services based on usage patterns

## Technical Considerations

### Services Requiring Special Parameters
Some services need specific parameters that may require two-step scanning:
- **ECS services**: Need cluster ARN
- **EKS node groups**: Need cluster name
- **Lambda event sources**: Optional filtering
- **Organizations OUs**: Need parent ID (can start with root)

**Solution**: Add a new method type for dependent services that first lists parent resources.

### Global vs Regional Services
Some services are global but accessible from any region:
- **CloudFront**: Global, but accessed via us-east-1
- **Route53**: Global
- **IAM**: Global
- **Organizations**: Global (us-east-1)
- **S3 Control**: Per-account, accessed via us-east-1

### Pagination Edge Cases
Services with custom pagination:
- **EC2 describe_snapshots**: Needs owner filter
- **EC2 describe_images**: Needs owner filter
- **Organizations**: Multiple list operations with different filters
- **Security Hub get_findings**: May have limits

## Estimated Impact

### Coverage Improvement
- **Current**: ~25 services, ~80 API calls
- **After Phase 1-2**: ~45 services, ~150 API calls
- **After Phase 4**: ~75 services, ~250 API calls

### Tag Report Value
- Identify $1000s in untagged resources
- Improve cost allocation accuracy
- Ensure compliance with tagging policies
- Reduce security risks from untracked resources

## Next Steps

1. **Review and prioritize** services based on your AWS usage
2. **Implement Phase 1** services (highest value, lowest complexity)
3. **Build tag analyzer** module
4. **Test thoroughly** with your AWS environment
5. **Document new services** in docs/services.md
6. **Update version** to 0.2.0 for major feature release

Would you like me to proceed with implementing any of these enhancements?
