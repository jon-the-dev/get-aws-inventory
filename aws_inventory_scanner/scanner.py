"""AWS Inventory Scanner - Main scanner module."""

import argparse
import concurrent.futures
import json
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime as dt

import boto3
import botocore
from botocore.client import Config

from .tag_analyzer import TagAnalyzer


class AWSInventoryScanner:
    """AWS Inventory Scanner class."""
    
    def __init__(self, regions=None, output_dir="./inventory", workers=35):
        """Initialize the scanner.
        
        Args:
            regions: List of regions to scan. If None, scans all regions.
            output_dir: Directory to store inventory files.
            workers: Number of concurrent workers.
        """
        self.regions = regions
        self.output_dir = output_dir
        self.workers = workers
        
        self.config = Config(
            connect_timeout=5,
            max_pool_connections=100,
            retries={"max_attempts": 5, "mode": "adaptive"},
        )
        
        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Service definitions
        self.paginated_services_east = {
            "iam": [  # only us-east-1
                ("list_users", "Users"),
                ("list_roles", "Roles"),
                ("list_groups", "Groups"),
            ],
            "route53domains": [("list_domains", "Domains")],  # only us-east-1
        }

        self.paginated_services = {
            "acm": [("list_certificates", "CertificateSummaryList")],
            "autoscaling": [
                ("describe_auto_scaling_groups", "AutoScalingGroups"),
                ("describe_launch_configurations", "LaunchConfigurations"),
                ("describe_auto_scaling_instances", "AutoScalingInstances"),
            ],
            "athena": [("list_data_catalogs", "DataCatalogsSummary")],
            "config": [
                ("describe_config_rules", "ConfigRules"),
                ("describe_configuration_aggregators", "ConfigurationAggregators"),
                ("list_resource_evaluations", "ResourceEvaluations"),
            ],
            "backup": [
                ("list_backup_plans", "BackupPlansList"),
                ("list_backup_vaults", "BackupVaultList"),
                ("list_backup_jobs", "BackupJobs"),
            ],
            "cloudfront": [
                ("list_distributions", "DistributionList"),
                (
                    "list_cloud_front_origin_access_identities",
                    "CloudFrontOriginAccessIdentityList",
                ),
            ],
            "codedeploy": [
                ("list_applications", "Applications"),
                ("list_deployments", "Deployments"),
            ],
            "ec2": [
                ("describe_instances", "Reservations"),
                ("describe_security_groups", "SecurityGroups"),
                ("describe_vpcs", "Vpcs"),
                ("describe_volumes", "Volumes"),
                ("describe_subnets", "Subnets"),
                ("describe_network_interfaces", "NetworkInterfaces"),
                ("describe_vpc_endpoints", "VpcEndpoints"),
                ("describe_nat_gateways", "NatGateways"),
                ("describe_internet_gateways", "InternetGateways"),
                ("describe_route_tables", "RouteTables"),
                ("describe_vpc_peering_connections", "VpcPeeringConnections"),
                ("describe_transit_gateways", "TransitGateways"),
                ("describe_transit_gateway_attachments", "TransitGatewayAttachments"),
                ("describe_network_acls", "NetworkAcls"),
                ("describe_snapshots", "Snapshots"),
                ("describe_images", "Images"),
            ],
            "ecr": [
                ("describe_repositories", "Repositories"),
            ],
            "efs": [
                ("describe_file_systems", "FileSystems"),
            ],
            "eks": [
                ("list_clusters", "Clusters"),
            ],
            "elasticache": [
                ("describe_cache_clusters", "CacheClusters"),
                ("describe_replication_groups", "ReplicationGroups"),
                ("describe_cache_parameter_groups", "CacheParameterGroups"),
            ],
            "elasticbeanstalk": [("describe_environments", "Environments")],
            "elb": [
                ("describe_load_balancers", "LoadBalancerDescriptions"),
            ],
            "es": [
                (
                    "describe_reserved_elasticsearch_instances",
                    "ReservedElasticsearchInstances",
                ),
            ],
            "lambda": [
                ("list_functions", "Functions"),
                ("list_layers", "Layers"),
                ("list_event_source_mappings", "EventSourceMappings"),
            ],
            "rds": [
                ("describe_db_instances", "DBInstances"),
                ("describe_db_snapshots", "DBSnapshots"),
                ("describe_db_subnet_groups", "DBSubnetGroups"),
                ("describe_db_clusters", "DBClusters"),
                ("describe_db_proxies", "DBProxies"),
                ("describe_db_parameter_groups", "DBParameterGroups"),
                ("describe_event_subscriptions", "EventSubscriptionsList"),
            ],
            "s3": [
                ("list_buckets", "Buckets"),
            ],
            "secretsmanager": [("list_secrets", "SecretList")],
            "sagemaker": [
                ("list_clusters", "ClusterSummaries"),
                ("list_endpoints", "Endpoints"),
                ("list_notebook_instances", "NotebookInstances"),
            ],
            # AI/ML Services (paginated only)
            "rekognition": [
                ("list_collections", "CollectionIds"),
                ("list_stream_processors", "StreamProcessors"),
            ],
            "comprehend": [
                ("list_document_classifiers", "DocumentClassifierPropertiesList"),
                ("list_entities_detection_jobs", "EntitiesDetectionJobPropertiesList"),
            ],
            "polly": [
                ("list_lexicons", "Lexicons"),
            ],
            "textract": [
                ("list_adapters", "Adapters"),
            ],
            "forecast": [
                ("list_datasets", "Datasets"),
                ("list_predictors", "Predictors"),
            ],
            "personalize": [
                ("list_datasets", "datasets"),
                ("list_solutions", "solutions"),
            ],
            "sns": [("list_topics", "Topics")],
            "sqs": [("list_queues", "QueueUrls")],
            "cloudformation": [("describe_stacks", "Stacks")],
            "cloudwatch": [("describe_alarms", "MetricAlarms")],
            "route53": [("list_hosted_zones", "HostedZones")],
            "dynamodb": [
                ("list_tables", "TableNames"),
                ("list_backups", "BackupSummaries"),
            ],
            "ecs": [
                ("list_clusters", "ClusterArns"),
            ],
            "workspaces": [("describe_workspaces", "Workspaces")],
            "fsx": [("describe_file_systems", "FileSystems")],
            "glacier": [("list_vaults", "VaultList")],
            "guardduty": [
                ("list_detectors", "DetectorIds"),
            ],
            "redshift": [
                ("describe_clusters", "Clusters"),
            ],
            "network-firewall": [("list_firewalls", "Firewalls")],
            # Networking services
            "elbv2": [
                ("describe_load_balancers", "LoadBalancers"),
                ("describe_target_groups", "TargetGroups"),
            ],
            "globalaccelerator": [
                ("list_accelerators", "Accelerators"),
            ],
            # Security services
            "securityhub": [
                ("list_members", "Members"),
                ("describe_standards", "Standards"),
            ],
            "accessanalyzer": [
                ("list_analyzers", "analyzers"),
            ],
            "inspector2": [
                ("list_findings", "findings"),
            ],
            "macie2": [
                ("list_classification_jobs", "items"),
            ],
            "ram": [
                ("get_resource_shares", "resourceShares"),
            ],
            "cognito-idp": [
                ("list_user_pools", "UserPools"),
            ],
            "cognito-identity": [
                ("list_identity_pools", "IdentityPools"),
            ],
            "acm-pca": [
                ("list_certificate_authorities", "CertificateAuthorities"),
            ],
            # Database services
            "docdb": [
                ("describe_db_clusters", "DBClusters"),
                ("describe_db_instances", "DBInstances"),
            ],
            "neptune": [
                ("describe_db_clusters", "DBClusters"),
                ("describe_db_instances", "DBInstances"),
            ],
            "timestream-query": [
                ("list_scheduled_queries", "ScheduledQueries"),
            ],
            # Analytics services
            "emr": [
                ("list_clusters", "Clusters"),
                ("list_studios", "Studios"),
            ],
            "kinesis": [
                ("list_streams", "StreamNames"),
            ],
            "kinesisanalyticsv2": [
                ("list_applications", "ApplicationSummaries"),
            ],
            "kafka": [
                ("list_clusters_v2", "ClusterInfoList"),
            ],
            "glue": [
                ("get_databases", "DatabaseList"),
                ("get_crawlers", "Crawlers"),
            ],
            "datapipeline": [
                ("list_pipelines", "pipelineIdList"),
            ],
            # Application Integration
            "events": [
                ("list_rules", "Rules"),
            ],
            "stepfunctions": [
                ("list_state_machines", "stateMachines"),
                ("list_activities", "activities"),
            ],
            "appsync": [
                ("list_graphql_apis", "graphqlApis"),
            ],
            "mq": [
                ("list_brokers", "BrokerSummaries"),
            ],
            "apigateway": [
                ("get_rest_apis", "items"),
                ("get_domain_names", "items"),
            ],
            # Management & Governance
            "logs": [
                ("describe_log_groups", "logGroups"),
            ],
            "organizations": [
                ("list_accounts", "Accounts"),
            ],
            "servicecatalog": [
                ("list_portfolios", "PortfolioDetails"),
            ],
            "resource-groups": [
                ("list_groups", "GroupIdentifiers"),
            ],
            "application-autoscaling": [
                ("describe_scalable_targets", "ScalableTargets"),
            ],
            # Developer Tools
            "codepipeline": [
                ("list_pipelines", "pipelines"),
                ("list_webhooks", "webhooks"),
            ],
            "codecommit": [
                ("list_repositories", "repositories"),
            ],
            "codeartifact": [
                ("list_repositories", "repositories"),
                ("list_domains", "domains"),
            ],
            "xray": [
                ("get_groups", "Groups"),
            ],
            # Storage
            "storagegateway": [
                ("list_gateways", "Gateways"),
            ],
            "transfer": [
                ("list_servers", "Servers"),
            ],
            # Compute
            "batch": [
                ("describe_job_queues", "jobQueues"),
                ("describe_compute_environments", "computeEnvironments"),
            ],
            "lightsail": [
                ("get_instances", "instances"),
            ],
        }
        
        self.non_paginated_services = {
            "apigatewayv2": ("get_apis", "Items"),
            "kms": ("list_keys", "Keys"),
            "cloudtrail": ("describe_trails", "trailList"),
            "codebuild": ("list_projects", "Projects"),
            "waf": ("list_web_acls", "WebACLs"),
            "ssm": ("get_parameters_by_path", "Parameters"),
            # AI/ML non-paginated
            "bedrock": ("list_foundation_models", "modelSummaries"),
            "bedrock-agent": ("list_agents", "agentSummaries"),
            "translate": ("list_terminologies", "TerminologyPropertiesList"),
            "transcribe": ("list_transcription_jobs", "TranscriptionJobSummaries"),
            "lexv2-models": ("list_bots", "botSummaries"),
            "kendra": ("list_indices", "IndexConfigurationSummaryItems"),
            # Additional services
            "iot": ("list_things", "things"),
            "gamelift": ("list_fleets", "FleetIds"),
            "firehose": ("list_delivery_streams", "DeliveryStreamNames"),
            "sesv2": ("list_email_identities", "EmailIdentities"),
            "apprunner": ("list_services", "ServiceSummaryList"),
            "timestream-write": ("list_databases", "Databases"),
        }

    def get_all_regions(self, cred_data):
        """Get all AWS regions."""
        ec2 = boto3.client(
            "ec2",
            aws_access_key_id=cred_data["accessKeyId"],
            aws_secret_access_key=cred_data["secretAccessKey"],
            aws_session_token=cred_data["sessionToken"],
        )
        return [region["RegionName"] for region in ec2.describe_regions()["Regions"]]

    def paginate_and_collect(self, client, method_name, key):
        """Paginate and collect resources."""
        paginator = client.get_paginator(method_name)
        resources = []
        try:
            for page in paginator.paginate():
                resources.extend(page.get(key, []))
        except botocore.exceptions.ClientError as err:
            self.logger.debug("Error collecting %s/%s: %s", method_name, key, err)
        return resources

    def handle_non_paginated_service(self, client, method_name, key, params=None):
        """Handle non-paginated service."""
        if params is None:
            params = {}

        method = getattr(client, method_name)
        svc_name = client.meta.service_model.service_name

        # Special handling for services that require specific parameters
        if svc_name == "ssm" and method_name == "get_parameters_by_path":
            if "Path" not in params:
                params["Path"] = "/"

        resources = []
        try:
            while True:
                response = method(**params)
                resources.extend(response.get(key, []))
                if "NextToken" in response:
                    params["NextToken"] = response["NextToken"]
                else:
                    break
        except botocore.exceptions.ClientError as err:
            self.logger.debug("Error collecting %s/%s: %s", method_name, key, err)
            return []

        return resources

    def write_to_file(self, data, file_name):
        """Write data to a file."""
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, sort_keys=True, default=str)
        except Exception as err:
            self.logger.error("Error writing to file: %s", err)
            with open(file_name.replace('.json', '.txt'), "w", encoding="utf-8") as f:
                f.write(str(data))
        self.logger.debug("Data written to %s", file_name)

    def process_service_region(self, service, method, key, region, aws_acct_id, cred_data):
        """Process a service in a specific region."""
        all_resources = []
        try:
            file_name = f"{self.output_dir}/{aws_acct_id}-{service}-{region}-{method}-{key}.json"
            if os.path.exists(file_name):
                self.logger.debug("%s already exists. Skipping.", file_name)
                return f"{file_name} already exists. Skipping."
                
            session = boto3.Session()
            client = session.client(
                service,
                region_name=region,
                config=self.config,
                aws_access_key_id=cred_data["accessKeyId"],
                aws_secret_access_key=cred_data["secretAccessKey"],
                aws_session_token=cred_data["sessionToken"],
            )

            if service in self.non_paginated_services:
                resources = self.handle_non_paginated_service(client, method, key)
            else:
                resources = self.paginate_and_collect(client, method, key)

            all_resources.extend(resources)
            self.logger.info(
                "Collected %s %s resources in %s using %s/%s",
                len(resources),
                service,
                region,
                method,
                key,
            )
            self.write_to_file(all_resources, file_name)
        except botocore.exceptions.BotoCoreError as e:
            self.logger.debug(
                "Error collecting %s resources in %s: %s",
                service,
                region,
                e,
            )
        return (service, all_resources)

    def scan(self, profile_name=None):
        """Run the AWS inventory scan."""
        # Get credentials
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
        else:
            session = boto3.Session()
            
        # Get temporary credentials
        sts_client = session.client("sts", region_name="us-east-1", config=self.config)
        cred_data = sts_client.get_session_token()["Credentials"]
        
        # Get account ID
        aws_acct_id = sts_client.get_caller_identity()["Account"]
        
        # Get regions to scan
        if self.regions is None:
            regions = self.get_all_regions(cred_data)
        else:
            regions = self.regions
            
        self.logger.info("Starting AWS inventory scan for account %s", aws_acct_id)
        self.logger.info("Scanning regions: %s", regions)

        futures = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            # US-East-1 only services
            for service, methods in self.paginated_services_east.items():
                region = "us-east-1"
                for method, key in methods:
                    futures.append(
                        executor.submit(
                            self.process_service_region,
                            service,
                            method,
                            key,
                            region,
                            aws_acct_id,
                            cred_data,
                        )
                    )

            # Regional paginated services
            for service, methods in self.paginated_services.items():
                for region in regions:
                    for method, key in methods:
                        futures.append(
                            executor.submit(
                                self.process_service_region,
                                service,
                                method,
                                key,
                                region,
                                aws_acct_id,
                                cred_data,
                            )
                        )

            # Regional non-paginated services
            for service, (method, key) in self.non_paginated_services.items():
                for region in regions:
                    futures.append(
                        executor.submit(
                            self.process_service_region,
                            service,
                            method,
                            key,
                            region,
                            aws_acct_id,
                            cred_data,
                        )
                    )

        # Wait for all futures to complete
        completed_count = 0
        total_count = len(futures)
        
        for future in as_completed(futures):
            completed_count += 1
            result = future.result()
            if completed_count % 10 == 0:
                self.logger.info("Completed %d/%d tasks", completed_count, total_count)
                
        self.logger.info("AWS inventory scan completed. Results saved to %s", self.output_dir)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AWS Inventory Scanner - Scan and inventory AWS resources across regions"
    )
    parser.add_argument(
        "--region",
        action="append",
        help="AWS region to scan (can be specified multiple times). If not specified, scans all regions."
    )
    parser.add_argument(
        "--profile",
        help="AWS profile to use for authentication"
    )
    parser.add_argument(
        "--output-dir",
        default="./inventory",
        help="Directory to store inventory files (default: ./inventory)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=35,
        help="Number of concurrent workers (default: 35)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--generate-tag-report",
        action="store_true",
        help="Generate tag analysis report from existing inventory files"
    )
    parser.add_argument(
        "--tag-report-format",
        choices=["json", "csv", "both"],
        default="both",
        help="Tag report output format (default: both)"
    )
    parser.add_argument(
        "--required-tags",
        nargs="+",
        help="List of required tag keys for compliance checking"
    )

    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Handle tag report generation only
    if args.generate_tag_report:
        try:
            analyzer = TagAnalyzer(inventory_dir=args.output_dir)
            print(f"Analyzing tags in directory: {args.output_dir}")

            # Extract tags from all inventory files
            tags_data = analyzer.extract_tags_from_directory()

            print(
                f"Processed {tags_data['file_count']} files, "
                f"found {len(tags_data['resources'])} resources"
            )

            # Generate reports
            report_files = analyzer.generate_tag_report(
                tags_data, output_dir=args.output_dir
            )

            print("\nTag reports generated:")
            print(f"  Summary: {report_files['summary']}")
            print(f"  Detailed: {report_files['detailed']}")
            print(f"  CSV: {report_files['csv']}")

            # Generate compliance report if required tags specified
            if args.required_tags:
                timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
                compliance_file = os.path.join(
                    args.output_dir,
                    f"tag-compliance-report-{timestamp}.json"
                )
                compliance_report = analyzer.generate_compliance_report(
                    tags_data, args.required_tags, compliance_file
                )

                print(f"  Compliance: {compliance_file}")
                print(
                    f"\nTag Compliance: "
                    f"{compliance_report['compliance_percentage']}% "
                    f"({compliance_report['compliant_resources']}/"
                    f"{compliance_report['total_resources']} resources)"
                )

            # Print errors if any
            if tags_data['errors']:
                print(f"\nWarnings: {len(tags_data['errors'])} errors occurred")
                if args.verbose:
                    for error in tags_data['errors'][:10]:
                        print(f"  - {error}")

        except Exception as e:
            print(f"Error generating tag report: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

        return  # Exit after generating report

    # Create scanner instance and run scan
    scanner = AWSInventoryScanner(
        regions=args.region,
        output_dir=args.output_dir,
        workers=args.workers
    )

    try:
        scanner.scan(profile_name=args.profile)
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error during scan: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
