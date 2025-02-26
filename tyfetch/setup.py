import sys
import logging
from setuptools import setup, find_packages

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def read_file(filename):
    """Safely read file contents with error handling"""
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        logger.error(f"Required file {filename} not found")
        sys.exit(1)
    except PermissionError:
        logger.error(f"Permission denied when accessing {filename}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error reading {filename}: {str(e)}")
        sys.exit(1)

try:
    long_description = read_file("README.md")

    setup(
        name="TYFETCH",
        version="0.1.0",
        packages=find_packages(exclude=['tests*']),
        install_requires=[
            "yt-dlp>=2023.0.0",
            "requests>=2.25.0",
        ],
        entry_points={
            "console_scripts": [
                "ytfetch = tyfetch.yt_script:main",
            ]
        },
        python_requires=">=3.6",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: End Users/Desktop",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        description="YouTube Video Downloader CLI with multiple download options",
    )
except Exception as e:
    logger.error(f"Setup failed: {str(e)}")
    sys.exit(1)