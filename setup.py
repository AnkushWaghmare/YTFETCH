import sys
import logging
from setuptools import setup, find_packages

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    setup(
        name="ytfetch",  # Changed to lowercase
        version="0.1.0",
        packages=find_packages(),
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
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        description="YouTube Video Downloader CLI with multiple download options",
    )
except Exception as e:
    logger.error(f"Setup failed: {str(e)}")
    sys.exit(1)
