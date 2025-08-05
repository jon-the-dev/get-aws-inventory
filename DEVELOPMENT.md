# Development Guide

## Setting up for Development

1. Clone the repository:
```bash
git clone https://github.com/jon-the-dev/aws-inventory-scanner.git
cd aws-inventory-scanner
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
```

4. Install development dependencies:
```bash
pip install build twine pytest black flake8
```

## Testing the Package

Test the CLI:
```bash
aws-inventory-scanner --help
```

Test with specific regions:
```bash
aws-inventory-scanner --region us-east-1 --verbose
```

## Building and Publishing

1. Build the package:
```bash
python -m build
```

2. Check the package:
```bash
python -m twine check dist/*
```

3. Upload to Test PyPI (recommended first):
```bash
python -m twine upload --repository testpypi dist/*
```

4. Test install from Test PyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ aws-inventory-scanner
```

5. Upload to PyPI:
```bash
python -m twine upload dist/*
```

## Package Structure

```
aws-inventory-scanner/
├── aws_inventory_scanner/
│   ├── __init__.py          # Package initialization
│   ├── scanner.py           # Main scanner class and CLI
│   └── cli.py              # CLI entry point
├── dist/                   # Built packages
├── setup.py               # Setup configuration
├── pyproject.toml         # Modern Python packaging config
├── requirements.txt       # Dependencies
├── README.md             # Package documentation
├── LICENSE               # MIT License
└── MANIFEST.in           # Package manifest
```

## Making Changes

1. Make your changes to the code
2. Update the version in `pyproject.toml` and `setup.py`
3. Update the changelog in `README.md`
4. Build and test the package
5. Upload to PyPI

## Version Management

Update version numbers in:
- `pyproject.toml`
- `setup.py`
- `aws_inventory_scanner/__init__.py`
