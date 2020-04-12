from download_manager.download_URL_txt import ManagerURL

manager_url = ManagerURL()
urls = manager_url.getAllUrls()
yurls = manager_url.getYoutubeUrls()
wp_id = manager_url.getWP_ID("https://www.youtube.com/watch?v=dDwWE1hp8rY")
print(urls)
print("\n")
print(yurls)
print("\n")
print(wp_id)
print("done")