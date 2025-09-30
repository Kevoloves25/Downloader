import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import Config
from video_downloader import VideoDownloader

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class VideoDownloadBot:
    def __init__(self):
        self.downloader = VideoDownloader()
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send welcome message when user sends /start"""
        welcome_text = """
🤖 **Social Media Video Downloader Bot**

Send me a link from:
• Instagram (Reels, Posts)
• TikTok

I'll download and send you the video!

⚠️ Note: Only public videos are supported.
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages with URLs"""
        user_message = update.message.text
        
        # Check if message contains a URL
        if not self.downloader.is_supported_url(user_message):
            await update.message.reply_text("❌ Please send a valid Instagram or TikTok URL.")
            return
        
        # Send "processing" message
        processing_msg = await update.message.reply_text("⏳ Downloading video...")
        
        try:
            # Download the video
            result = self.downloader.download_video(user_message)
            
            if result['success']:
                await processing_msg.edit_text("📤 Sending video...")
                
                # Send the video file
                with open(result['file_path'], 'rb') as video_file:
                    await update.message.reply_video(
                        video=video_file,
                        caption=f"🎬 {result['title']}",
                        supports_streaming=True
                    )
                
                await processing_msg.delete()
                
                # Clean up the downloaded file
                self.downloader.cleanup_file(result['file_path'])
                
            else:
                await processing_msg.edit_text(f"❌ Download failed: {result['error']}")
                
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            await processing_msg.edit_text("❌ An error occurred while processing the video.")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")

def main():
    """Start the bot"""
    if not Config.TELEGRAM_TOKEN:
        print("❌ Please set TELEGRAM_TOKEN in your .env file")
        return
    
    # Create bot application
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    bot = VideoDownloadBot()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    application.add_error_handler(bot.error_handler)
    
    # Start the bot
    print("🤖 Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
