"""Test suite for new AWS services added to inventory scanner."""

import pytest
import boto3
from aws_inventory_scanner.scanner import AWSInventoryScanner


class TestNewNetworkingServices:
    """Test networking services."""

    @pytest.fixture
    def scanner(self):
        return AWSInventoryScanner()

    def test_ec2_enhanced_methods(self, scanner):
        """Test enhanced EC2 networking methods."""
        client = boto3.client("ec2", region_name="us-east-1")
        
        ec2_methods = [m for m, _ in scanner.paginated_services["ec2"]]
        
        # Verify new networking methods exist
        assert "describe_vpc_endpoints" in ec2_methods
        assert "describe_nat_gateways" in ec2_methods
        assert "describe_transit_gateways" in ec2_methods
        assert "describe_snapshots" in ec2_methods
        
        # Verify they can paginate
        assert client.can_paginate("describe_vpc_endpoints")
        assert client.can_paginate("describe_nat_gateways")
        assert client.can_paginate("describe_transit_gateways")

    def test_elbv2_methods(self, scanner):
        """Test ELBv2 (ALB/NLB) methods."""
        assert "elbv2" in scanner.paginated_services
        
        client = boto3.client("elbv2", region_name="us-east-1")
        assert hasattr(client, "describe_load_balancers")
        assert hasattr(client, "describe_target_groups")
        assert client.can_paginate("describe_load_balancers")
        assert client.can_paginate("describe_target_groups")

    def test_globalaccelerator_methods(self, scanner):
        """Test Global Accelerator methods."""
        assert "globalaccelerator" in scanner.paginated_services
        
        client = boto3.client("globalaccelerator", region_name="us-west-2")
        assert hasattr(client, "list_accelerators")
        assert client.can_paginate("list_accelerators")

    def test_directconnect_methods(self, scanner):
        """Test Direct Connect methods."""
        # Direct Connect methods are not paginated, skipping
        pass


class TestNewSecurityServices:
    """Test security services."""

    @pytest.fixture
    def scanner(self):
        return AWSInventoryScanner()

    def test_securityhub_methods(self, scanner):
        """Test Security Hub methods."""
        assert "securityhub" in scanner.paginated_services
        
        client = boto3.client("securityhub", region_name="us-east-1")
        assert hasattr(client, "list_members")
        assert hasattr(client, "describe_standards")
        assert client.can_paginate("list_members")

    def test_accessanalyzer_methods(self, scanner):
        """Test IAM Access Analyzer methods."""
        assert "accessanalyzer" in scanner.paginated_services
        
        client = boto3.client("accessanalyzer", region_name="us-east-1")
        assert hasattr(client, "list_analyzers")
        assert client.can_paginate("list_analyzers")

    def test_inspector2_methods(self, scanner):
        """Test Inspector v2 methods."""
        assert "inspector2" in scanner.paginated_services
        
        client = boto3.client("inspector2", region_name="us-east-1")
        assert hasattr(client, "list_findings")
        assert client.can_paginate("list_findings")

    def test_macie2_methods(self, scanner):
        """Test Macie methods."""
        assert "macie2" in scanner.paginated_services
        
        client = boto3.client("macie2", region_name="us-east-1")
        assert hasattr(client, "list_classification_jobs")
        assert client.can_paginate("list_classification_jobs")

    def test_cognito_methods(self, scanner):
        """Test Cognito methods."""
        assert "cognito-idp" in scanner.paginated_services
        assert "cognito-identity" in scanner.paginated_services
        
        idp_client = boto3.client("cognito-idp", region_name="us-east-1")
        assert hasattr(idp_client, "list_user_pools")
        assert idp_client.can_paginate("list_user_pools")
        
        identity_client = boto3.client("cognito-identity", region_name="us-east-1")
        assert hasattr(identity_client, "list_identity_pools")


class TestNewDatabaseServices:
    """Test database services."""

    @pytest.fixture
    def scanner(self):
        return AWSInventoryScanner()

    def test_rds_enhanced_methods(self, scanner):
        """Test enhanced RDS methods."""
        rds_methods = [m for m, _ in scanner.paginated_services["rds"]]
        
        assert "describe_db_proxies" in rds_methods
        assert "describe_db_parameter_groups" in rds_methods
        assert "describe_event_subscriptions" in rds_methods
        
        client = boto3.client("rds", region_name="us-east-1")
        assert client.can_paginate("describe_db_proxies")

    def test_docdb_methods(self, scanner):
        """Test DocumentDB methods."""
        assert "docdb" in scanner.paginated_services
        
        client = boto3.client("docdb", region_name="us-east-1")
        assert hasattr(client, "describe_db_clusters")
        assert hasattr(client, "describe_db_instances")
        assert client.can_paginate("describe_db_clusters")

    def test_neptune_methods(self, scanner):
        """Test Neptune methods."""
        assert "neptune" in scanner.paginated_services
        
        client = boto3.client("neptune", region_name="us-east-1")
        assert hasattr(client, "describe_db_clusters")
        assert client.can_paginate("describe_db_clusters")

    def test_timestream_methods(self, scanner):
        """Test Timestream methods."""
        # timestream-write list_databases is non-paginated
        assert "timestream-write" in scanner.non_paginated_services
        
        client = boto3.client("timestream-write", region_name="us-east-1")
        assert hasattr(client, "list_databases")

    def test_dynamodb_enhanced_methods(self, scanner):
        """Test enhanced DynamoDB methods."""
        # DynamoDB has list_tables and list_backups (paginated)
        dynamodb_methods = [m for m, _ in scanner.paginated_services["dynamodb"]]
        
        assert "list_tables" in dynamodb_methods
        assert "list_backups" in dynamodb_methods


class TestNewAnalyticsServices:
    """Test analytics services."""

    @pytest.fixture
    def scanner(self):
        return AWSInventoryScanner()

    def test_emr_methods(self, scanner):
        """Test EMR methods."""
        assert "emr" in scanner.paginated_services
        
        client = boto3.client("emr", region_name="us-east-1")
        assert hasattr(client, "list_clusters")
        assert hasattr(client, "list_studios")
        assert client.can_paginate("list_clusters")

    def test_kinesis_methods(self, scanner):
        """Test Kinesis methods."""
        assert "kinesis" in scanner.paginated_services
        
        client = boto3.client("kinesis", region_name="us-east-1")
        assert hasattr(client, "list_streams")
        assert client.can_paginate("list_streams")

    def test_firehose_methods(self, scanner):
        """Test Kinesis Firehose methods."""
        # list_delivery_streams is non-paginated
        assert "firehose" in scanner.non_paginated_services
        
        client = boto3.client("firehose", region_name="us-east-1")
        assert hasattr(client, "list_delivery_streams")

    def test_kafka_methods(self, scanner):
        """Test MSK (Kafka) methods."""
        assert "kafka" in scanner.paginated_services
        
        client = boto3.client("kafka", region_name="us-east-1")
        assert hasattr(client, "list_clusters_v2")
        assert client.can_paginate("list_clusters_v2")

    def test_glue_methods(self, scanner):
        """Test Glue methods."""
        assert "glue" in scanner.paginated_services
        
        client = boto3.client("glue", region_name="us-east-1")
        assert hasattr(client, "get_databases")
        assert hasattr(client, "get_crawlers")
        assert client.can_paginate("get_databases")


class TestNewApplicationIntegrationServices:
    """Test application integration services."""

    @pytest.fixture
    def scanner(self):
        return AWSInventoryScanner()

    def test_eventbridge_methods(self, scanner):
        """Test EventBridge methods."""
        assert "events" in scanner.paginated_services
        
        client = boto3.client("events", region_name="us-east-1")
        assert hasattr(client, "list_event_buses")
        assert hasattr(client, "list_rules")
        assert client.can_paginate("list_rules")

    def test_stepfunctions_methods(self, scanner):
        """Test Step Functions methods."""
        assert "stepfunctions" in scanner.paginated_services
        
        client = boto3.client("stepfunctions", region_name="us-east-1")
        assert hasattr(client, "list_state_machines")
        assert hasattr(client, "list_activities")
        assert client.can_paginate("list_state_machines")

    def test_appsync_methods(self, scanner):
        """Test AppSync methods."""
        assert "appsync" in scanner.paginated_services
        
        client = boto3.client("appsync", region_name="us-east-1")
        assert hasattr(client, "list_graphql_apis")
        assert client.can_paginate("list_graphql_apis")

    def test_mq_methods(self, scanner):
        """Test MQ methods."""
        assert "mq" in scanner.paginated_services
        
        client = boto3.client("mq", region_name="us-east-1")
        assert hasattr(client, "list_brokers")

    def test_ses_methods(self, scanner):
        """Test SES v2 methods."""
        # list_email_identities is non-paginated
        assert "sesv2" in scanner.non_paginated_services
        
        client = boto3.client("sesv2", region_name="us-east-1")
        assert hasattr(client, "list_email_identities")


class TestNewManagementServices:
    """Test management and governance services."""

    @pytest.fixture
    def scanner(self):
        return AWSInventoryScanner()

    def test_cloudwatch_logs_methods(self, scanner):
        """Test CloudWatch Logs methods."""
        assert "logs" in scanner.paginated_services
        
        client = boto3.client("logs", region_name="us-east-1")
        assert hasattr(client, "describe_log_groups")
        assert client.can_paginate("describe_log_groups")

    def test_organizations_methods(self, scanner):
        """Test Organizations methods."""
        assert "organizations" in scanner.paginated_services
        
        client = boto3.client("organizations", region_name="us-east-1")
        assert hasattr(client, "list_accounts")
        assert client.can_paginate("list_accounts")

    def test_servicecatalog_methods(self, scanner):
        """Test Service Catalog methods."""
        assert "servicecatalog" in scanner.paginated_services
        
        client = boto3.client("servicecatalog", region_name="us-east-1")
        assert hasattr(client, "list_portfolios")
        assert client.can_paginate("list_portfolios")


class TestNewDeveloperToolsServices:
    """Test developer tools services."""

    @pytest.fixture
    def scanner(self):
        return AWSInventoryScanner()

    def test_codepipeline_methods(self, scanner):
        """Test CodePipeline methods."""
        assert "codepipeline" in scanner.paginated_services
        
        client = boto3.client("codepipeline", region_name="us-east-1")
        assert hasattr(client, "list_pipelines")
        assert hasattr(client, "list_webhooks")
        assert client.can_paginate("list_pipelines")

    def test_codecommit_methods(self, scanner):
        """Test CodeCommit methods."""
        assert "codecommit" in scanner.paginated_services
        
        client = boto3.client("codecommit", region_name="us-east-1")
        assert hasattr(client, "list_repositories")
        assert client.can_paginate("list_repositories")

    def test_codeartifact_methods(self, scanner):
        """Test CodeArtifact methods."""
        assert "codeartifact" in scanner.paginated_services
        
        client = boto3.client("codeartifact", region_name="us-east-1")
        assert hasattr(client, "list_repositories")
        assert hasattr(client, "list_domains")
        assert client.can_paginate("list_repositories")


class TestNewComputeServices:
    """Test compute services."""

    @pytest.fixture
    def scanner(self):
        return AWSInventoryScanner()

    def test_batch_methods(self, scanner):
        """Test Batch methods."""
        assert "batch" in scanner.paginated_services
        
        client = boto3.client("batch", region_name="us-east-1")
        assert hasattr(client, "describe_job_queues")
        assert hasattr(client, "describe_compute_environments")
        assert client.can_paginate("describe_job_queues")

    def test_apprunner_methods(self, scanner):
        """Test App Runner methods."""
        # list_services is non-paginated
        assert "apprunner" in scanner.non_paginated_services
        
        client = boto3.client("apprunner", region_name="us-east-1")
        assert hasattr(client, "list_services")

    def test_lambda_enhanced_methods(self, scanner):
        """Test enhanced Lambda methods."""
        lambda_methods = [m for m, _ in scanner.paginated_services["lambda"]]
        
        assert "list_layers" in lambda_methods
        assert "list_event_source_mappings" in lambda_methods
        
        client = boto3.client("lambda", region_name="us-east-1")
        assert client.can_paginate("list_layers")
        assert client.can_paginate("list_event_source_mappings")


class TestServiceCoverageExpanded:
    """Test expanded service coverage."""

    @pytest.fixture
    def scanner(self):
        return AWSInventoryScanner()

    def test_total_service_count_expanded(self, scanner):
        """Test that we have significantly more services now."""
        paginated_east = set(scanner.paginated_services_east.keys())
        paginated = set(scanner.paginated_services.keys())
        non_paginated = set(scanner.non_paginated_services.keys())
        
        all_services = paginated_east | paginated | non_paginated
        
        # Should have at least 75 services now
        assert len(all_services) >= 75, \
            f"Expected at least 75 services, found {len(all_services)}"

    def test_no_duplicate_services_expanded(self, scanner):
        """Test no duplicates in expanded service list."""
        paginated_east = set(scanner.paginated_services_east.keys())
        paginated = set(scanner.paginated_services.keys())
        non_paginated = set(scanner.non_paginated_services.keys())
        
        east_paginated_overlap = paginated_east & paginated
        east_non_paginated_overlap = paginated_east & non_paginated
        paginated_non_paginated_overlap = paginated & non_paginated
        
        assert len(east_paginated_overlap) == 0
        assert len(east_non_paginated_overlap) == 0
        assert len(paginated_non_paginated_overlap) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
