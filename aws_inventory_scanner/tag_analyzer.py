"""AWS Tag Analyzer - Extract and analyze tags from inventory data."""

import csv
import json
import logging
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class TagAnalyzer:
    """Analyzes tags from AWS inventory JSON files."""

    def __init__(self, inventory_dir="./inventory"):
        """Initialize the tag analyzer.

        Args:
            inventory_dir: Directory containing inventory JSON files.
        """
        self.inventory_dir = inventory_dir
        self.logger = logging.getLogger(__name__)

        # Tag key variations to look for
        self.tag_keys = [
            "Tags",
            "TagList",
            "tags",
            "TagSet",
            "TagSpecifications",
        ]

        # Common tag key patterns for compliance checking
        self.common_tag_patterns = {
            "name": ["Name", "name", "NAME"],
            "environment": ["Environment", "environment", "Env", "env"],
            "owner": ["Owner", "owner", "Team", "team"],
            "cost_center": [
                "CostCenter",
                "cost-center",
                "CostCentre",
                "BillingCode",
            ],
            "application": ["Application", "application", "App", "app"],
            "project": ["Project", "project"],
        }

    def extract_tags_from_resource(self, resource):
        """Extract tags from a single resource.

        Args:
            resource: Resource dictionary from AWS API response.

        Returns:
            List of tag dictionaries with 'Key' and 'Value'.
        """
        tags = []

        # Try different tag key variations
        for tag_key in self.tag_keys:
            if tag_key in resource:
                tag_data = resource[tag_key]

                # Handle list format: [{"Key": "Name", "Value": "MyResource"}]
                if isinstance(tag_data, list):
                    for tag in tag_data:
                        if isinstance(tag, dict):
                            # Standard format
                            if "Key" in tag and "Value" in tag:
                                tags.append(
                                    {"Key": tag["Key"], "Value": tag["Value"]}
                                )
                            # Alternative format (key/value lowercase)
                            elif "key" in tag and "value" in tag:
                                tags.append(
                                    {"Key": tag["key"], "Value": tag["value"]}
                                )

                # Handle dict format: {"Name": "MyResource"}
                elif isinstance(tag_data, dict):
                    for key, value in tag_data.items():
                        tags.append({"Key": key, "Value": str(value)})

                break  # Found tags, no need to check other keys

        return tags

    def get_resource_identifier(self, resource, service):
        """Get a human-readable identifier for a resource.

        Args:
            resource: Resource dictionary.
            service: AWS service name.

        Returns:
            String identifier for the resource.
        """
        # Common ID fields to check
        id_fields = [
            "ResourceId",
            "Id",
            "id",
            "ARN",
            "Arn",
            "arn",
            "Name",
            "name",
            # Service-specific fields
            "InstanceId",
            "VolumeId",
            "VpcId",
            "SubnetId",
            "GroupId",
            "BucketName",
            "DBInstanceIdentifier",
            "ClusterIdentifier",
            "FunctionName",
            "LoadBalancerName",
            "LoadBalancerArn",
            "QueueUrl",
            "TopicArn",
            "KeyId",
            "SecretId",
            "FileSystemId",
            "ClusterName",
            "RepositoryName",
        ]

        for field in id_fields:
            if field in resource:
                return str(resource[field])

        # If no standard field found, try to find any field ending with "Id"
        for key, value in resource.items():
            if key.endswith("Id") or key.endswith("ID"):
                return str(value)

        return "unknown"

    def extract_tags_from_file(self, file_path):
        """Extract tags from a single inventory JSON file.

        Args:
            file_path: Path to JSON inventory file.

        Returns:
            Dictionary containing extracted tag information.
        """
        result = {
            "file": file_path,
            "resources": [],
            "tags": [],
            "errors": [],
        }

        try:
            # Parse filename to get metadata
            filename = os.path.basename(file_path)
            parts = filename.replace(".json", "").split("-")

            if len(parts) < 5:
                result["errors"].append(
                    f"Invalid filename format: {filename}"
                )
                return result

            account_id = parts[0]
            service = parts[1]
            region = parts[2]
            method = parts[3]
            key = "-".join(parts[4:])

            # Read JSON file
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Handle both list and dict responses
            resources = data if isinstance(data, list) else [data]

            for resource in resources:
                if not isinstance(resource, dict):
                    continue

                resource_id = self.get_resource_identifier(resource, service)
                tags = self.extract_tags_from_resource(resource)

                resource_info = {
                    "account_id": account_id,
                    "service": service,
                    "region": region,
                    "method": method,
                    "resource_type": key,
                    "resource_id": resource_id,
                    "tags": tags,
                    "tag_count": len(tags),
                }

                result["resources"].append(resource_info)
                result["tags"].extend(
                    [
                        {
                            **resource_info,
                            "tag_key": tag["Key"],
                            "tag_value": tag["Value"],
                        }
                        for tag in tags
                    ]
                )

        except json.JSONDecodeError as e:
            result["errors"].append(f"JSON decode error: {e}")
        except Exception as e:
            result["errors"].append(f"Error processing file: {e}")

        return result

    def extract_tags_from_directory(self, directory=None):
        """Extract tags from all inventory files in a directory.

        Args:
            directory: Directory path. Uses self.inventory_dir if None.

        Returns:
            Dictionary with aggregated tag information.
        """
        if directory is None:
            directory = self.inventory_dir

        self.logger.info("Extracting tags from directory: %s", directory)

        all_tags = []
        all_resources = []
        errors = []

        # Find all JSON files
        json_files = list(Path(directory).glob("*.json"))
        self.logger.info("Found %d JSON files to process", len(json_files))

        for file_path in json_files:
            file_result = self.extract_tags_from_file(str(file_path))
            all_resources.extend(file_result["resources"])
            all_tags.extend(file_result["tags"])
            errors.extend(file_result["errors"])

        return {
            "resources": all_resources,
            "tags": all_tags,
            "errors": errors,
            "file_count": len(json_files),
        }

    def generate_tag_report(self, tags_data, output_dir=None):
        """Generate comprehensive tag report.

        Args:
            tags_data: Tag data from extract_tags_from_directory.
            output_dir: Directory to save reports. Uses inventory_dir if None.

        Returns:
            Dictionary with report file paths.
        """
        if output_dir is None:
            output_dir = self.inventory_dir

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_files = {}

        # Generate summary report
        summary = self._generate_summary(tags_data)
        summary_file = os.path.join(
            output_dir, f"tag-report-summary-{timestamp}.json"
        )
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str)
        report_files["summary"] = summary_file
        self.logger.info("Summary report saved to: %s", summary_file)

        # Generate detailed report
        detailed = self._generate_detailed_report(tags_data)
        detailed_file = os.path.join(
            output_dir, f"tag-report-detailed-{timestamp}.json"
        )
        with open(detailed_file, "w", encoding="utf-8") as f:
            json.dump(detailed, f, indent=2, default=str)
        report_files["detailed"] = detailed_file
        self.logger.info("Detailed report saved to: %s", detailed_file)

        # Generate CSV report
        csv_file = os.path.join(output_dir, f"tag-report-{timestamp}.csv")
        self._generate_csv_report(tags_data, csv_file)
        report_files["csv"] = csv_file
        self.logger.info("CSV report saved to: %s", csv_file)

        return report_files

    def _generate_summary(self, tags_data):
        """Generate summary statistics."""
        resources = tags_data["resources"]
        tags = tags_data["tags"]

        # Count resources with and without tags
        resources_with_tags = sum(1 for r in resources if r["tag_count"] > 0)
        resources_without_tags = len(resources) - resources_with_tags

        # Count tag key frequency
        tag_key_freq = defaultdict(int)
        tag_value_freq = defaultdict(lambda: defaultdict(int))

        for tag in tags:
            tag_key_freq[tag["tag_key"]] += 1
            tag_value_freq[tag["tag_key"]][tag["tag_value"]] += 1

        # Service breakdown
        service_breakdown = defaultdict(
            lambda: {"total": 0, "tagged": 0, "untagged": 0}
        )
        for resource in resources:
            service = resource["service"]
            service_breakdown[service]["total"] += 1
            if resource["tag_count"] > 0:
                service_breakdown[service]["tagged"] += 1
            else:
                service_breakdown[service]["untagged"] += 1

        return {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_resources": len(resources),
                "resources_with_tags": resources_with_tags,
                "resources_without_tags": resources_without_tags,
                "tag_coverage_percent": (
                    round(
                        (resources_with_tags / len(resources) * 100), 2
                    )
                    if len(resources) > 0
                    else 0
                ),
                "unique_tag_keys": len(tag_key_freq),
                "total_tag_entries": len(tags),
            },
            "tag_key_frequency": dict(
                sorted(
                    tag_key_freq.items(), key=lambda x: x[1], reverse=True
                )
            ),
            "top_tag_values": {
                key: dict(
                    sorted(
                        values.items(), key=lambda x: x[1], reverse=True
                    )[:10]
                )
                for key, values in sorted(
                    tag_value_freq.items(), key=lambda x: sum(x[1].values()),
                    reverse=True,
                )[:10]
            },
            "service_breakdown": dict(service_breakdown),
            "errors": tags_data.get("errors", []),
        }

    def _generate_detailed_report(self, tags_data):
        """Generate detailed tag analysis."""
        resources = tags_data["resources"]
        tags = tags_data["tags"]

        # Untagged resources
        untagged = [
            {
                "service": r["service"],
                "region": r["region"],
                "resource_type": r["resource_type"],
                "resource_id": r["resource_id"],
            }
            for r in resources
            if r["tag_count"] == 0
        ]

        # Tag inconsistencies (similar keys)
        tag_keys = set(tag["tag_key"] for tag in tags)
        inconsistencies = self._find_tag_inconsistencies(tag_keys)

        # Resources by tag
        resources_by_tag = defaultdict(list)
        for tag in tags:
            resources_by_tag[tag["tag_key"]].append(
                {
                    "service": tag["service"],
                    "region": tag["region"],
                    "resource_id": tag["resource_id"],
                    "value": tag["tag_value"],
                }
            )

        return {
            "generated_at": datetime.now().isoformat(),
            "untagged_resources": untagged,
            "untagged_count": len(untagged),
            "tag_inconsistencies": inconsistencies,
            "resources_by_tag_key": {
                key: {
                    "count": len(resources_list),
                    "unique_values": len(
                        set(r["value"] for r in resources_list)
                    ),
                    "sample_resources": resources_list[:5],
                }
                for key, resources_list in sorted(
                    resources_by_tag.items(), key=lambda x: len(x[1]),
                    reverse=True,
                )
            },
        }

    def _find_tag_inconsistencies(self, tag_keys):
        """Find similar tag keys that might be inconsistencies."""
        inconsistencies = []

        # Group by lowercase version
        lowercase_groups = defaultdict(set)
        for key in tag_keys:
            lowercase_groups[key.lower()].add(key)

        # Find groups with multiple variations
        for lowercase_key, variations in lowercase_groups.items():
            if len(variations) > 1:
                inconsistencies.append(
                    {
                        "similar_keys": sorted(list(variations)),
                        "recommendation": f"Standardize to one format",
                        "pattern": lowercase_key,
                    }
                )

        return inconsistencies

    def _generate_csv_report(self, tags_data, output_file):
        """Generate CSV report of all tags."""
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(
                [
                    "AccountID",
                    "Service",
                    "Region",
                    "ResourceType",
                    "ResourceID",
                    "TagKey",
                    "TagValue",
                ]
            )

            # Write tag data
            for tag in tags_data["tags"]:
                writer.writerow(
                    [
                        tag["account_id"],
                        tag["service"],
                        tag["region"],
                        tag["resource_type"],
                        tag["resource_id"],
                        tag["tag_key"],
                        tag["tag_value"],
                    ]
                )

    def find_missing_required_tags(self, tags_data, required_tags):
        """Find resources missing required tags.

        Args:
            tags_data: Tag data from extract_tags_from_directory.
            required_tags: List of required tag keys.

        Returns:
            List of resources missing required tags.
        """
        missing = []

        for resource in tags_data["resources"]:
            resource_tags = set(tag["Key"] for tag in resource["tags"])
            missing_tags = set(required_tags) - resource_tags

            if missing_tags:
                missing.append(
                    {
                        "service": resource["service"],
                        "region": resource["region"],
                        "resource_id": resource["resource_id"],
                        "missing_tags": sorted(list(missing_tags)),
                    }
                )

        return missing

    def generate_compliance_report(
        self, tags_data, required_tags, output_file=None
    ):
        """Generate tag compliance report.

        Args:
            tags_data: Tag data from extract_tags_from_directory.
            required_tags: List of required tag keys.
            output_file: Output file path. Auto-generated if None.

        Returns:
            Compliance report dictionary.
        """
        missing = self.find_missing_required_tags(tags_data, required_tags)

        total_resources = len(tags_data["resources"])
        compliant_resources = total_resources - len(missing)

        report = {
            "generated_at": datetime.now().isoformat(),
            "required_tags": required_tags,
            "total_resources": total_resources,
            "compliant_resources": compliant_resources,
            "non_compliant_resources": len(missing),
            "compliance_percentage": (
                round((compliant_resources / total_resources * 100), 2)
                if total_resources > 0
                else 0
            ),
            "non_compliant_details": missing,
        }

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, default=str)
            self.logger.info("Compliance report saved to: %s", output_file)

        return report
