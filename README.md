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

### Step 1: Clone the Repository
<div class="code-block">
<pre><code class="language-bash">git clone https://github.com/AnkushWaghmare/YTFETCH.git
cd YTFETCH</code></pre>
<button class="copy-button" onclick="copyCode(this)">📋</button>
</div>

### Step 2: Upgrade pip (Required)
<div class="code-block">
<pre><code class="language-bash">python -m pip install --upgrade pip</code></pre>
<button class="copy-button" onclick="copyCode(this)">📋</button>
</div>

### Step 3: Install Package
<div class="code-block">
<pre><code class="language-bash">python -m pip install -e .</code></pre>
<button class="copy-button" onclick="copyCode(this)">📋</button>
</div>

### Alternative: Install Dependencies Only
<div class="code-block">
<pre><code class="language-bash">python -m pip install -r requirements.txt</code></pre>
<button class="copy-button" onclick="copyCode(this)">📋</button>
</div>

## 💡 Usage

### Basic Video Download
<div class="code-block">
<pre><code class="language-bash">ytfetch https://youtube.com/watch?v=VIDEO_ID</code></pre>
<button class="copy-button" onclick="copyCode(this)">📋</button>
</div>

### Download with Specific Resolution
<div class="code-block">
<pre><code class="language-bash">ytfetch -r 1080 https://youtube.com/watch?v=VIDEO_ID</code></pre>
<button class="copy-button" onclick="copyCode(this)">Copy</button>
</div>

### Extract Audio Only
<div class="code-block">
<pre><code class="language-bash">ytfetch -a https://youtube.com/watch?v=VIDEO_ID</code></pre>
<button class="copy-button" onclick="copyCode(this)">Copy</button>
</div>

### Download Playlist
<div class="code-block">
<pre><code class="language-bash">ytfetch -p https://youtube.com/playlist?list=PLAYLIST_ID</code></pre>
<button class="copy-button" onclick="copyCode(this)">Copy</button>
</div>

### Batch Download from File
<div class="code-block">
<pre><code class="language-bash">ytfetch -b videos.txt</code></pre>
<button class="copy-button" onclick="copyCode(this)">Copy</button>
</div>

### Using Proxy
<div class="code-block">
<pre><code class="language-bash">ytfetch -x http://proxy.example.com:8080 https://youtube.com/watch?v=VIDEO_ID</code></pre>
<button class="copy-button" onclick="copyCode(this)">Copy</button>
</div>

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

### Download Best Quality
<div class="code-block">
<pre><code class="language-bash">ytfetch -r best https://youtube.com/watch?v=VIDEO_ID</code></pre>
<button class="copy-button" onclick="copyCode(this)">📋</button>
</div>

### Download MP3 Audio
<div class="code-block">
<pre><code class="language-bash">ytfetch -a -f mp3 https://youtube.com/watch?v=VIDEO_ID</code></pre>
<button class="copy-button" onclick="copyCode(this)">📋</button>
</div>

### Batch Download with 4 Workers
<div class="code-block">
<pre><code class="language-bash">ytfetch -b videos.txt -m --workers 4</code></pre>
<button class="copy-button" onclick="copyCode(this)">📋</button>
</div>

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect YouTube's terms of service and content creators' rights.

<style>
.code-block {
    position: relative;
    margin: 10px 0;
}

.copy-button {
    position: absolute;
    top: 5px;
    right: 5px;
    padding: 5px 8px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    opacity: 0.6;
    transition: opacity 0.2s;
    font-size: 14px;
}

.copy-button:hover {
    opacity: 1;
}

.copy-button.copied {
    background-color: #45a049;
}

pre {
    background-color: #f6f8fa;
    padding: 16px;
    border-radius: 6px;
    overflow: auto;
}
</style>

<script>
function copyCode(button) {
    const pre = button.parentElement.querySelector('pre');
    const code = pre.textContent;
    navigator.clipboard.writeText(code);
    
    button.textContent = '✓';
    button.classList.add('copied');
    setTimeout(() => {
        button.textContent = '📋';
        button.classList.remove('copied');
    }, 2000);
}
</script>

