from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # mylist = ['a','b']
    mylist = {'a':'http://www.google.com','b':'http://www.youtube.com'}
    return render_template("home.html",keywords = mylist)
    
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)