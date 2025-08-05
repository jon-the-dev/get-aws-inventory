# Supported AWS Services

The AWS Inventory Scanner supports comprehensive resource discovery across 25+ AWS services. This page provides a complete list of all supported services and the specific resources that are collected.

## Service Categories

### Compute Services

#### Amazon EC2 (Elastic Compute Cloud)
- **Instances**: Running, stopped, and terminated EC2 instances
- **Security Groups**: Inbound and outbound rules for network security
- **VPCs**: Virtual Private Clouds and their configurations
- **Volumes**: EBS volumes (attached and unattached)
- **Subnets**: Public and private subnets
- **Network Interfaces**: Elastic Network Interfaces (ENIs)
- **Elastic IPs**: Allocated Elastic IP addresses

**API Methods Used:**
- `describe_instances` → Reservations
- `describe_security_groups` → SecurityGroups
- `describe_vpcs` → Vpcs
- `describe_volumes` → Volumes
- `describe_subnets` → Subnets
- `describe_network_interfaces` → NetworkInterfaces
- `describe_addresses` → Addresses

#### AWS Lambda
- **Functions**: Lambda functions with their configurations
- **Runtime information**: Runtime versions, memory, timeout settings
- **Environment variables**: Function environment configurations

**API Methods Used:**
- `list_functions` → Functions

#### Amazon ECS (Elastic Container Service)
- **Clusters**: ECS cluster configurations
- **Services**: Running services within clusters
- **Task definitions**: Container task specifications

**API Methods Used:**
- `list_clusters` → ClusterArns

#### Amazon EKS (Elastic Kubernetes Service)
- **Clusters**: Kubernetes cluster configurations
- **Node groups**: Worker node configurations
- **Networking**: VPC and subnet configurations

**API Methods Used:**
- `list_clusters` → Clusters

#### AWS Elastic Beanstalk
- **Environments**: Application environments and their configurations
- **Applications**: Deployed applications
- **Platform versions**: Runtime platform information

**API Methods Used:**
- `describe_environments` → Environments

### Storage Services

#### Amazon S3 (Simple Storage Service)
- **Buckets**: All S3 buckets in the account
- **Bucket policies**: Access control policies
- **Versioning**: Bucket versioning configurations

**API Methods Used:**
- `list_buckets` → Buckets

#### Amazon EFS (Elastic File System)
- **File Systems**: EFS file systems and their configurations
- **Mount targets**: Network mount points
- **Access points**: Application-specific access configurations

**API Methods Used:**
- `describe_file_systems` → FileSystems

#### Amazon FSx
- **File Systems**: FSx file systems (Windows, Lustre, NetApp, OpenZFS)
- **Backups**: File system backups
- **Storage configurations**: Performance and capacity settings

**API Methods Used:**
- `describe_file_systems` → FileSystems

#### Amazon Glacier
- **Vaults**: Glacier vaults for long-term archival
- **Vault policies**: Access control policies
- **Archive inventories**: Stored archive information

**API Methods Used:**
- `list_vaults` → VaultList

### Database Services

#### Amazon RDS (Relational Database Service)
- **DB Instances**: Database instances (MySQL, PostgreSQL, Oracle, SQL Server, etc.)
- **DB Snapshots**: Database backups and snapshots
- **DB Subnet Groups**: Network configurations for databases
- **DB Clusters**: Aurora clusters and their configurations

**API Methods Used:**
- `describe_db_instances` → DBInstances
- `describe_db_snapshots` → DBSnapshots
- `describe_db_subnet_groups` → DBSubnetGroups
- `describe_db_clusters` → DBClusters

#### Amazon DynamoDB
- **Tables**: DynamoDB tables and their configurations
- **Backups**: Point-in-time recovery and on-demand backups
- **Global tables**: Multi-region table configurations

**API Methods Used:**
- `list_tables` → TableNames
- `list_backups` → BackupSummaries

#### Amazon ElastiCache
- **Cache Clusters**: Redis and Memcached clusters
- **Replication groups**: Redis replication configurations
- **Parameter groups**: Cache configuration parameters

**API Methods Used:**
- `describe_cache_clusters` → CacheClusters

#### Amazon Redshift
- **Clusters**: Data warehouse clusters
- **Snapshots**: Cluster snapshots and backups
- **Parameter groups**: Cluster configuration parameters

**API Methods Used:**
- `describe_clusters` → Clusters

### Networking Services

#### Elastic Load Balancing (ELB)
- **Load Balancers**: Classic, Application, and Network Load Balancers
- **Target groups**: Load balancer targets
- **Listeners**: Load balancer routing rules

**API Methods Used:**
- `describe_load_balancers` → LoadBalancerDescriptions

#### Amazon CloudFront
- **Distributions**: CDN distributions and their configurations
- **Origin Access Identities**: S3 bucket access controls
- **Cache behaviors**: Content caching rules

**API Methods Used:**
- `list_distributions` → DistributionList
- `list_cloud_front_origin_access_identities` → CloudFrontOriginAccessIdentityList

#### Amazon Route 53
- **Hosted Zones**: DNS hosted zones
- **Record sets**: DNS records
- **Health checks**: Route 53 health monitoring

**API Methods Used:**
- `list_hosted_zones` → HostedZones

#### Route 53 Domains (US-East-1 only)
- **Domains**: Registered domain names
- **Domain configurations**: DNS and transfer settings

**API Methods Used:**
- `list_domains` → Domains

### Security Services

#### AWS IAM (Identity and Access Management) - US-East-1 only
- **Users**: IAM users and their configurations
- **Roles**: IAM roles and trust policies
- **Groups**: IAM groups and their members
- **Policies**: Managed and inline policies

**API Methods Used:**
- `list_users` → Users
- `list_roles` → Roles
- `list_groups` → Groups

#### AWS Secrets Manager
- **Secrets**: Stored secrets and their metadata
- **Rotation configurations**: Automatic rotation settings
- **Resource policies**: Access control policies

**API Methods Used:**
- `list_secrets` → SecretList

#### Amazon GuardDuty
- **Detectors**: GuardDuty detectors and their configurations
- **Findings**: Security findings and threats
- **Member accounts**: Multi-account configurations

**API Methods Used:**
- `list_detectors` → DetectorIds

#### AWS WAF (Web Application Firewall)
- **Web ACLs**: Web application firewall rules
- **Rule groups**: Reusable rule collections
- **IP sets**: IP address allow/deny lists

**API Methods Used:**
- `list_web_acls` → WebACLs

#### AWS Network Firewall
- **Firewalls**: Network firewall configurations
- **Firewall policies**: Traffic filtering rules
- **Rule groups**: Network security rules

**API Methods Used:**
- `list_firewalls` → Firewalls

### Management & Governance

#### AWS CloudFormation
- **Stacks**: Infrastructure stacks and their resources
- **Stack events**: Deployment history
- **Stack outputs**: Exported values

**API Methods Used:**
- `describe_stacks` → Stacks

#### Amazon CloudWatch
- **Alarms**: Metric alarms and their configurations
- **Metrics**: Custom and AWS service metrics
- **Dashboards**: CloudWatch dashboards

**API Methods Used:**
- `describe_alarms` → MetricAlarms

#### AWS Config
- **Configuration Rules**: Compliance rules
- **Configuration Aggregators**: Multi-account/region aggregation
- **Resource Evaluations**: Compliance evaluation results
- **Configuration Recorders**: Resource change tracking

**API Methods Used:**
- `describe_config_rules` → ConfigRules
- `describe_configuration_aggregators` → ConfigurationAggregators
- `list_resource_evaluations` → ResourceEvaluations
- `describe_configuration_recorders` → ConfigurationRecorders

#### AWS Backup
- **Backup Plans**: Backup scheduling and retention policies
- **Backup Vaults**: Backup storage locations
- **Backup Jobs**: Active and completed backup operations

**API Methods Used:**
- `list_backup_plans` → BackupPlansList
- `list_backup_vaults` → BackupVaultList
- `list_backup_jobs` → BackupJobs

#### AWS CloudTrail
- **Trails**: API logging configurations
- **Event history**: API call records
- **Insights**: CloudTrail Insights configurations

**API Methods Used:**
- `describe_trails` → trailList

### Developer Tools

#### AWS CodeBuild
- **Projects**: Build projects and their configurations
- **Builds**: Build history and status
- **Build environments**: Runtime environments

**API Methods Used:**
- `list_projects` → Projects

#### AWS CodeDeploy
- **Applications**: Deployment applications
- **Deployments**: Deployment history and status
- **Deployment groups**: Target configurations

**API Methods Used:**
- `list_applications` → Applications
- `list_deployments` → Deployments

### Analytics

#### Amazon Athena
- **Data Catalogs**: Metadata catalogs for querying
- **Databases**: Athena databases
- **Tables**: Queryable data tables

**API Methods Used:**
- `list_data_catalogs` → DataCatalogsSummary

### Machine Learning

#### Amazon SageMaker
- **Clusters**: SageMaker compute clusters
- **Endpoints**: Model serving endpoints
- **Notebook Instances**: Jupyter notebook environments
- **Models**: Trained machine learning models

**API Methods Used:**
- `list_clusters` → ClusterSummaries
- `list_endpoints` → Endpoints
- `list_notebook_instances` → NotebookInstances

### Application Integration

#### Amazon SNS (Simple Notification Service)
- **Topics**: SNS topics and their configurations
- **Subscriptions**: Topic subscriptions
- **Platform applications**: Mobile push notifications

**API Methods Used:**
- `list_topics` → Topics

#### Amazon SQS (Simple Queue Service)
- **Queues**: SQS queues and their configurations
- **Queue attributes**: Message retention, visibility timeout
- **Dead letter queues**: Failed message handling

**API Methods Used:**
- `list_queues` → QueueUrls

### Other Services

#### Amazon ECR (Elastic Container Registry)
- **Repositories**: Container image repositories
- **Images**: Stored container images
- **Repository policies**: Access control policies

**API Methods Used:**
- `describe_repositories` → Repositories

#### AWS Certificate Manager (ACM)
- **Certificates**: SSL/TLS certificates
- **Certificate validation**: Domain and DNS validation
- **Certificate usage**: Associated AWS resources

**API Methods Used:**
- `list_certificates` → CertificateSummaryList

#### Amazon API Gateway v2
- **APIs**: REST and WebSocket APIs
- **Stages**: API deployment stages
- **Routes**: API routing configurations

**API Methods Used:**
- `get_apis` → Items

#### Auto Scaling
- **Auto Scaling Groups**: EC2 auto scaling configurations
- **Launch Configurations**: Instance launch templates
- **Auto Scaling Instances**: Instances managed by auto scaling

**API Methods Used:**
- `describe_auto_scaling_groups` → AutoScalingGroups
- `describe_launch_configurations` → LaunchConfigurations
- `describe_auto_scaling_instances` → AutoScalingInstances

#### AWS Systems Manager (SSM)
- **Parameters**: Parameter Store values
- **Parameter hierarchies**: Organized parameter structures
- **Secure strings**: Encrypted parameter values

**API Methods Used:**
- `get_parameters_by_path` → Parameters

#### AWS Key Management Service (KMS)
- **Keys**: Customer and AWS managed keys
- **Key policies**: Access control policies
- **Key usage**: Encryption/decryption operations

**API Methods Used:**
- `list_keys` → Keys

#### Amazon WorkSpaces
- **WorkSpaces**: Virtual desktop instances
- **Directories**: Active Directory configurations
- **Bundles**: WorkSpace image configurations

**API Methods Used:**
- `describe_workspaces` → Workspaces

#### Amazon Elasticsearch Service
- **Reserved Instances**: Reserved Elasticsearch capacity
- **Domains**: Elasticsearch clusters
- **Domain configurations**: Cluster settings

**API Methods Used:**
- `describe_reserved_elasticsearch_instances` → ReservedElasticsearchInstances

## Regional vs Global Services

### Global Services (US-East-1 only)
These services are global and only scanned in the US-East-1 region:
- IAM (Users, Roles, Groups)
- Route 53 Domains

### Regional Services
All other services are scanned in each specified region or all regions if none are specified.

## Service Coverage Notes

- **Comprehensive Coverage**: The scanner aims to collect the most important resources from each service
- **Read-Only Operations**: All operations are read-only and do not modify your AWS resources
- **Error Handling**: Services that are not available in a region or lack permissions are gracefully skipped
- **Extensible**: The scanner architecture allows for easy addition of new services and resources

## Adding New Services

The scanner is designed to be easily extensible. New services can be added by updating the service definitions in the scanner configuration. See the [API Reference](api.md) for details on extending the scanner.
