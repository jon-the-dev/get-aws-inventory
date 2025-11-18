# CLAUDE.md - AI Assistant Development Guide

This document provides comprehensive guidance for AI assistants (like Claude) working on the AWS Inventory Scanner codebase. It covers the project structure, conventions, workflows, and best practices.

## Project Overview

**AWS Inventory Scanner** is a Python-based CLI tool that scans and inventories AWS resources across all regions in an AWS account. It uses boto3 to interact with AWS APIs, supports 25+ AWS services, and outputs structured JSON files for each service/region combination.

### Key Characteristics

- **Language**: Python 3.8+
- **Main Dependencies**: boto3, botocore
- **Distribution**: Published to PyPI as `aws-inventory-scanner`
- **Architecture**: Multi-threaded concurrent processing
- **Output**: JSON files per service/region
- **Documentation**: MkDocs-based static site

## Repository Structure

```
aws-inventory-scanner/
├── aws_inventory_scanner/           # Main package directory
│   ├── __init__.py                 # Package initialization, exports AWSInventoryScanner
│   ├── scanner.py                  # Core scanner logic and CLI entry point
│   └── cli.py                      # CLI wrapper (imports main from scanner.py)
├── docs/                           # MkDocs documentation
│   ├── index.md                    # Documentation home page
│   ├── installation.md             # Installation instructions
│   ├── usage.md                    # Usage examples and CLI reference
│   ├── services.md                 # List of supported AWS services
│   ├── output.md                   # Output format documentation
│   ├── api.md                      # Python API reference
│   ├── examples.md                 # Example use cases
│   ├── troubleshooting.md          # Common issues and solutions
│   └── stylesheets/                # Custom CSS for docs
├── .github/                        # GitHub-specific files
│   ├── workflows/                  # GitHub Actions workflows
│   │   ├── ci.yml                 # MkDocs deployment workflow
│   │   ├── dependabot-auto-merge.yml
│   │   ├── review-bot.yml
│   │   ├── stale.yml
│   │   └── cron-update-pre-commit.yml
│   ├── ISSUE_TEMPLATE/            # Issue templates
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml             # Dependabot configuration
├── pyproject.toml                  # Modern Python packaging configuration
├── requirements.txt                # Package dependencies
├── mkdocs.yml                      # MkDocs configuration
├── .pre-commit-config.yaml         # Pre-commit hooks configuration
├── .gitignore                      # Git ignore patterns
├── CODEOWNERS                      # Code ownership (@jon-the-dev)
├── LICENSE                         # MIT License
├── README.md                       # Main project README
├── DEVELOPMENT.md                  # Development workflow guide
├── MANIFEST.in                     # Package manifest
└── upload_to_pypi.sh              # PyPI upload script
```

## Core Components

### 1. scanner.py (lines 1-412)

The main module containing all core functionality:

#### AWSInventoryScanner Class (lines 17-354)

**Constructor** (`__init__`, lines 20-165):
- Parameters: `regions`, `output_dir`, `workers`
- Sets up boto3 Config with timeouts and retries
- Defines service definitions in three categories:
  - `paginated_services_east`: IAM, Route53 domains (us-east-1 only)
  - `paginated_services`: Regional services with pagination support
  - `non_paginated_services`: Services requiring manual pagination

**Key Methods**:
- `get_all_regions()` (lines 167-175): Retrieves all AWS regions using EC2 API
- `paginate_and_collect()` (lines 177-186): Uses boto3 paginators to collect resources
- `handle_non_paginated_service()` (lines 188-214): Manually handles pagination with NextToken
- `write_to_file()` (lines 216-225): Writes JSON output with error handling fallback to .txt
- `process_service_region()` (lines 227-268): Core worker function for scanning a service in a region
- `scan()` (lines 270-353): Main orchestration method using ThreadPoolExecutor

#### CLI Function (lines 356-411)

- Uses argparse for command-line argument parsing
- Supports: `--region`, `--profile`, `--output-dir`, `--workers`, `--verbose`
- Entry point: `main()` function

### 2. __init__.py (lines 1-9)

- Exports `AWSInventoryScanner` class
- Defines package metadata: `__version__`, `__author__`, `__email__`

### 3. cli.py (lines 1-6)

- Simple wrapper that imports and calls `main()` from scanner.py
- Used as entry point in pyproject.toml

## Code Conventions

### Style Guidelines

1. **Line Length**: Maximum 80 characters (enforced by pylint in pre-commit)
2. **Docstrings**: Use triple-quoted docstrings for classes and functions
3. **Formatting**: Managed by prettier and pre-commit hooks
4. **Imports**: Follow standard Python import ordering (stdlib, third-party, local)
5. **Error Handling**:
   - Use specific exception types (e.g., `botocore.exceptions.ClientError`)
   - Log errors at DEBUG level for API failures
   - Graceful degradation (continue scanning other services on failure)

### Naming Conventions

- **Classes**: PascalCase (e.g., `AWSInventoryScanner`)
- **Functions/Methods**: snake_case (e.g., `get_all_regions`, `process_service_region`)
- **Variables**: snake_case (e.g., `aws_acct_id`, `output_dir`)
- **Constants**: Not used extensively, but would be UPPER_SNAKE_CASE
- **Private methods**: Leading underscore (not used in this codebase currently)

### Logging

- Use the `logging` module with logger instances
- Log levels:
  - `INFO`: Progress updates, resource counts, completion messages
  - `DEBUG`: Detailed operation info, API errors
- Verbose mode controlled by `--verbose` flag

### Configuration Management

- Boto3 Config object (scanner.py:32-36):
  - `connect_timeout=5`
  - `max_pool_connections=100`
  - `retries={"max_attempts": 5, "mode": "adaptive"}`

## Development Workflow

### Initial Setup

```bash
# Clone repository
git clone https://github.com/jon-the-dev/aws-inventory-scanner.git
cd aws-inventory-scanner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install build twine pytest black flake8
```

### Pre-commit Hooks

The project uses extensive pre-commit hooks (`.pre-commit-config.yaml`):

- **Formatting**: prettier
- **File checks**: executables, large files, merge conflicts, YAML syntax, private keys
- **Markdown**: markdownlint with auto-fix
- **Terraform**: fmt, docs, validate, tflint, tfsec (for infrastructure code)
- **GitHub Actions**: JSON schema validation
- **Shell scripts**: shellcheck
- **Python**: pylint with max line length 80

Install pre-commit hooks:
```bash
pre-commit install
```

Run manually:
```bash
pre-commit run --all-files
```

### Testing

```bash
# Test CLI
aws-inventory-scanner --help

# Test with specific region
aws-inventory-scanner --region us-east-1 --verbose

# Test with profile
aws-inventory-scanner --profile my-aws-profile --region us-east-1
```

Note: There's currently no automated test suite (pytest tests should be added).

### Building and Publishing

```bash
# 1. Update version in:
#    - pyproject.toml (line 7)
#    - aws_inventory_scanner/__init__.py (line 3)
#    - Update CHANGELOG in README.md

# 2. Build the package
python -m build

# 3. Check the package
python -m twine check dist/*

# 4. Upload to Test PyPI (recommended first)
python -m twine upload --repository testpypi dist/*

# 5. Test install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ aws-inventory-scanner

# 6. Upload to PyPI
python -m twine upload dist/*
# OR use the script:
./upload_to_pypi.sh
```

### Documentation

Documentation is built with MkDocs Material theme:

```bash
# Install documentation dependencies
pip install mkdocs mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-video

# Serve locally
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages (done automatically by CI on main branch push)
mkdocs gh-deploy --force
```

## Adding New AWS Services

To add support for a new AWS service:

### Step 1: Identify Service Category

Determine if the service supports boto3 paginators:
```python
import boto3
client = boto3.client('service-name', region_name='us-east-1')
print(client.can_paginate('method_name'))
```

### Step 2: Add to Appropriate Dictionary

**For paginated services** (scanner.py:56-153):
```python
self.paginated_services = {
    # ... existing services ...
    "new-service": [
        ("list_method_name", "ResponseKey"),
        ("describe_method_name", "ItemsKey"),
    ],
}
```

**For us-east-1 only services** (scanner.py:47-54):
```python
self.paginated_services_east = {
    # ... existing services ...
    "new-global-service": [("list_items", "Items")],
}
```

**For non-paginated services** (scanner.py:155-165):
```python
self.non_paginated_services = {
    # ... existing services ...
    "new-service": ("get_method", "ResponseKey"),
}
```

### Step 3: Test the New Service

```bash
aws-inventory-scanner --region us-east-1 --verbose
```

Check the output directory for files matching pattern:
```
{account_id}-{service}-{region}-{method}-{key}.json
```

### Step 4: Update Documentation

Update `docs/services.md` with the new service in the appropriate category.

## Common File Patterns

### Output Files

Format: `{account_id}-{service}-{region}-{method}-{key}.json`

Example:
```
123456789012-ec2-us-east-1-describe_instances-Reservations.json
123456789012-s3-us-east-1-list_buckets-Buckets.json
123456789012-rds-us-west-2-describe_db_instances-DBInstances.json
```

### Skip Existing Files

The scanner skips existing files (scanner.py:232-234):
```python
if os.path.exists(file_name):
    self.logger.debug("%s already exists. Skipping.", file_name)
    return f"{file_name} already exists. Skipping."
```

## Key Technical Details

### Threading Model

- Uses `concurrent.futures.ThreadPoolExecutor`
- Default workers: 35 (configurable via `--workers`)
- Each task processes one service/method/region combination
- Progress logged every 10 completed tasks

### AWS Credentials

The scanner uses a two-step credential approach:
1. Creates a boto3 Session (optionally with profile)
2. Calls `sts.get_session_token()` to get temporary credentials
3. Uses temporary credentials for all API calls

This ensures consistent credentials across all threads and regions.

### Error Handling Philosophy

- **Fail gracefully**: Don't stop the entire scan if one service/region fails
- **Log and continue**: Log errors at DEBUG level and move to next task
- **Fallback on write**: If JSON serialization fails, write to .txt file

## GitHub Workflows

### ci.yml - Documentation Deployment

- **Trigger**: Push to main branch
- **Purpose**: Deploy MkDocs documentation to GitHub Pages
- **Steps**:
  1. Checkout code
  2. Setup Python 3.x
  3. Install mkdocs-material and plugins
  4. Run `mkdocs gh-deploy --force`

### Other Workflows

- **dependabot-auto-merge.yml**: Auto-merge Dependabot PRs
- **review-bot.yml**: Automated PR reviews
- **stale.yml**: Mark and close stale issues
- **cron-update-pre-commit.yml**: Keep pre-commit hooks updated

## Best Practices for AI Assistants

### When Making Changes

1. **Read before modifying**: Always read the full file before making edits
2. **Preserve structure**: Maintain the existing code organization and patterns
3. **Update all version locations**: pyproject.toml, __init__.py, README.md changelog
4. **Test changes**: Verify changes work with `pip install -e .` and test CLI
5. **Update documentation**: Modify relevant docs/ files if adding features
6. **Follow conventions**: Match existing naming, logging, and error handling patterns

### When Adding Features

1. **Check existing patterns**: See how similar features are implemented
2. **Maintain backward compatibility**: Don't break existing CLI arguments or API
3. **Add CLI arguments**: Update argparse in scanner.py:main()
4. **Document**: Update README.md, DEVELOPMENT.md, and relevant docs/ files
5. **Consider threading**: Ensure new code is thread-safe for concurrent execution

### When Fixing Bugs

1. **Understand the flow**: Trace execution through scan() → process_service_region()
2. **Check error logs**: Look at DEBUG level logging for API errors
3. **Test with verbose mode**: Use `--verbose` flag to see detailed output
4. **Verify across services**: Test with multiple services/regions if applicable

### When Refactoring

1. **Maintain the public API**: Don't change AWSInventoryScanner constructor or scan() method signature
2. **Keep CLI compatible**: Preserve all existing command-line arguments
3. **Update docstrings**: Ensure documentation matches new implementation
4. **Consider performance**: Maintain or improve scanning speed (threading model)

## Common Commands Reference

```bash
# Development
pip install -e .                    # Install in development mode
aws-inventory-scanner --help        # Show CLI help
python -m aws_inventory_scanner.scanner  # Run directly

# Testing
aws-inventory-scanner --region us-east-1 --verbose
aws-inventory-scanner --profile dev-account --output-dir ./test-output

# Code Quality
pre-commit run --all-files         # Run all pre-commit hooks
pylint aws_inventory_scanner/       # Run pylint directly

# Documentation
mkdocs serve                        # Serve docs locally
mkdocs build                        # Build docs
mkdocs gh-deploy                    # Deploy to GitHub Pages

# Building/Publishing
python -m build                     # Build distribution packages
python -m twine check dist/*        # Validate distribution
python -m twine upload --repository testpypi dist/*  # Upload to Test PyPI
python -m twine upload dist/*       # Upload to PyPI
```

## Important Files to Update When...

### Adding a New Service
- `aws_inventory_scanner/scanner.py` - Add to service dictionaries
- `docs/services.md` - Document the new service
- `README.md` - Update supported services list if major service

### Changing Version
- `pyproject.toml` - Line 7: version = "x.y.z"
- `aws_inventory_scanner/__init__.py` - Line 3: __version__ = "x.y.z"
- `README.md` - Add entry to Changelog section

### Modifying CLI Arguments
- `aws_inventory_scanner/scanner.py` - Update main() function argparse
- `docs/usage.md` - Document new CLI arguments
- `README.md` - Update usage examples

### Changing Dependencies
- `requirements.txt` - Add/update dependency
- `pyproject.toml` - Update dependencies array (lines 33-36)
- Test with clean virtual environment

### Updating Documentation
- `docs/*.md` - Edit relevant documentation files
- `mkdocs.yml` - Add new pages to nav if needed
- Test locally with `mkdocs serve`

## AWS IAM Permissions Required

The scanner requires read-only permissions. Recommended policies:
- **ReadOnlyAccess** (AWS managed policy) - Broadest access
- **Custom policy** - Specific read permissions for each service

Minimum permissions pattern:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "s3:List*",
        "rds:Describe*",
        "lambda:List*",
        // ... etc for each service
      ],
      "Resource": "*"
    }
  ]
}
```

## Troubleshooting for AI Assistants

### Issue: Import errors after changes
**Solution**: Reinstall in development mode: `pip install -e .`

### Issue: CLI not found
**Solution**: Check entry point in pyproject.toml line 45, reinstall package

### Issue: Service not being scanned
**Solution**: Check service is in correct dictionary (paginated vs non-paginated), verify method name and response key

### Issue: Permission errors during scan
**Solution**: Verify AWS credentials have read permissions for the service, check CloudTrail for AccessDenied events

### Issue: Output files not created
**Solution**: Check output_dir exists and is writable, verify no existing files (scanner skips existing)

## Code Ownership

- **Primary maintainer**: @jon-the-dev (see CODEOWNERS file)
- All changes should be reviewed by code owner
- Follow existing patterns and conventions established by maintainer

## License

This project is licensed under the MIT License. All contributions must be compatible with MIT licensing.

---

**Last Updated**: 2025-11-18
**Version**: 0.1.0
**Python Version**: 3.8+
**Boto3 Version**: >=1.26.0
