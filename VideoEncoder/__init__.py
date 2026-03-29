import os
import logging
import time
from io import BytesIO, StringIO
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from pyrogram import Client

# Start time
botStartTime = time.time()

# Load environment variables
if os.path.exists('config.env'):
    load_dotenv('config.env')

# Bot credentials
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
session = os.getenv("SESSION_NAME", "VideoEncoderBot")

# Database and directories
database = os.getenv("MONGO_URI")
drive_dir = os.getenv("DRIVE_DIR")
index = os.getenv("INDEX_URL")
download_dir = os.getenv("DOWNLOAD_DIR", "downloads")
encode_dir = os.getenv("ENCODE_DIR", "encoded")

# Users
owner = list(set(int(x) for x in os.getenv("OWNER_ID", "").split()))
sudo_users = list(set(int(x) for x in os.getenv("SUDO_USERS", "").split()))
everyone = list(set(int(x) for x in os.getenv("EVERYONE_CHATS", "").split()))
all_users = everyone + sudo_users + owner

# Log channel
try:
    log = int(os.getenv("LOG_CHANNEL"))
except:
    log = owner[0] if owner else None
    if not log:
        print("⚠️ Fill log channel or provide user/channel/group ID at least!")

# In-memory data
data = []

# Progress format
PROGRESS = """
• {0} of {1}
• Speed: {2}
• ETA: {3}
"""

# Supported video MIME types
video_mimetype = [
    "video/x-flv",
    "video/mp4",
    "application/x-mpegURL",
    "video/MP2T",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/quicktime",
    "video/mpeg"
]

# Helper to create in-memory files
def memory_file(name=None, contents=None, *, bytes=True):
    if isinstance(contents, str) and bytes:
        contents = contents.encode()
    file = BytesIO() if bytes else StringIO()
    if name:
        file.name = name
    if contents:
        file.write(contents)
        file.seek(0)
    return file

# Check and create folders
for folder in [download_dir, encode_dir, 'VideoEncoder/utils/extras']:
    if not os.path.isdir(folder):
        os.makedirs(folder)

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            'VideoEncoder/utils/extras/logs.txt',
            backupCount=20,
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

# Final Client setup — ✅ FIXED plugins path
app = Client(
    session_name=session,
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
    plugins=dict(root="VideoEncoder/plugins"),  # fixed path
    sleep_threshold=30,
    max_concurrent_transmissions=16,
    workers=32,
    ipv6=False
)

if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run()
