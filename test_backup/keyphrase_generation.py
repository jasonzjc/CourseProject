# This is the orignal tool to generate the keywords and key phrases from downloaded vtt files. 
# It is no longer a part of the current tool, but can be used in the future.


# # Try KeyBERT for Keyword Extraction
# Use Python 3.6.14  
# Need to install [keybert](https://github.com/MaartenGr/KeyBERT):
# 
# ```
# pip install keybert
# ```

# %%
from keybert import KeyBERT
import yake

# %% [markdown]
# Import os and glob modules.  
# Indicating the docment route. 

# %%
import os, glob

# %% [markdown]
# Read the transcript documents  
# Each row includes the timestamp and the content, which are divided by arrow `-->`  
# The contents before the first timestamp are context and are excluded from the documents being read.

# %%
# y = [x.split('/')[1] for x in script_path]
# y.sort()
# print(y)


# %% [markdown]
# Sort the document titles.

# %%
class Documents:
    def __init__(self,doc_path):
        self.script_path = []
        self.doc_path = glob.glob('test data/*.vtt')
        self.doc_size = len(self.doc_path)
        for i in range(1,self.doc_size+1):
            self.script_path.append(doc_path.format(i))

        self.time_arrow = '-->'
        self.scrip_content = []
        self.doc = ''
        self.doc_indexed = []
    
    def doc_extract(self):

        # Extract the sentences by removing the time stamps, and concantenate them to form the documents.  
        # Also restore the sentences with the time stamps and transcript file name into another list. Eventualy, it is used to retrieve the location of the key phrases. 

        for file in self.script_path:
            with open(file,'r',encoding="utf-8") as query_file:
                start_flg = 0
                transcript_id = file
                for line in query_file:
                    if start_flg == 1 and self.time_arrow not in line:
                        this_sentence = line.strip()
                        if len(this_sentence) > 0:
                            self.scrip_content.append(this_sentence)
                            this_sentence_indexed = (this_sentence,transcript_id,t1,t2)
                            self.doc_indexed.append(this_sentence_indexed)
                    elif start_flg ==1 and self.time_arrow in line:
                        [t1,t2] = line.split(self.time_arrow)
                        t1 = t1.strip()
                        t2 = t2.strip()
                    elif start_flg == 0 and self.time_arrow in line:
                        start_flg = 1
                        [t1,t2] = line.split(self.time_arrow)
                        t1 = t1.strip()
                        t2 = t2.strip()
                this_doc = ' '.join(self.scrip_content)
            self.doc = self.doc + this_doc


# %%
def train_yk(doc,topword_no):
    kw_extractor_yk = yake.KeywordExtractor(lan="en",top=topword_no)
    keywords_yk = kw_extractor_yk.extract_keywords(doc)
    return keywords_yk


# %%
def train_bert_with_cand(doc,candidate_words,diverse):
    candidates = [candidate[0] for candidate in candidate_words]

    kw_model = KeyBERT('all-MiniLM-L6-v2')
    keywords = kw_model.extract_keywords(doc, candidates=candidates,use_mmr=True, diversity=diverse)

    return keywords

# %% [markdown]
# Locate the key phrase in the document

# %%
def locate_word(doc_indexed,word):
    word = "retrieval model"
    result = []
    for sentence in doc_indexed:
        if word in sentence[0]:
            # this_result = (sentence[1],sentence[2])
            result.append(sentence)
    return result

def locate_all_words(doc_indexed,word_list):
    word_location_dic = {}
    for word in word_list:
        word_location_dic[word] = locate_word(doc_indexed,word)
    return word_location_dic

# %% [markdown]
# Use KeyBERT to extract the keywords.


def find_keywords():

    doc_path = r'test data/tr-lec{}-transcription-english.vtt'
    all_doc = Documents(doc_path)
    all_doc.doc_extract()
    keywords_yk = train_yk(all_doc.doc,50)
    keywords_bert = train_bert_with_cand(all_doc.doc,keywords_yk,0.7)

    keywords_list = [word[0] for word in keywords_bert]
    keywords_locations = locate_all_words(all_doc.doc_indexed,keywords_list)

    return keywords_locations

if __name__ == "__main__":
    print(find_keywords())
