import sys
import logging
from setuptools import setup, find_packages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    setup(
        name="ytfetch",
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
        description="YouTube Video Downloader CLI with multiple download options",
    )
except Exception as e:
    logger.error(f"Setup failed: {str(e)}")
    sys.exit(1)
