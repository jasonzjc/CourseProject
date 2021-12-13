from flask import Flask, render_template
import os, json, re

app = Flask(__name__)

# play list URL
url = 'https://www.youtube.com/playlist?list=PLUl4u3cNGP63z5HAguqleEbsICfHgDPaG'
playlist_name = re.search('playlist\?list=(.+)',url).group(1)

# home page
@app.route("/")
def home():
    
    default_video_url = 'https://www.youtube.com/embed/YrHlHbtiSM0'

    # load the restored key phrase list and their links
    path = os.path.join(os.getcwd(),'cache','key_url','{}.json'.format(playlist_name))
    with open(path,'r') as file_handle:
        keywords_url = json.loads(file_handle.read())
    return render_template("home.html",keywords = keywords_url,video_url = default_video_url)

# the page after clicking the key phrase on the home page
# corresponding video is loaded
@app.route("/videos/<vid>")
def videos(vid):
    path = os.path.join(os.getcwd(),'cache','key_url','{}.json'.format(playlist_name))
    with open(path,'r') as file_handle:
        keywords_url = json.loads(file_handle.read())
    
    # restore the video link with start time
    [vname,stime] = vid.split(':')
    v_url = 'https://www.youtube.com/embed/{}?start={}'.format(vname,stime)
    return render_template("home.html",keywords = keywords_url,video_url = v_url)

# About page
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    
    app.run(debug=True, use_reloader=True)