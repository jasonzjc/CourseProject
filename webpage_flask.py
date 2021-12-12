from flask import Flask, render_template
import os, json, re

app = Flask(__name__)

url = 'https://www.youtube.com/playlist?list=PLUl4u3cNGP61iQEFiWLE21EJCxwmWvvek'
playlist_name = re.search('playlist\?list=(.+)',url).group(1)

@app.route("/")
def home():
    
    default_video_url = 'https://www.youtube.com/embed/YrHlHbtiSM0'
    path = os.path.join(os.getcwd(),'cache','key_url','{}.json'.format(playlist_name))
    with open(path,'r') as file_handle:
        keywords_url = json.loads(file_handle.read())
    return render_template("home.html",keywords = keywords_url,video_url = default_video_url)

@app.route("/videos/<vid>")
def videos(vid):
    path = os.path.join(os.getcwd(),'cache','key_url','{}.json'.format(playlist_name))
    with open(path,'r') as file_handle:
        keywords_url = json.loads(file_handle.read())
    [vname,stime] = vid.split(':')
    v_url = 'https://www.youtube.com/embed/{}?start={}'.format(vname,stime)
    return render_template("home.html",keywords = keywords_url,video_url = v_url)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    
    app.run(debug=True, use_reloader=True)