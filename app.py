from flask import Flask, render_template, request

from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

import torch

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/summarize')
def summarize():
    return render_template('summarize.html')


@app.route('/summarizer',methods=['POST'])
def summarizer():
    video_url=request.form['video_url']
    video_id = video_url.split("=")[1]

    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    # extract transcript to json array

    #transcript[0:5]

    result = ""
    for i in transcript:
        result += ' ' + i['text']
    #print(result)
    #print(len(result))


    summarizer = pipeline('summarization')

    num_iters = int(len(result)/1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        #print("input text \n" + result[start:end])
        out = summarizer(result[start:end])  #minimum and maximum lenth
        out = out[0]
        out = out['summary_text']
        #print("Summarized text\n"+out)
        summarized_text.append(out)

    #print(summarized_text)

    l=len(str(summarized_text))

    summarized_text = str(summarized_text)

    return render_template('summarizedresult.html',summarized_text=summarized_text,video_id=video_id)
    




@app.route('/summarizecheck')
def summarsummarizecheckize():


    #youtube_video = "https://www.youtube.com/watch?v=agl3vjzbG2o"
    youtube_video = "https://www.youtube.com/watch?v=n0P0rIlABOM"

    video_id = youtube_video.split("=")[1]

    #YouTubeVideo(video_id)

    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    #transcript[0:5]

    result = ""
    for i in transcript:
        result += ' ' + i['text']
    #print(result)
    #print(len(result))


    summarizer = pipeline('summarization')

    num_iters = int(len(result)/1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        #print("input text \n" + result[start:end])
        out = summarizer(result[start:end])
        out = out[0]
        out = out['summary_text']
        #print("Summarized text\n"+out)
        summarized_text.append(out)

    #print(summarized_text)

    l=len(str(summarized_text))

    summarized_text = str(summarized_text)

    return render_template('index.html',video_id = summarized_text,lenght=l)
    


app.add_url_rule('/index','index',index)

if __name__ == "__main__":
    app.run(debug=True)
