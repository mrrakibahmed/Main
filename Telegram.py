import os
import subprocess
import uuid
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7519273294:AAGqaTQIQq1X4GF_F5DexzBrKfbFYga8NDE"

# Helper function: check if URL is valid for yt-dlp
def is_supported_url(url):
    yt_dlp_domains = [
        "tiktok.com", "facebook.com", "fb.watch", "youtube.com", "youtu.be",
        "instagram.com", "pin.it", "pinterest.com"
    ]
    return any(domain in url for domain in yt_dlp_domains)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 হ্যালো Sir, শুধু TikTok, YouTube, FB, Instagram বা Pinterest লিংক পাঠাও, আমি ভিডিও নামিয়ে দেবো "
    )

# Handle link messages
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not is_supported_url(url):
        await update.message.reply_text("❌ সরি,  এই লিংকটা সাপোর্ট করি না 😥")
        return

    await update.message.reply_text("📥 ডাউনলোড হচ্ছে... একটু অপেক্ষা করো 😌")

    # Random filename for temporary download
    file_id = str(uuid.uuid4())
    output_template = f"{file_id}.%(ext)s"

    try:
        # Run yt-dlp subprocess
        result = subprocess.run(
            ["yt-dlp", "-o", output_template, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check for success
        if result.returncode != 0:
            await update.message.reply_text("😓 ডাউনলোড করতে পারলাম না... লিংকটা আবার চেক করো?")
            return

        # Find downloaded file
        for file in os.listdir():
            if file.startswith(file_id):
                with open(file, "rb") as video:
                    await update.message.reply_video(video)
                os.remove(file)  # Clean up
                return

        await update.message.reply_text("😓 ফাইল খুঁজে পেলাম না... কিছু একটা গোলমাল হইছে")

    except Exception as e:
        await update.message.reply_text(f"⚠️ সমস্যা হইছে জান: {e}")

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))

    print("🤖 বট চালু হইছে !")
    app.run_polling()