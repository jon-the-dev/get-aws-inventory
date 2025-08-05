# Complete Resource List

This document provides a comprehensive list of all AWS resources that the AWS Inventory Scanner can discover and catalog, organized by service category.

## Summary Statistics

- **Total Services Supported**: 25+
- **Total Resource Types**: 75+
- **Regional Services**: 23
- **Global Services**: 2 (IAM, Route53 Domains)

## Compute Resources

### Amazon EC2 (Elastic Compute Cloud)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| EC2 Instances | `describe_instances` | `Reservations` | Virtual servers including running, stopped, and terminated instances |
| Security Groups | `describe_security_groups` | `SecurityGroups` | Virtual firewalls controlling inbound and outbound traffic |
| VPCs | `describe_vpcs` | `Vpcs` | Virtual Private Clouds and network configurations |
| EBS Volumes | `describe_volumes` | `Volumes` | Block storage volumes (attached and unattached) |
| Subnets | `describe_subnets` | `Subnets` | Network subnets within VPCs |
| Network Interfaces | `describe_network_interfaces` | `NetworkInterfaces` | Elastic Network Interfaces (ENIs) |
| Elastic IPs | `describe_addresses` | `Addresses` | Static IP addresses |

### AWS Lambda
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Functions | `list_functions` | `Functions` | Serverless functions with configurations and runtime information |

### Amazon ECS (Elastic Container Service)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Clusters | `list_clusters` | `ClusterArns` | Container orchestration clusters |

### Amazon EKS (Elastic Kubernetes Service)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Clusters | `list_clusters` | `Clusters` | Managed Kubernetes clusters |

### AWS Elastic Beanstalk
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Environments | `describe_environments` | `Environments` | Application deployment environments |

### Auto Scaling
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Auto Scaling Groups | `describe_auto_scaling_groups` | `AutoScalingGroups` | EC2 auto scaling configurations |
| Launch Configurations | `describe_launch_configurations` | `LaunchConfigurations` | Instance launch templates |
| Auto Scaling Instances | `describe_auto_scaling_instances` | `AutoScalingInstances` | Instances managed by auto scaling |

## Storage Resources

### Amazon S3 (Simple Storage Service)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Buckets | `list_buckets` | `Buckets` | Object storage buckets |

### Amazon EFS (Elastic File System)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| File Systems | `describe_file_systems` | `FileSystems` | Network-attached file systems |

### Amazon FSx
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| File Systems | `describe_file_systems` | `FileSystems` | High-performance file systems (Windows, Lustre, NetApp, OpenZFS) |

### Amazon Glacier
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Vaults | `list_vaults` | `VaultList` | Long-term archival storage vaults |

## Database Resources

### Amazon RDS (Relational Database Service)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| DB Instances | `describe_db_instances` | `DBInstances` | Relational database instances (MySQL, PostgreSQL, Oracle, SQL Server, etc.) |
| DB Snapshots | `describe_db_snapshots` | `DBSnapshots` | Database backups and snapshots |
| DB Subnet Groups | `describe_db_subnet_groups` | `DBSubnetGroups` | Network configurations for databases |
| DB Clusters | `describe_db_clusters` | `DBClusters` | Aurora clusters and configurations |

### Amazon DynamoDB
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Tables | `list_tables` | `TableNames` | NoSQL database tables |
| Backups | `list_backups` | `BackupSummaries` | Point-in-time recovery and on-demand backups |

### Amazon ElastiCache
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Cache Clusters | `describe_cache_clusters` | `CacheClusters` | Redis and Memcached clusters |

### Amazon Redshift
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Clusters | `describe_clusters` | `Clusters` | Data warehouse clusters |

## Networking Resources

### Elastic Load Balancing (ELB)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Load Balancers | `describe_load_balancers` | `LoadBalancerDescriptions` | Classic, Application, and Network Load Balancers |

### Amazon CloudFront
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Distributions | `list_distributions` | `DistributionList` | CDN distributions and configurations |
| Origin Access Identities | `list_cloud_front_origin_access_identities` | `CloudFrontOriginAccessIdentityList` | S3 bucket access controls |

### Amazon Route 53
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Hosted Zones | `list_hosted_zones` | `HostedZones` | DNS hosted zones |

### Route 53 Domains (Global - US-East-1 only)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Domains | `list_domains` | `Domains` | Registered domain names |

## Security Resources

### AWS IAM (Identity and Access Management) - Global (US-East-1 only)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Users | `list_users` | `Users` | IAM users and their configurations |
| Roles | `list_roles` | `Roles` | IAM roles and trust policies |
| Groups | `list_groups` | `Groups` | IAM groups and their members |

### AWS Secrets Manager
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Secrets | `list_secrets` | `SecretList` | Stored secrets and their metadata |

### Amazon GuardDuty
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Detectors | `list_detectors` | `DetectorIds` | Threat detection service configurations |

### AWS WAF (Web Application Firewall)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Web ACLs | `list_web_acls` | `WebACLs` | Web application firewall rules |

### AWS Network Firewall
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Firewalls | `list_firewalls` | `Firewalls` | Network firewall configurations |

### AWS Key Management Service (KMS)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Keys | `list_keys` | `Keys` | Customer and AWS managed encryption keys |

## Management & Governance Resources

### AWS CloudFormation
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Stacks | `describe_stacks` | `Stacks` | Infrastructure as code stacks |

### Amazon CloudWatch
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Alarms | `describe_alarms` | `MetricAlarms` | Metric alarms and monitoring configurations |

### AWS Config
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Configuration Rules | `describe_config_rules` | `ConfigRules` | Compliance rules |
| Configuration Aggregators | `describe_configuration_aggregators` | `ConfigurationAggregators` | Multi-account/region aggregation |
| Resource Evaluations | `list_resource_evaluations` | `ResourceEvaluations` | Compliance evaluation results |
| Configuration Recorders | `describe_configuration_recorders` | `ConfigurationRecorders` | Resource change tracking |

### AWS Backup
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Backup Plans | `list_backup_plans` | `BackupPlansList` | Backup scheduling and retention policies |
| Backup Vaults | `list_backup_vaults` | `BackupVaultList` | Backup storage locations |
| Backup Jobs | `list_backup_jobs` | `BackupJobs` | Active and completed backup operations |

### AWS CloudTrail
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Trails | `describe_trails` | `trailList` | API logging configurations |

## Developer Tools Resources

### AWS CodeBuild
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Projects | `list_projects` | `Projects` | Build projects and configurations |

### AWS CodeDeploy
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Applications | `list_applications` | `Applications` | Deployment applications |
| Deployments | `list_deployments` | `Deployments` | Deployment history and status |

## Analytics Resources

### Amazon Athena
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Data Catalogs | `list_data_catalogs` | `DataCatalogsSummary` | Metadata catalogs for querying |

## Machine Learning Resources

### Amazon SageMaker
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Clusters | `list_clusters` | `ClusterSummaries` | SageMaker compute clusters |
| Endpoints | `list_endpoints` | `Endpoints` | Model serving endpoints |
| Notebook Instances | `list_notebook_instances` | `NotebookInstances` | Jupyter notebook environments |

## Application Integration Resources

### Amazon SNS (Simple Notification Service)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Topics | `list_topics` | `Topics` | Notification topics and configurations |

### Amazon SQS (Simple Queue Service)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Queues | `list_queues` | `QueueUrls` | Message queues and configurations |

## Container Resources

### Amazon ECR (Elastic Container Registry)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Repositories | `describe_repositories` | `Repositories` | Container image repositories |

## Certificate Resources

### AWS Certificate Manager (ACM)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Certificates | `list_certificates` | `CertificateSummaryList` | SSL/TLS certificates |

## API Resources

### Amazon API Gateway v2
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| APIs | `get_apis` | `Items` | REST and WebSocket APIs |

## Systems Management Resources

### AWS Systems Manager (SSM)
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Parameters | `get_parameters_by_path` | `Parameters` | Parameter Store values and configurations |

## Workspace Resources

### Amazon WorkSpaces
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| WorkSpaces | `describe_workspaces` | `Workspaces` | Virtual desktop instances |

## Search Resources

### Amazon Elasticsearch Service
| Resource Type | API Method | Response Key | Description |
|---------------|------------|--------------|-------------|
| Reserved Instances | `describe_reserved_elasticsearch_instances` | `ReservedElasticsearchInstances` | Reserved Elasticsearch capacity |

## Resource Coverage by Service

### High Coverage Services (5+ Resource Types)
- **Amazon EC2**: 7 resource types (Instances, Security Groups, VPCs, Volumes, Subnets, Network Interfaces, Elastic IPs)
- **Amazon RDS**: 4 resource types (DB Instances, Snapshots, Subnet Groups, Clusters)
- **AWS IAM**: 3 resource types (Users, Roles, Groups)
- **Auto Scaling**: 3 resource types (Groups, Launch Configurations, Instances)
- **AWS Config**: 4 resource types (Rules, Aggregators, Evaluations, Recorders)
- **AWS Backup**: 3 resource types (Plans, Vaults, Jobs)
- **Amazon SageMaker**: 3 resource types (Clusters, Endpoints, Notebook Instances)

### Medium Coverage Services (2-4 Resource Types)
- **Amazon CloudFront**: 2 resource types
- **AWS CodeDeploy**: 2 resource types
- **Amazon DynamoDB**: 2 resource types

### Single Resource Services
Most services provide 1 primary resource type, focusing on their core functionality.

## Regional Distribution

### Global Services (US-East-1 Only)
- AWS IAM (Users, Roles, Groups)
- Route 53 Domains

### Regional Services (All Specified Regions)
All other services are scanned across all specified regions, allowing for:
- Multi-region resource discovery
- Regional compliance checking
- Disaster recovery planning
- Cost optimization across regions

## File Output Summary

The scanner generates approximately **75+ JSON files per region** (depending on resource availability), with the naming convention:
```
{account_id}-{service}-{region}-{api_method}-{response_key}.json
```

For a full account scan across all regions (~20 regions), this results in approximately **1,500+ JSON files** containing comprehensive resource inventory data.

## Resource Identification Patterns

### Common Resource Identifiers
- **EC2 Instances**: `InstanceId` (i-1234567890abcdef0)
- **S3 Buckets**: `Name` (bucket-name)
- **RDS Instances**: `DBInstanceIdentifier` (mydb-instance)
- **Lambda Functions**: `FunctionName` (my-function)
- **IAM Users**: `UserName` (username)
- **VPCs**: `VpcId` (vpc-12345678)
- **Security Groups**: `GroupId` (sg-12345678)

### Resource Relationships
The scanner captures resource relationships through:
- **VPC associations** (instances → subnets → VPCs)
- **Security group attachments** (instances → security groups)
- **Volume attachments** (instances → EBS volumes)
- **Load balancer targets** (load balancers → instances)
- **IAM role assignments** (services → IAM roles)

This comprehensive resource discovery enables detailed analysis of your AWS infrastructure, security posture, and cost optimization opportunities.
