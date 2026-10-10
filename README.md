# 📥 ReelSaver – Instagram Video & Audio Downloader

### 🚀 Simple Online Media Downloader Built with Python & Streamlit

**ReelSaver** is a user-friendly web application built with Python and Streamlit that helps users download supported Instagram Reels and video posts in video or audio format.

The application provides a clean, responsive interface with Dark Mode and Light Mode, Instagram URL validation, a compact media preview, and a result section with a download button.

---

# 🚀 Project Overview

ReelSaver provides a simple workflow for processing supported Instagram media links.

```text
Open ReelSaver
      ↓
Enter Instagram URL
      ↓
Choose Video or Audio
      ↓
Confirm Download Permission
      ↓
Fetch Media
      ↓
Preview Result
      ↓
Download File
```

---

# ✨ Features

- 🎬 Download supported Instagram Reels and video posts
- 🎵 Extract audio and convert it to MP3
- 🔗 Instagram URL input and validation
- 🎥 MP4 video download when a compatible format is available
- 🎧 Audio preview with an integrated audio player
- 🖼️ Compact, centered video preview
- 📥 Download the processed media file
- 📍 Automatic scrolling to the result section after successful processing
- 🌙 Dark Mode
- ☀️ Light Mode
- 🎨 Clean and user-friendly interface
- 📱 Responsive layout for desktop and mobile browsers
- 📦 File size validation
- 🐍 Python-based application
- 🧰 FFmpeg integration for MP3 conversion
- ☁️ Streamlit Community Cloud deployment support

**Note:** Download availability depends on Instagram access, content restrictions, compatible media formats, and the hosting environment. Not every Instagram URL is guaranteed to work.

---

# 🧠 How It Works

## 1️⃣ Open the Application

Open ReelSaver in your browser.

The application displays a simple interface where you can paste a supported Instagram Reel or video post URL.

## 2️⃣ Enter an Instagram URL

Paste the URL of the media you want to download.

Example:

```text
https://www.instagram.com/reel/REEL_ID/
```

The application validates the URL before attempting to retrieve the media.

## 3️⃣ Choose the Download Format

Select one of the available formats.

**Video Download**

```text
Instagram URL
      ↓
Select Video MP4
      ↓
Fetch Media
      ↓
Preview Video
      ↓
Download Video
```

**Audio Download**

```text
Instagram URL
      ↓
Select Audio MP3
      ↓
Fetch Audio
      ↓
Convert to MP3
      ↓
Preview Audio
      ↓
Download MP3
```

MP3 conversion requires FFmpeg.

## 4️⃣ Preview the Result

After successful processing, ReelSaver displays a result section containing:

- The video preview or audio player
- The generated filename
- The output file size
- A download button

The application automatically scrolls toward the result section after a successful download operation.

## 5️⃣ Download Your File

Click the download button to save the generated media file to your device.

The exact download behavior may depend on your browser and device.

---

# 🛠️ Technologies Used

## Programming Language

- Python

## User Interface

- Streamlit
- HTML
- CSS
- JavaScript

## Media Processing

- yt-dlp
- FFmpeg

## Python Libraries

- Streamlit
- yt-dlp
- Python Standard Library

## Version Control

- Git
- GitHub

## Deployment

- Streamlit Community Cloud

---

# 📁 Project Structure

```text
reelsaver-downloader/
│
├── app.py
│
├── requirements.txt
│
├── packages.txt
│
└── README.md
```

### File Description

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application, interface, URL validation, media processing, preview, and downloads |
| `requirements.txt` | Python dependencies required to run the application |
| `packages.txt` | System packages required for deployment, including FFmpeg |
| `README.md` | Project documentation and setup instructions |

This structure describes the main repository files. Additional files may be added as the project develops.

---

# 💻 Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/shekinapilla4809/reelsaver-downloader.git
```

## 2️⃣ Open the Project Folder

```bash
cd reelsaver-downloader
```

## 3️⃣ Create a Virtual Environment

Creating a virtual environment is recommended.

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

## 4️⃣ Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

## 5️⃣ Install FFmpeg

FFmpeg is required for audio extraction and MP3 conversion.

Verify your installation:

```bash
ffmpeg -version
```

If the command is not recognized, install FFmpeg and configure it in your system's PATH.

## 6️⃣ Run the Application

```bash
streamlit run app.py
```

The application normally opens in your default browser.

Local URL:

```text
http://localhost:8501
```

---

# 📦 Requirements

## `requirements.txt`

```text
streamlit
yt-dlp
```

These are the main Python dependencies used by the application.

## `packages.txt`

```text
ffmpeg
```

This file configures the FFmpeg system package for supported Streamlit Community Cloud deployments.

---

# 🎨 Theme Support

ReelSaver includes two interface themes.

### ☀️ Light Mode

A bright interface with clear text, readable controls, and a clean appearance.

### 🌙 Dark Mode

A dark interface designed for comfortable viewing.

Users can switch between themes using the theme selector in the application.

---

# 🎬 Video Download

The video workflow allows users to:

- Enter a supported Instagram URL
- Validate the URL
- Fetch available video media
- Preview the resulting file
- View the filename and file size
- Download the output

Video availability and compatibility depend on the source and the formats returned by yt-dlp.

---

# 🎵 Audio Download

The audio workflow allows users to:

- Enter a supported Instagram URL
- Select Audio MP3
- Extract the available audio
- Convert it to MP3 using FFmpeg
- Listen to the result
- Download the MP3 file

Audio extraction may fail if the source is inaccessible or Instagram restricts the request.

---

# 📍 Automatic Result Scrolling

ReelSaver includes an automatic result-scrolling feature.

After a successful media fetch:

1. The application stores the processed file in the current Streamlit session.
2. The result section displays the preview and file information.
3. The browser attempts to scroll smoothly to the result.
4. The user can preview or download the file.

Browser behavior and Streamlit rendering may affect scrolling in some environments.

---

# ☁️ Deployment

ReelSaver can be deployed using **Streamlit Community Cloud**, subject to the platform's current policies and resource limits.

## Deployment Steps

1. Push the project files to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in using your GitHub account.
4. Create a new app.
5. Select the `reelsaver-downloader` repository.
6. Select the `main` branch.
7. Set the main file path to `app.py`.
8. Click **Deploy**.

Ensure that `requirements.txt` and `packages.txt` are included in the repository.

### Hosting Considerations

Free hosting environments may impose limits on memory, execution time, temporary storage, and file sizes.

This application processes media using temporary files and holds the resulting file in Streamlit session state. Large downloads may exceed available resources, and temporary files may not persist between sessions or restarts.

Instagram may also restrict requests from cloud-hosted servers, so successful deployment does not guarantee that every URL can be processed.

---

# 🎯 Problem Statement

Downloading supported online media can be inconvenient when users need to work with command-line tools or separate applications.

A simple browser-based interface can make the workflow easier by combining URL validation, format selection, media preview, and file downloads in one place.

---

# 💡 Proposed Solution

ReelSaver provides a straightforward interface built with Python and Streamlit.

By integrating yt-dlp with FFmpeg, the application supports configured video downloads and audio extraction through a simple workflow.

The application focuses on usability, theme selection, responsive layout, compact previews, and convenient access to processed media.

---

# 🌟 Key Benefits

- Simple and user-friendly interface
- Video and audio options in one application
- Compact video preview
- Integrated audio player
- Automatic result scrolling
- Light and Dark themes
- File size validation
- Python-based implementation
- Straightforward local setup
- GitHub-based project management
- Optional cloud deployment

---

# 🔮 Future Enhancements

Potential future improvements include:

- 📋 Download history
- 📦 Batch URL processing
- 🎧 Additional audio formats
- 🎞️ Additional video formats
- 📊 Improved download progress reporting
- 📱 Further mobile interface improvements
- ⚙️ Advanced media settings
- ☁️ Configurable persistent storage
- 🧾 More detailed error messages
- 🧪 Automated testing

These are possible future enhancements and may not be available in the current version.

---

# ⚖️ Responsible Use

ReelSaver is intended for lawful media processing where downloading is permitted.

Users are responsible for complying with applicable laws, copyright requirements, Instagram's Terms of Use, and any permissions associated with the content they access.

Only download content you own, have permission to download, or are otherwise legally permitted to save.

Do not use the application to bypass access restrictions or download protected content without authorization.

ReelSaver is an independent project and is not affiliated with, endorsed by, or officially connected to Instagram or Meta.

---

# 👩‍💻 Developer

### Shekina Pilla

**B.Tech – Computer Science & Engineering (Data Science)**

### Areas of Interest

- Python Development
- Full Stack Development
- Artificial Intelligence
- Data Science
- Web Applications
- Cloud Applications

---

# 🙏 Acknowledgements

This project uses the following technologies:

- Python
- Streamlit
- yt-dlp
- FFmpeg
- HTML
- CSS
- JavaScript
- GitHub

Thanks to the developers and maintainers of these technologies.

---

# 📜 License

No specific license is declared for this project.

If you plan to distribute the application or allow others to reuse its source code, consider adding an appropriate `LICENSE` file and reviewing the licenses of its dependencies.

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ star on GitHub.

**GitHub Repository:**  
https://github.com/shekinapilla4809/reelsaver-downloader

Thank you for visiting **ReelSaver – Instagram Video & Audio Downloader!** 📥🎬🎵
