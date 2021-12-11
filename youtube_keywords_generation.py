from youtube_scrape_playlist import playlist_generation
from youtube_transcript_api import YouTubeTranscriptApi

def scraping(url):
    playlist = playlist_generation(url)
    doc = ""
    doc_indexed = {}
    for title,value in playlist:
        this_transcript = YouTubeTranscriptApi.get_transcript(value[0])
        transcript_content = []
        for sentence in this_transcript:
            transcript_content.append(sentence['text'])
        this_doc = ' '.join(transcript_content)
        doc = doc + this_doc
        doc_indexed[title] = this_transcript



if __name__ == "__main__":
    url = 'https://www.youtube.com/playlist?list=PLUl4u3cNGP63z5HAguqleEbsICfHgDPaG'