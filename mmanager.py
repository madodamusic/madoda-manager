from mm_downloads.download import Download
from mm_uploads.google_drive.upload import GdriveUpload
import sys
class MMangaer:
    def __init__(self):
        self.m_contents = [{"download_url":"https://www.youtube.com/watch?v=z29nI8RQV0U&list=RDz29nI8RQV0U","gdrive_upload_times":5, "post_id":22, "tags":{"artist": "Chris Brown", "title":"Don't Judge Me"} }]
    
    
    def download_and_upload_to_gdrive(self):
        self.m_contents = Download(self.m_contents).main()
        self.m_contents = GdriveUpload(self.m_contents).mp3()
        print(self.m_contents)


if __name__ == "__main__":
    mm = MMangaer()
    mm.download_and_upload_to_gdrive()