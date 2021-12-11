from youtube_scrape_playlist import playlist_generation

url = 'https://www.youtube.com/playlist?list=PLUl4u3cNGP63z5HAguqleEbsICfHgDPaG'
playlist = playlist_generation(url)
print(playlist)