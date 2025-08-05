# AWS Inventory Scanner Documentation

This directory contains the complete documentation for the AWS Inventory Scanner utility.

## Documentation Structure

- **`docs/`** - Main documentation content (Markdown files)
- **`mkdocs.yml`** - MkDocs configuration file
- **`requirements.txt`** - Python dependencies for building docs
- **`Pipfile`** & **`Pipfile.lock`** - Pipenv configuration

## Building the Documentation

### Prerequisites

Install the required dependencies:

```bash
cd docs
pip install -r requirements.txt
```

Or using Pipenv:

```bash
cd docs
pipenv install
pipenv shell
```

### Local Development

To serve the documentation locally with live reload:

```bash
mkdocs serve
```

The documentation will be available at `http://localhost:8000`

### Building Static Site

To build the static HTML documentation:

```bash
mkdocs build
```

The built site will be in the `site/` directory.

## Documentation Pages

1. **[Home](docs/index.md)** - Overview and introduction
2. **[Installation](docs/installation.md)** - Installation instructions and requirements
3. **[Usage](docs/usage.md)** - Command-line and Python API usage
4. **[Supported Services](docs/services.md)** - Detailed list of AWS services and resources
5. **[Complete Resource List](docs/resource-list.md)** - Comprehensive table of all resources
6. **[Output Format](docs/output.md)** - File structure and data processing
7. **[API Reference](docs/api.md)** - Python API documentation
8. **[Examples](docs/examples.md)** - Practical usage examples
9. **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## Contributing to Documentation

1. Edit the Markdown files in the `docs/` directory
2. Test changes locally with `mkdocs serve`
3. Ensure all links work and formatting is correct
4. Submit changes via pull request

## Documentation Features

- **Material Design** theme for modern appearance
- **Search functionality** for easy navigation
- **Code syntax highlighting** for examples
- **Responsive design** for mobile devices
- **Git revision dates** for tracking updates
- **Edit links** for easy contribution

## Customization

- **Theme settings**: Edit `mkdocs.yml` under the `theme` section
- **Custom CSS**: Add styles to `docs/stylesheets/extra.css`
- **Navigation**: Update the `nav` section in `mkdocs.yml`
- **Plugins**: Add or configure plugins in `mkdocs.yml`
