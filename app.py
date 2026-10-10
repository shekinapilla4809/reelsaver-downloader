
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

import streamlit as st
import streamlit.components.v1 as components
import yt_dlp


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="ReelSaver | Video & Audio Downloader",
    page_icon="📥",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =====================================================
# CONSTANTS
# =====================================================
MAX_FILE_SIZE = 100 * 1024 * 1024
ALLOWED_HOSTS = {"instagram.com", "www.instagram.com"}


# =====================================================
# SESSION STATE
# =====================================================
defaults = {
    "theme": "Dark",
    "media_bytes": None,
    "media_filename": None,
    "media_type": None,
    "result_ready": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# THEME
# =====================================================
dark = st.session_state.theme == "Dark"

if dark:
    BG = "#0B1020"
    CARD = "#151C2E"
    INPUT_BG = "#0E1628"
    TEXT = "#F5F7FF"
    MUTED = "#A6B0C3"
    BORDER = "#29344B"
    ACCENT = "#C13584"
else:
    BG = "#F4F6FB"
    CARD = "#FFFFFF"
    INPUT_BG = "#FFFFFF"
    TEXT = "#172033"
    MUTED = "#64748B"
    BORDER = "#DCE3EF"
    ACCENT = "#B52B79"


# =====================================================
# CSS
# =====================================================
st.markdown(
    f"""
    <style>
    :root {{
        color-scheme: {"dark" if dark else "light"};
    }}

    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    .block-container {{
        max-width: 720px;
        padding: 1rem 1rem 2rem;
    }}

    h1, h2, h3, h4, p, label {{
        color: {TEXT};
    }}

    .brand {{
        font-size: 23px;
        font-weight: 800;
        letter-spacing: -0.6px;
        padding-top: 5px;
    }}

    .hero {{
        text-align: center;
        padding: 22px 6px 18px;
    }}

    .hero h1 {{
        color: {TEXT};
        font-size: clamp(25px, 5vw, 35px);
        line-height: 1.25;
        margin-bottom: 10px;
    }}

    .hero p {{
        color: {MUTED};
        font-size: 14px;
        line-height: 1.7;
    }}

    .accent {{
        color: {ACCENT};
    }}

    .panel {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 15px;
        padding: 16px;
        margin: 10px 0;
    }}

    .panel h3 {{
        margin-top: 0;
        margin-bottom: 7px;
    }}

    .muted {{
        color: {MUTED};
        font-size: 13px;
        line-height: 1.6;
    }}

    .result-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 17px;
        margin-top: 12px;
        margin-bottom: 12px;
    }}

    .ready-label {{
        color: #16A36A;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .file-name {{
        color: {TEXT};
        font-size: 14px;
        font-weight: 600;
        overflow-wrap: anywhere;
        margin-top: 10px;
    }}

    .stTextInput input {{
        background: {INPUT_BG};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 10px;
        min-height: 44px;
    }}

    .stButton button,
    .stDownloadButton button,
    .stFormSubmitButton button {{
        border-radius: 10px;
        min-height: 44px;
        font-weight: 600;
    }}

    .stButton button[kind="primary"],
    .stDownloadButton button[kind="primary"],
    .stFormSubmitButton button[kind="primary"] {{
        background: {ACCENT};
        border-color: {ACCENT};
        color: #FFFFFF;
    }}

    /* Compact centered video preview */
    div[data-testid="stVideo"] {{
        width: 100% !important;
        max-width: 200px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        overflow: hidden;
        border-radius: 12px;
    }}

    div[data-testid="stVideo"] video {{
        width: 100% !important;
        max-width: 200px !important;
        max-height: 300px !important;
        object-fit: contain;
        display: block;
        margin: 0 auto;
        border-radius: 12px;
    }}

    div[data-testid="stAudio"] {{
        max-width: 360px;
        margin: 10px auto;
    }}

    div[data-testid="stAlert"] {{
        border-radius: 10px;
    }}

    .footer {{
        text-align: center;
        color: {MUTED};
        font-size: 12px;
        line-height: 1.8;
        padding-top: 15px;
    }}

    @media (max-width: 600px) {{
        .block-container {{
            padding: 0.6rem 0.65rem 1.5rem;
        }}

        .panel, .result-card {{
            padding: 13px;
            border-radius: 12px;
        }}

        .hero {{
            padding: 18px 3px 14px;
        }}

        div[data-testid="stVideo"] {{
            max-width: 175px !important;
        }}

        div[data-testid="stVideo"] video {{
            max-width: 175px !important;
            max-height: 250px !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# URL VALIDATION
# =====================================================
def validate_url(raw_url: str) -> str:
    raw_url = raw_url.strip()

    if not raw_url:
        raise ValueError("Please paste an Instagram link first.")

    if len(raw_url) > 2048:
        raise ValueError("The link is too long.")

    try:
        parsed = urlsplit(raw_url)
        hostname = (parsed.hostname or "").lower()
        port = parsed.port
    except ValueError:
        raise ValueError("Please enter a valid URL.")

    if parsed.scheme.lower() != "https":
        raise ValueError("Please enter a valid HTTPS Instagram link.")

    if hostname not in ALLOWED_HOSTS:
        raise ValueError("Please enter a valid Instagram link.")

    if parsed.username or parsed.password:
        raise ValueError("URLs containing login credentials are not allowed.")

    if port not in (None, 443):
        raise ValueError("Invalid URL port.")

    match = re.fullmatch(
        r"/(reel|reels|p|tv)/([A-Za-z0-9_-]+)/?",
        parsed.path,
    )

    if not match:
        raise ValueError(
            "Please paste a valid Instagram Reel or video post link."
        )

    return (
        f"https://www.instagram.com/"
        f"{match.group(1)}/{match.group(2)}/"
    )


# =====================================================
# DOWNLOAD / CONVERT MEDIA
# =====================================================
def fetch_media(url: str, media_type: str):
    with tempfile.TemporaryDirectory(prefix="reelsaver_") as folder:
        folder_path = Path(folder)
        output_template = str(folder_path / "media.%(ext)s")

        options = {
            "outtmpl": output_template,
            "noplaylist": True,
            "max_filesize": MAX_FILE_SIZE,
            "socket_timeout": 20,
            "retries": 2,
            "quiet": True,
            "no_warnings": True,
            "cachedir": False,
        }

        if media_type == "Audio MP3":
            if not shutil.which("ffmpeg"):
                raise RuntimeError(
                    "FFmpeg is required for MP3 conversion. "
                    "Install FFmpeg and restart the app."
                )

            options.update({
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            })
        else:
            options["format"] = "best[ext=mp4]/best"

        with yt_dlp.YoutubeDL(options) as downloader:
            info = downloader.extract_info(url, download=True)

        if not info:
            raise RuntimeError("No media information was returned.")

        allowed_extensions = {".mp4", ".webm", ".mkv", ".mp3"}

        candidates = [
            file_path
            for file_path in folder_path.glob("media.*")
            if file_path.is_file()
            and file_path.suffix.lower() in allowed_extensions
            and not file_path.name.endswith(".part")
        ]

        if media_type == "Audio MP3":
            candidates = [
                file_path
                for file_path in candidates
                if file_path.suffix.lower() == ".mp3"
            ]

        if not candidates:
            raise RuntimeError("The media file could not be created.")

        media_path = max(candidates, key=lambda p: p.stat().st_mtime)
        size = media_path.stat().st_size

        if size == 0:
            raise RuntimeError("The downloaded media file is empty.")

        if size > MAX_FILE_SIZE:
            raise RuntimeError(
                "The downloaded file exceeds the 100 MB size limit."
            )

        data = media_path.read_bytes()

        title = str(info.get("title") or "instagram_media")
        safe_title = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            title,
        ).strip("_")[:60] or "instagram_media"

        filename = safe_title + media_path.suffix.lower()

        return data, filename


# =====================================================
# HEADER + THEME SELECTOR
# =====================================================
left, right = st.columns([3, 1])

with left:
    st.markdown(
        '<div class="brand">📥 <span class="accent">'
        'Reel</span>Saver</div>',
        unsafe_allow_html=True,
    )

with right:
    selected_theme = st.selectbox(
        "Theme",
        ["Dark", "Light"],
        index=0 if dark else 1,
        key="theme_selector",
        label_visibility="collapsed",
    )

if selected_theme != st.session_state.theme:
    st.session_state.theme = selected_theme
    st.rerun()


# =====================================================
# HERO SECTION
# =====================================================
st.markdown(
    """
    <div class="hero">
        <h1>Instagram Video & Audio Downloader</h1>
        <p>
            Download eligible videos and audio in a few simple steps.
            <br>Simple, fast and mobile-friendly.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# INPUT PANEL
# =====================================================
st.markdown(
    """
    <div class="panel">
        <h3>Paste your link</h3>
        <p class="muted">
            Copy a public Instagram Reel or video post link.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("media_form"):
    url_input = st.text_input(
        "Instagram URL",
        placeholder="https://www.instagram.com/reel/...",
        max_chars=2048,
        label_visibility="collapsed",
    )

    media_type = st.radio(
        "Download format",
        ["Video MP4", "Audio MP3"],
        horizontal=True,
    )

    permission = st.checkbox(
        "I own this content or have permission to download it."
    )

    submitted = st.form_submit_button(
        "Fetch Media →",
        type="primary",
        use_container_width=True,
    )


# =====================================================
# PROCESS REQUEST
# =====================================================
if submitted:
    # Clear the previous result before starting a new request.
    st.session_state.media_bytes = None
    st.session_state.media_filename = None
    st.session_state.media_type = None
    st.session_state.result_ready = False

    if not permission:
        st.warning(
            "Please confirm you have permission to download this content."
        )

    else:
        try:
            clean_url = validate_url(url_input)

            with st.spinner(
                "Fetching your media... Please wait."
            ):
                data, filename = fetch_media(clean_url, media_type)

            # Save the result so it remains visible after reruns.
            st.session_state.media_bytes = data
            st.session_state.media_filename = filename
            st.session_state.media_type = media_type
            st.session_state.result_ready = True

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            error_text = str(error).lower()

            if "ffmpeg" in error_text:
                st.error(str(error))
            elif "max filesize" in error_text or "100 mb" in error_text:
                st.error("This file exceeds the 100 MB size limit.")
            else:
                st.error(
                    "Unable to fetch this media. It may be private, "
                    "unavailable, unsupported or temporarily blocked "
                    "by Instagram. Check the link and try again."
                )


# =====================================================
# RESULT SECTION
# Display below the form, then scroll into view
# =====================================================
if (
    st.session_state.result_ready
    and st.session_state.media_bytes
):
    data = st.session_state.media_bytes
    filename = st.session_state.media_filename
    output_type = st.session_state.media_type
    file_size_mb = len(data) / (1024 * 1024)

    # Result anchor for automatic scrolling.
    st.markdown(
        '<div id="result-section"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="result-card">
            <div class="ready-label">✓ MEDIA READY</div>
            <h3>Your {output_type} is ready!</h3>
            <p class="muted">
                Preview your file below, then use the download button
                to save it to your device.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Center the small preview.
    preview_left, preview_center, preview_right = st.columns([1, 2, 1])

    with preview_center:
        if output_type == "Video MP4":
            st.video(data)
        else:
            st.audio(data, format="audio/mpeg")

    st.markdown(
        f"""
        <div class="result-card">
            <div class="file-name">📄 {filename}</div>
            <p class="muted">File size: {file_size_mb:.2f} MB</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    suffix = Path(filename).suffix.lower()

    if suffix == ".mp3":
        mime_type = "audio/mpeg"
    elif suffix == ".mp4":
        mime_type = "video/mp4"
    elif suffix == ".webm":
        mime_type = "video/webm"
    elif suffix == ".mkv":
        mime_type = "video/x-matroska"
    else:
        mime_type = "application/octet-stream"

    st.download_button(
        label=f"⬇ Download {output_type}",
        data=data,
        file_name=filename,
        mime=mime_type,
        type="primary",
        use_container_width=True,
        key="download_media_button",
    )

    st.caption("Your file is ready. Click above to save it.")

    # Try to scroll the page to the result after rendering.
    # The fallback is simply displaying the result below the form.
    components.html(
        """
        <script>
        (function () {
            function scrollToResult() {
                try {
                    const doc = window.parent.document;
                    const target = doc.getElementById("result-section");

                    if (target) {
                        target.scrollIntoView({
                            behavior: "smooth",
                            block: "start"
                        });
                    }
                } catch (e) {
                    // The result remains visible below the form.
                }
            }

            setTimeout(scrollToResult, 300);
            setTimeout(scrollToResult, 800);
        })();
        </script>
        """,
        height=0,
    )


# =====================================================
# FOOTER
# =====================================================
st.markdown("---")

st.markdown(
    """
    <div class="footer">
        ReelSaver · Independent tool, not affiliated with Instagram.
        <br>Only download content you own or have permission to save.
        <br>Availability depends on Instagram access and content restrictions.
    </div>
    """,
    unsafe_allow_html=True,
)
