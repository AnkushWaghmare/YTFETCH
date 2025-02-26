<div align="center">

# 📥 YTFETCH

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/badge/downloads-1k%2Fmonth-brightgreen.svg)](https://github.com/yourusername/YTFETCH)

A powerful and flexible YouTube video downloader with multiple download options

</div>

## 🚀 Features

- 📹 Download single videos in various resolutions
- 🎵 Extract audio from videos
- 📑 Download entire playlists
- 📝 Batch download from text file
- 🔄 Concurrent downloads with threading/multiprocessing
- 🌐 Proxy support for restricted content

## 🛠️ Installation

Clone and install:
```bash
git clone https://github.com/AnkushWaghmare/YTFETCH.git
cd YTFETCH
python -m pip install --upgrade pip
python -m pip install -e .
```

## 💡 Usage

Basic video download:
```bash
ytfetch https://youtube.com/watch?v=VIDEO_ID
```

Download with specific resolution:
```bash
ytfetch -r 1080 https://youtube.com/watch?v=VIDEO_ID
```

Extract audio:
```bash
ytfetch -a https://youtube.com/watch?v=VIDEO_ID
```

Download Playlist:
```bash
ytfetch -p https://youtube.com/playlist?list=PLAYLIST_ID
```

Batch Download from File:
```bash
ytfetch -b videos.txt
```

Using Proxy:
```bash
ytfetch -x http://proxy.example.com:8080 https://youtube.com/watch?v=VIDEO_ID
```

## 📋 Command Options

| Option | Description |
|--------|-------------|
| `-r, --resolution` | Video resolution (e.g., 1080, 720, best) |
| `-f, --format` | Output format (mp4, webm, mp3) |
| `-a, --audio` | Extract audio only |
| `-p, --playlist` | Download full playlist |
| `-b, --batch` | Batch download from text file |
| `-x, --proxy` | Use proxy server |
| `-m, --multithreading` | Use multithreading for batch downloads |
| `-M, --multiprocessing` | Use multiprocessing for batch downloads |
| `--workers` | Number of worker threads/processes |

## 🎯 Examples

Download Best Quality:
```bash
ytfetch -r best https://youtube.com/watch?v=VIDEO_ID
```

Download MP3 Audio:
```bash
ytfetch -a -f mp3 https://youtube.com/watch?v=VIDEO_ID
```

Batch Download with 4 Workers:
```bash
ytfetch -b videos.txt -m --workers 4
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect YouTube's terms of service and content creators' rights.

## 📦 About

YTFETCH is a fast and versatile CLI YouTube downloader with support for video, audio, playlists, and parallel downloads. Built with Python and designed for efficiency and ease of use.

