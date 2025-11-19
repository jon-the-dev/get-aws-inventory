"""AWS Inventory Scanner - A tool to scan and inventory AWS resources across regions."""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .scanner import AWSInventoryScanner
from .tag_analyzer import TagAnalyzer

__all__ = ["AWSInventoryScanner", "TagAnalyzer"]
