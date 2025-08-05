#!/bin/bash

# Script to upload AWS Inventory Scanner to PyPI

set -e

echo "Building package..."
python -m build

echo "Checking package with twine..."
python -m twine check dist/*

echo "Package is ready for upload!"
echo ""
echo "To upload to Test PyPI (recommended first):"
echo "python -m twine upload --repository testpypi dist/*"
echo ""
echo "To upload to PyPI:"
echo "python -m twine upload dist/*"
echo ""
echo "Note: You'll need to create accounts on PyPI and TestPyPI first:"
echo "- PyPI: https://pypi.org/account/register/"
echo "- TestPyPI: https://test.pypi.org/account/register/"
