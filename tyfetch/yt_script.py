#!/usr/bin/env python3
import argparse
import concurrent.futures
import logging
import os
import time
import sys
from functools import partial
from typing import Optional, Dict, Any
import yt_dlp
import shutil
import subprocess

# Add this after existing imports
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser('~'), 'Desktop')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

class DownloadError(Exception):
    """Custom exception for download failures"""
    pass

def safe_file_read(file_path: str) -> str:
    """Safely read file contents with proper error handling"""
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except PermissionError:
        logger.error(f"Permission denied when accessing: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error reading file {file_path}: {str(e)}")
        raise

def progress_hook(d: Dict[str, Any]) -> None:
    """Enhanced progress hook with better error handling"""
    try:
        if d.get("status") == "downloading":
            filename = d.get("filename", "Unknown")
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            speed = d.get("speed", 0)
            
            if total:
                percent = (downloaded / total) * 100
                speed_mb = (speed or 0) / (1024 * 1024)  # Convert to MB/s
                logger.info(f"Downloading {filename}: {percent:.1f}% complete ({speed_mb:.1f} MB/s)")
            else:
                logger.info(f"Downloading {filename}: {downloaded/(1024*1024):.1f} MB downloaded")
        
        elif d.get("status") == "finished":
            logger.info(f"Download complete: {d.get('filename', 'Unknown')}")
        
        elif d.get("status") == "error":
            logger.error(f"Download error: {d.get('error', 'Unknown error')}")
    except Exception as e:
        logger.error(f"Progress hook error: {str(e)}")

def find_ffmpeg():
    """Find FFmpeg binary path"""
    try:
        # Check if ffmpeg is in PATH
        ffmpeg_path = shutil.which('ffmpeg')
        if ffmpeg_path:
            return ffmpeg_path
            
        # Mac-specific Homebrew paths first
        mac_paths = [
            '/opt/homebrew/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
        ]
        
        # Common FFmpeg locations
        common_locations = [
            *mac_paths,
            '/usr/bin/ffmpeg',
            'C:\\ffmpeg\\bin\\ffmpeg.exe',  # Windows
        ]
        
        for location in common_locations:
            if os.path.isfile(location):
                return location
                
        return None
    except Exception:
        return None

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    try:
        ffmpeg_path = find_ffmpeg()
        if not ffmpeg_path:
            # Detect OS for specific instructions
            if sys.platform == "darwin":  # macOS
                install_cmd = "brew install ffmpeg"
                if not shutil.which('brew'):
                    install_cmd = "First install Homebrew from https://brew.sh, then run: " + install_cmd
            elif sys.platform == "linux":
                install_cmd = "sudo apt-get install ffmpeg  # For Ubuntu/Debian\nsudo dnf install ffmpeg  # For Fedora"
            else:  # Windows
                install_cmd = "Download from https://ffmpeg.org/download.html"
            
            logger.error(f"""
FFmpeg is required but not found! 

Installation instructions for your system:
{install_cmd}

After installing, try running the command again.
""")
            return False, None
            
        result = subprocess.run([ffmpeg_path, '-version'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        if result.returncode == 0:
            logger.info("FFmpeg found at: " + ffmpeg_path)
            return True, ffmpeg_path
        return False, None
    except Exception as e:
        logger.error(f"FFmpeg check failed: {str(e)}")
        return False, None

def create_ydl_opts(
    resolution: str,
    output_format: str,
    extract_audio: bool,
    is_playlist: bool,
    proxy: Optional[str]
) -> Dict[str, Any]:
    """Create yt-dlp options with error handling"""
    try:
        output_template = os.path.join(DEFAULT_OUTPUT_DIR, '%(title)s.%(ext)s')
        has_ffmpeg, ffmpeg_path = check_ffmpeg()

        if not has_ffmpeg:
            raise DownloadError("Please install FFmpeg first and try again")

        common_opts = {
            "outtmpl": output_template,
            "quiet": True,
            "proxy": proxy,
            "progress_hooks": [progress_hook],
            "ffmpeg_location": ffmpeg_path,
        }

        if extract_audio:
            common_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": output_format,
                    "preferredquality": "192",
                }],
            })
            return common_opts

        # Video format selection
        video_format = (f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]"
                       if resolution.isdigit() else "bestvideo+bestaudio/best")

        common_opts.update({
            "format": video_format,
            "merge_output_format": output_format,
            "noplaylist": not is_playlist,
            "ignoreerrors": True,
        })

        return common_opts

    except Exception as e:
        logger.error(f"Error creating yt-dlp options: {str(e)}")
        raise

def download_with_retry(func, *args, retries: int = 3, **kwargs):
    """Generic retry decorator with exponential backoff"""
    for attempt in range(1, retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == retries:
                logger.error(f"Final attempt failed: {str(e)}")
                raise
            wait_time = min(2 ** attempt, 60)  # Cap wait time at 60 seconds
            logger.warning(f"Attempt {attempt} failed: {str(e)}. Retrying in {wait_time}s...")
            time.sleep(wait_time)

def download_video(
    url: str,
    resolution: str = "best",
    output_format: str = "mp4",
    extract_audio: bool = False,
    is_playlist: bool = False,
    proxy: Optional[str] = None,
) -> None:
    """Enhanced video download function with better error handling"""
    try:
        ydl_opts = create_ydl_opts(resolution, output_format, extract_audio, is_playlist, proxy)
        
        def _download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Starting download: {url}")
                ydl.download([url])

        download_with_retry(_download)
    except Exception as e:
        logger.error(f"Download failed for {url}: {str(e)}")
        raise DownloadError(f"Failed to download {url}: {str(e)}")

def batch_download(
    file_path: str,
    resolution: str,
    output_format: str,
    extract_audio: bool,
    proxy: Optional[str],
    use_processes: bool = False,
    workers: Optional[int] = None,
) -> None:
    """
    Batch download videos from a file containing one URL per line.
    Supports concurrent downloads using either threading or processing.
    """
    if not os.path.exists(file_path):
        logger.error("Batch file not found: %s", file_path)
        return

    with open(file_path, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        logger.error("No URLs found in %s", file_path)
        return

    # Choose the executor based on concurrency flag.
    ExecutorClass = concurrent.futures.ProcessPoolExecutor if use_processes else concurrent.futures.ThreadPoolExecutor

    # Set default worker count if not provided.
    if workers is None:
        workers = os.cpu_count() or 4

    mode = "processes" if use_processes else "threads"
    logger.info("Starting batch download with %d %s...", workers, mode)

    download_func = partial(
        download_video,
        resolution=resolution,
        output_format=output_format,
        extract_audio=extract_audio,
        is_playlist=False,
        proxy=proxy,
    )

    with ExecutorClass(max_workers=workers) as executor:
        future_to_url = {executor.submit(download_func, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
                logger.info("Completed download for: %s", url)
            except Exception as exc:
                logger.error("Download generated an exception for %s: %s", url, exc)


def download_playlist(
    playlist_url: str,
    resolution: str,
    output_format: str,
    extract_audio: bool,
    proxy: Optional[str],
    retries: int = 3,
) -> None:
    """
    Download an entire playlist.
    """
    download_video(
        url=playlist_url,
        resolution=resolution,
        output_format=output_format,
        extract_audio=extract_audio,
        is_playlist=True,
        proxy=proxy,
        retries=retries,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="""
╭─────────────────────────────────────────────────────╮
│         YTFETCH - YouTube Video Downloader          │
╰─────────────────────────────────────────────────────╯

A powerful CLI tool to download videos, playlists, and extract audio from YouTube.

Usage: ytfetch [OPTIONS] URL
       ytfetch -b [BATCH_FILE]""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=argparse.SUPPRESS
    )

    # URL argument
    parser._positionals.title = 'Arguments'
    parser.add_argument("url",
                       nargs="?",
                       metavar='URL',
                       help="YouTube video/playlist URL")

    # Optional arguments
    optional = parser._optionals
    optional.title = 'Options'
    
    # Basic options
    parser.add_argument("-v", "--version",
                       action="version",
                       version="YTFETCH 0.1.0",
                       help="Show version information")
    parser.add_argument("-a", "--audio",
                       action="store_true",
                       help="Extract audio only")
    parser.add_argument("-p", "--playlist",
                       action="store_true",
                       help="Download full playlist")

    # Options with parameters
    parser.add_argument("-r", "--resolution",
                       metavar=' ',
                       default="best",
                       help="Set video quality (1080, 720, best, max)")
    parser.add_argument("-f", "--format",
                       metavar=' ',
                       default="mp4",
                       help="Select format (mp4, webm, mp3)")
    parser.add_argument("-b", "--batch",
                       metavar=' ',
                       help="Batch download from text file")
    parser.add_argument("-x", "--proxy",
                       metavar=' ',
                       help="Use proxy server for downloads")
    
    # Processing options
    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument("-m", "--multithreading",
                         action="store_true",
                         help="Enable multithreading for batch downloads")
    me_group.add_argument("-M", "--multiprocessing",
                         action="store_true",
                         help="Enable multiprocessing for batch downloads")
    parser.add_argument("-w", "--workers",
                       type=int,
                       metavar=' ',
                       help="Number of parallel downloads (default: CPU count)")

    args = parser.parse_args()

    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    try:
        # Fix the use_processes variable definition
        use_processes = args.multiprocessing

        if args.batch:
            if not os.path.exists(args.batch):
                logger.error(f"Batch file not found: {args.batch}")
                sys.exit(1)
            batch_download(
                file_path=args.batch,
                resolution=args.resolution,
                output_format=args.format,
                extract_audio=args.audio,
                proxy=args.proxy,
                use_processes=use_processes,
                workers=args.workers,
            )
        elif args.url:
            if args.playlist:
                download_playlist(
                    playlist_url=args.url,
                    resolution=args.resolution,
                    output_format=args.format,
                    extract_audio=args.audio,
                    proxy=args.proxy,
                )
            else:
                download_video(
                    url=args.url,
                    resolution=args.resolution,
                    output_format=args.format,
                    extract_audio=args.audio,
                    is_playlist=False,
                    proxy=args.proxy,
                )
        else:
            parser.print_help()
            sys.exit(0)
    except KeyboardInterrupt:
        logger.info("\nDownload interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
#this is the end of the script