from setuptools import setup
from pathlib import Path

setup(
    long_description=Path("README.rst").read_text(),
    long_description_content_type = "text/restructuredtext"
)
