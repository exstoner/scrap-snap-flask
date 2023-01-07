from flask import Flask, render_template, request, url_for, redirect, send_file, session
from bs4 import BeautifulSoup
import json
import requests
import urllib.parse
from io import BytesIO
from flask import Response


app = Flask(__name__)
    

@app.route("/", methods=['POST', 'GET'])
def index():
     if request.method == "POST":
           # Get the SnapChat URL
           url_received = request.form["url_request"]
           
           # When URL is presented 
           if url_received:
            # Retrieve The URL
            r = requests.get(url_received)
            # Scrape
            soup = BeautifulSoup(r.content, 'html.parser')
            script = soup.findAll("script", attrs={"id": "__NEXT_DATA__"})
            # Remove extra charachters from Script
            script = str(script)
            video = script.strip()[52:-10]
            # Load the scraped data in JSON
            data = json.loads(video)
            # Get data from JSON
            video_name = data['props']['pageProps']['linkPreview']['title']
            creator = data['props']['pageProps']['publicProfileInfo']['title']
            video_link = data['props']['pageProps']['preselectedStory']['premiumStory']['playerStory']['snapList']
            # Render To HTML
            return render_template("generate.html", video_name=video_name,video_link=video_link,creator=creator)
           else:
               return render_template("index.html") 
     else:
         return render_template("index.html")
    
@app.route("/download", methods=['POST','GET'])
def download_video():
    if request.method == 'POST':
        # Get each clip URL
        button_value = request.form['download_video']
        # Download the Video 
        r = requests.get(button_value)
        video_content = r.content
        # Prompet User to Save Video
        response = Response(video_content, mimetype="video/mp4")
        response.headers["Content-Disposition"] = "attachment"
        return response

    



if __name__ == '__main__':
    app.run()