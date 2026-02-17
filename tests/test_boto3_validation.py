"""Test suite for AWS Inventory Scanner boto3 API calls."""

import pytest
import boto3
from botocore.exceptions import ClientError
from aws_inventory_scanner.scanner import AWSInventoryScanner


class TestBoto3APIValidation:
    """Validate that all boto3 API calls in scanner are valid."""

    @pytest.fixture
    def scanner(self):
        """Create scanner instance."""
        return AWSInventoryScanner()

    def test_paginated_services_east_valid(self, scanner):
        """Test that US-East-1 only services have valid boto3 methods."""
        for service, methods in scanner.paginated_services_east.items():
            client = boto3.client(service, region_name="us-east-1")
            for method_name, response_key in methods:
                # Verify method exists
                assert hasattr(client, method_name), \
                    f"Service '{service}' missing method '{method_name}'"
                
                # Verify paginator exists
                assert client.can_paginate(method_name), \
                    f"Service '{service}' method '{method_name}' cannot paginate"

    def test_paginated_services_valid(self, scanner):
        """Test that regional paginated services have valid boto3 methods."""
        for service, methods in scanner.paginated_services.items():
            client = boto3.client(service, region_name="us-east-1")
            for method_name, response_key in methods:
                # Verify method exists
                assert hasattr(client, method_name), \
                    f"Service '{service}' missing method '{method_name}'"
                
                # Verify paginator exists
                assert client.can_paginate(method_name), \
                    f"Service '{service}' method '{method_name}' cannot paginate"

    def test_non_paginated_services_valid(self, scanner):
        """Test that non-paginated services have valid boto3 methods."""
        for service, (method_name, response_key) in scanner.non_paginated_services.items():
            client = boto3.client(service, region_name="us-east-1")
            
            # Verify method exists
            assert hasattr(client, method_name), \
                f"Service '{service}' missing method '{method_name}'"

    def test_ai_ml_services_present(self, scanner):
        """Test that all AI/ML services are included."""
        ai_ml_services = [
            "bedrock",
            "bedrock-agent",
            "rekognition",
            "comprehend",
            "translate",
            "transcribe",
            "polly",
            "textract",
            "forecast",
            "personalize",
            "lexv2-models",
            "kendra",
        ]
        
        all_services = set(scanner.paginated_services.keys()) | set(scanner.non_paginated_services.keys())
        
        for service in ai_ml_services:
            assert service in all_services, \
                f"AI/ML service '{service}' not found in any service category"

    def test_bedrock_methods(self, scanner):
        """Test Bedrock service methods."""
        client = boto3.client("bedrock", region_name="us-east-1")
        
        assert hasattr(client, "list_foundation_models")
        assert hasattr(client, "list_model_customization_jobs")
        assert client.can_paginate("list_model_customization_jobs")

    def test_rekognition_methods(self, scanner):
        """Test Rekognition service methods."""
        client = boto3.client("rekognition", region_name="us-east-1")
        
        assert hasattr(client, "list_collections")
        assert hasattr(client, "list_stream_processors")
        assert client.can_paginate("list_collections")
        assert client.can_paginate("list_stream_processors")

    def test_comprehend_methods(self, scanner):
        """Test Comprehend service methods."""
        client = boto3.client("comprehend", region_name="us-east-1")
        
        assert hasattr(client, "list_document_classifiers")
        assert hasattr(client, "list_entities_detection_jobs")
        assert client.can_paginate("list_document_classifiers")
        assert client.can_paginate("list_entities_detection_jobs")

    def test_translate_methods(self, scanner):
        """Test Translate service methods."""
        client = boto3.client("translate", region_name="us-east-1")
        
        assert hasattr(client, "list_terminologies")
        # list_terminologies is non-paginated in this version

    def test_transcribe_methods(self, scanner):
        """Test Transcribe service methods."""
        client = boto3.client("transcribe", region_name="us-east-1")
        
        assert hasattr(client, "list_transcription_jobs")
        # list_transcription_jobs is non-paginated in this version

    def test_polly_methods(self, scanner):
        """Test Polly service methods."""
        client = boto3.client("polly", region_name="us-east-1")
        
        assert hasattr(client, "list_lexicons")
        assert client.can_paginate("list_lexicons")

    def test_textract_methods(self, scanner):
        """Test Textract service methods."""
        client = boto3.client("textract", region_name="us-east-1")
        
        assert hasattr(client, "list_adapters")
        assert client.can_paginate("list_adapters")

    def test_forecast_methods(self, scanner):
        """Test Forecast service methods."""
        client = boto3.client("forecast", region_name="us-east-1")
        
        assert hasattr(client, "list_datasets")
        assert hasattr(client, "list_predictors")
        assert client.can_paginate("list_datasets")
        assert client.can_paginate("list_predictors")

    def test_personalize_methods(self, scanner):
        """Test Personalize service methods."""
        client = boto3.client("personalize", region_name="us-east-1")
        
        assert hasattr(client, "list_datasets")
        assert hasattr(client, "list_solutions")
        assert client.can_paginate("list_datasets")
        assert client.can_paginate("list_solutions")

    def test_lexv2_methods(self, scanner):
        """Test Lex V2 service methods."""
        client = boto3.client("lexv2-models", region_name="us-east-1")
        
        assert hasattr(client, "list_bots")
        # list_bots is non-paginated in this version

    def test_kendra_methods(self, scanner):
        """Test Kendra service methods."""
        client = boto3.client("kendra", region_name="us-east-1")
        
        assert hasattr(client, "list_indices")
        # list_indices is non-paginated in this version

    def test_response_keys_match(self, scanner):
        """Test that response keys are valid for each service method."""
        # This test validates the structure but doesn't make actual API calls
        # Response key validation would require actual AWS credentials and resources
        
        all_services = {
            **{svc: methods for svc, methods in scanner.paginated_services_east.items()},
            **{svc: methods for svc, methods in scanner.paginated_services.items()},
        }
        
        for service, methods in all_services.items():
            for method_name, response_key in methods:
                # Verify response_key is a non-empty string
                assert isinstance(response_key, str), \
                    f"Service '{service}' method '{method_name}' has invalid response_key type"
                assert len(response_key) > 0, \
                    f"Service '{service}' method '{method_name}' has empty response_key"


class TestServiceCoverage:
    """Test service coverage and completeness."""

    @pytest.fixture
    def scanner(self):
        """Create scanner instance."""
        return AWSInventoryScanner()

    def test_total_service_count(self, scanner):
        """Test that we have expected number of services."""
        paginated_east = set(scanner.paginated_services_east.keys())
        paginated = set(scanner.paginated_services.keys())
        non_paginated = set(scanner.non_paginated_services.keys())
        
        # Count unique services
        all_services = paginated_east | paginated | non_paginated
        
        # Should have at least 36 services (25 original + 11 AI/ML)
        assert len(all_services) >= 36, \
            f"Expected at least 36 services, found {len(all_services)}"

    def test_ai_ml_service_count(self, scanner):
        """Test that all 12 AI/ML services are present."""
        ai_ml_services = {
            "bedrock", "bedrock-agent", "rekognition", "comprehend", "translate",
            "transcribe", "polly", "textract", "forecast",
            "personalize", "lexv2-models", "kendra"
        }
        
        all_services = set(scanner.paginated_services.keys()) | set(scanner.non_paginated_services.keys())
        found_ai_ml = ai_ml_services & all_services
        
        assert len(found_ai_ml) == 12, \
            f"Expected 12 AI/ML services, found {len(found_ai_ml)}: {found_ai_ml}"

    def test_no_duplicate_services(self, scanner):
        """Test that services aren't duplicated across categories."""
        paginated_east = set(scanner.paginated_services_east.keys())
        paginated = set(scanner.paginated_services.keys())
        non_paginated = set(scanner.non_paginated_services.keys())
        
        # Check for overlaps
        east_paginated_overlap = paginated_east & paginated
        east_non_paginated_overlap = paginated_east & non_paginated
        paginated_non_paginated_overlap = paginated & non_paginated
        
        assert len(east_paginated_overlap) == 0, \
            f"Services in both east and paginated: {east_paginated_overlap}"
        assert len(east_non_paginated_overlap) == 0, \
            f"Services in both east and non-paginated: {east_non_paginated_overlap}"
        assert len(paginated_non_paginated_overlap) == 0, \
            f"Services in both paginated and non-paginated: {paginated_non_paginated_overlap}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
