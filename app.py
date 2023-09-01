from flask import Flask, render_template, request
import requests
import openai
import os
import time

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)

# Load environment variables from .env file


# Access the API key from the environment


def get_completion(prompt):
    # Set your OpenAI API key here
    openai.api_key = "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"

    # Define a prompt to start the conversation
    #prompt = "You are a helpful assistant.\nUser: Hello, can you tell me about the weather today?"

    # Get a response from the API
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose the engine that suits your use case
        prompt=prompt,
        max_tokens=50  # You can adjust the max_tokens parameter to control the response length
    )

    # Extract the assistant's reply from the response
    return  response.choices[0].text.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        pdf = request.files['pdf']
        num_sentences = int(request.form['sentences'])
        import PyPDF2
        import re
        pdf_reader = PyPDF2.PdfReader(pdf)
        text = ""
        summary=""
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            
        # Remove text that resembles URLs or links
            cleaned_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', page_text)
            cleaned_text = re.sub(r'www\.[^\s]+', '', cleaned_text)
        
            text += cleaned_text
            #text+=page_text
            
            #if text and num_sentences:
                #pdf_content = text
            if len(text)>=3000 :
                prompt = f"Summarize the following text:\n{text}\nThe summary should follow the following rules :\n 1)The summary should contain atleast {num_sentences}\n\n 2) Every sentence of summary should be complete ad ended with full stop . 3) There should not be any knowledge gaps"
                summary = summary +"\n\n\n\n\n  \n\n\n\n\n\n\n"+get_completion(prompt)
                text=""
            
                time.sleep(25)
            

    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
