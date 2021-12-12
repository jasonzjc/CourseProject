# Generate keywords for a course in a YouTuBe playlist
# Input is the YouTuBe playlist url
# Output is the key phrases, the corresponding videos, and the play time 
from youtube_scrape_playlist import playlist_generation
from youtube_transcript_api import YouTubeTranscriptApi

from keybert import KeyBERT
import yake

import json
import re,os

class Documents:

    '''
    Documents class to crawl transcripts of a playlist/course and 
    generate the document collection
    '''
    def __init__(self,url):
        self.script_path = url
        self.doc_size = 0
        self.scrip_content = []
        self.doc = ''
        self.doc_indexed = {}
        self.playlist = {}

    def scraping(self):

        '''
        Scraping each video page in the playlist and 
        collect the transcripts and their timestamps
        Generate
        1) a string of all transcripts
        2) a dictionary containing each sentence and its location (video it is from and its timestamp)
        '''

        print('Playlist generating...')
        self.playlist = playlist_generation(self.script_path)

        print('Transcrips scraping...')
        for title,value in self.playlist.items():
            this_transcript = YouTubeTranscriptApi.get_transcript(value[0])
            transcript_content = []
            for sentence in this_transcript:
                sentence['text'] = sentence['text'].replace("\n"," ")
                transcript_content.append(sentence['text'])
            this_doc = ' '.join(transcript_content)
            self.doc = self.doc + this_doc
            self.doc_indexed[title] = this_transcript

    def get_doc(self):

        '''
        I/O function to output the string of all transcripts
        '''

        if self.doc == '':
            self.scraping()
        return self.doc

    def get_doc_indexed(self):

        '''
        I/O function to output the indexed document in the form of a dictionary
        '''

        if self.doc_indexed == {}:
            self.scraping()
        return self.doc_indexed

    def get_playlist(self):

        '''
        I/O function to output the playlist, which includes video title, number, and the URL
        '''

        if self.playlist == {}:
            self.playlist = playlist_generation(self.script_path)
        return self.playlist

    def get_url(self):

        return self.script_path

class KeyPhraseFinder:

    def __init__(self):
        self.keywords_list = []
        self.keywords_locations = {}
        self.keywords_first_location = {}

    def train_yk(self,doc,topword_no):

        '''
        Train YK! to generate key words
        Input a document, and the number of key words desired
        Output a list of keywords and likelihood
        '''

        kw_extractor_yk = yake.KeywordExtractor(lan="en",top=topword_no)
        keywords_yk = kw_extractor_yk.extract_keywords(doc)
        return keywords_yk

    def train_bert_with_cand(self,doc,candidate_words,diverse):

        '''
        Train Bert to generate key phrases
        Input a document, a list of candidate words, and a diverse factor
        Output a list of keywords and likelihood
        '''

        candidates = [candidate[0] for candidate in candidate_words]

        kw_model = KeyBERT('all-MiniLM-L6-v2')
        keywords = kw_model.extract_keywords(doc, candidates=candidates,use_mmr=True, diversity=diverse)

        return keywords

    def locate_word(self,doc_indexed,word):

        '''
        Find all the locations of the given key phrase in the document
        '''

        result = []
        for title,transcripts in doc_indexed.items():
            for sentence in transcripts:
                if word in sentence['text']:
                    result.append([title,sentence])
        return result

    def locate_all_words(self,doc_indexed,word_list):

        '''
        Collect all the locations of the given key phrase list
        '''

        word_location_dic = {}
        for word in word_list:
            word_location_dic[word] = self.locate_word(doc_indexed,word)
        return word_location_dic

    def find_keywords(self,all_doc,topK=50,diverse_factor=0.7):

        '''
        find key phrases and their locations with the input of a Documents instance
        '''

        print('Finding keywords...')
        keywords_yk = self.train_yk(all_doc.get_doc(),topK)
        keywords_bert = self.train_bert_with_cand(all_doc.get_doc(),keywords_yk,diverse_factor)

        self.keywords_list = [word[0] for word in keywords_bert]
        self.keywords_locations =self.locate_all_words(all_doc.get_doc_indexed(),self.keywords_list)

    def get_keywords_list(self):

        return self.keywords_list

    def get_keywords_locations(self):

        return self.keywords_locations

    def get_keywords_first_location(self):

        for keyword,locations in self.keywords_locations.items():
            self.keywords_first_location[keyword] = locations[0]

        return self.keywords_first_location

def get_keywords_links(finder,docs):

    keywords_first_location = finder.get_keywords_first_location()
    play_list = docs.get_playlist()
    keywords_links = {}
    for keyword, first_location in keywords_first_location.items():
        title = first_location[0]
        video_name = play_list[title][0]
        video_url_embed = 'https://www.youtube.com/embed/' + video_name
        start_time = int(first_location[1]['start'])
        video_time_url = video_url_embed + '?start={}'.format(start_time)
        keywords_links[keyword] = video_time_url
    return keywords_links
        

def dump_to_json(docs,content,folder_name):

    url = docs.get_url()
    playlist_name = re.search('playlist\?list=(.+)',url).group(1)
    path = os.path.join(os.getcwd(),'cache','{}'.format(folder_name))
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path,'{}.json'.format(playlist_name)),'w+') as json_file:
        json.dump(content,json_file)

if __name__ == "__main__":
    url = 'https://www.youtube.com/playlist?list=PLUl4u3cNGP61iQEFiWLE21EJCxwmWvvek'
    mydocs = Documents(url)
    finder = KeyPhraseFinder()

    finder.find_keywords(mydocs)

    keywords_links = get_keywords_links(finder,mydocs)
    dump_to_json(mydocs,mydocs.get_doc_indexed(),'doc_indexed')
    dump_to_json(mydocs,keywords_links,'key_url')

    # keywordslist = finder.get_keywords_list()
    # keywordslocation = finder.get_keywords_locations()

    # print('Keywords: ')
    # print(keywordslist)

    # print('Keywords Locations: ')
    # print(keywordslocation)