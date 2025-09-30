import os
import yt_dlp
from config import Config

class VideoDownloader:
    def __init__(self):
        self.download_path = Config.DOWNLOAD_PATH
        self._ensure_download_dir()
    
    def _ensure_download_dir(self):
        """Create download directory if it doesn't exist"""
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
    
    def is_supported_url(self, url):
        """Check if the URL is from a supported platform"""
        supported_domains = ['instagram.com', 'tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com']
        return any(domain in url.lower() for domain in supported_domains)
    
    def download_video(self, url):
        """Download video from URL and return file path"""
        try:
            ydl_opts = {
                'outtmpl': os.path.join(self.download_path, '%(title).100s.%(ext)s'),
                'format': 'best[filesize<50M]',  # Limit to 50MB
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                return {
                    'success': True,
                    'file_path': filename,
                    'title': info.get('title', 'Video'),
                    'duration': info.get('duration', 0)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def cleanup_file(self, file_path):
        """Clean up downloaded file after sending"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
