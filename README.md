# CourseProject: Intelligent Learning Platform

# Overview

The topic of this project is to organize the scattered lectures into a coherent “multimedia textbook” and create an index.  A course typically covers many words, but only a few are key words and relates to the knowledge introduced in the course. The learner may like to quickly find the lecture or the location a specific topic is presented, or a specific key word is defined and explained. This topic relates to the text retrieval, language model, and topic analysis introduced in the text information system class.

# Software Implementation
## Dataset Selction
Originally, I plan to use the content of this course as an example, and I did extracted the key phrases (i.e. index) of this course. However, I then found no way to embed the Coursera videos into my webpage. I believe this is due to that Coursera does not allow video embedding. Furthermore, I found no explicity way to generate a link to a specific timestamp on Coursera videos. Therefore, I have to turn to an alternative solution.  
In this project, I used open course playlists in YouTube as the input data, because:
1. There are a good bunch of these courses in YouTube, e.g. MIT OCW.
2. The transcripts are well-orgniazed.
3. YouTube allows users to embed its vidoes to webpages.

## Software Structure
This software is constructed from three modules:
- Data collection
- Key phrases extraction
- Platform integration
They are explained in details below.

## Data Collection
The data collection module is to collect the essential contents of the user specified course, includes the URL of each video and the transcript of each video. The URL of a YouTube playlist is like this: https://www.youtube.com/playlist?list=PLUl4u3cNGP61iQEFiWLE21EJCxwmWvvek. The string after 'list=' is its list ID. In this page, all the videos are listed. 
![alt text](https://github.com/jasonzjc/CourseProject/blob/Pre-publish/images/playlist.png?raw=true)

First of all, the title and URL of each video is scraped using [BeautifulSoupt](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). The URL of a YouTube video is typically like this: https://www.youtube.com/watch?v=YrHlHbtiSM0. The string after 'v=' is its unique video ID. Therefore, we can obtain the video IDs in this playlist. With the video ID, we can crawl its transcript. Here [YouTubeTranscriptApi](https://github.com/jdepoix/youtube-transcript-api) is used to get the transcripts.

With these information, we generated two data: 
- A string concatenating all the texts in the transcripts, to represent the document of this course. This will be fed into the algorithm to extract the key phrases.
- A dictionary containing the title, URL, content, start and stop time of each sentence. This is used to locate the key phrases and these locations will be used by the platform.

## Key Phrases Geneartion
With the content of a course, now we need to generate the key phrases. It is not necessiarly a single word, but could also contain two, three, or many words. Therefore, it appears to be difficule to simply relies on TF-IDF algorithm. Here I used [BERT](https://arxiv.org/abs/1810.04805v2) algorithm. BERT stands for Bidirectional Encoder Representations from Transformers. It is a [transformer-based machine learning technique for natural language processing (NLP) pre-training developed by Google](https://en.wikipedia.org/wiki/BERT_(language_model)). The document embedding is extraced with BERT first, then word embeddings are extracted for N-gram words/phrases. Lastly, cosine similarity is used to find the words and phrases with the highest similarity to the document. Here, the tool [KeyBERT](https://github.com/MaartenGr/KeyBERT) is used to realize BERT algorithm.

It is also found that some phrases BERT found is not quite the keywords of the document. E.g., a word are repeated in an example but it is not a technique word in this course. To conqur this, I tried to combine KERT with another keyword extractino method, i.e. [Yake!](https://github.com/LIAAD/yake). Yake! is used to execute a first-round keywords extraction. Then this list of keywords are input into BERT for keyword and phrase extraction. In the limited cases being studied, I found this algorithm works better than using BERT alone.

After the extraction of key phrases, they are located in the videos. In the current implementation, the first location is selected. This is because intuitively, a key phrase is typically explained during or just after the first time it is mentioned in a course. 

## Platform Integration
The key phrases and their locations are demonstrated in a Webpage. The webpage is generated with [FLASK](https://flask.palletsprojects.com/). The key phrases are listed on the left side of the page, with a link including the corresponding video ID and timestamp. The video block locates on its right. When clicking the link of a key phrase, the corresponding YouTube video will be refreshed on its right. By clicking the play button, the embedded video will automatically start from the timestamp when this keyphrase is introduced.

## Further Improvements
If this project is to be continued in the future, I would like to improve the key phrase geneartion algorithm. E.g., including the context into the algorithm. Titles of each video is a good candidate to improve the accuracy in key phrase generation. Also, the location of a key phrase is not necessary in the first time it is mentioned. Senmentical analysis can be used to pinpoint the sentence(s) it is explained. Thirdly, the platform can be improve to better integrate the key phrase, the transcript, and the video. The key phrases can be hierarchied to form the structure of a course.

# Software Usage
The software is supposed to run on Python 3.6.14 and above. 
1. Clone the repo and ensure that python3 is installed. After cloning, cd into CourseProject.
2. Run pip3 install -r requirements.txt to ensure you have the required packages to run this project.
3. Ensure you have a Chrome browser installed. Check its version and download the corresponding chromedriver [here](https://chromedriver.chromium.org/downloads). Use it to overwrite the chromedriver file in the repo.
4. Find a course playlist from YouTube. You can find a lot of playlist [here](https://www.youtube.com/c/mitocw). Be sure you copied the URL of a **playlist**, in a form like this: https://www.youtube.com/playlist?list=PLUl4u3cNGP63z5HAguqleEbsICfHgDPaG
5. Open `youtube_scrape_playlist.py` and replace the `url` value with your URL in the `__main__` function (Line 46). Run this file.
6. Open `webpage_flask.py` and replace the `url` value with your URL (Line 6). Run this file. 
7. Open http://127.0.0.1:5000/ in your browser. You should be able to click the key phrases and see the change of videos.

# Contribution
Jiecheng Zhao (NetID: jz109) is the only member of this team.
