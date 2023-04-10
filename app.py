import os
import torch
from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import yake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

app = Flask(__name__)

# Set the secret key for sessions
app.secret_key = "everySessionIsUniq929234"

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Load the pre-trained GPT-2 model and tokenizer - use gpt2-large for a better experience
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

@app.route('/')
def home():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html', chat_history=session['chat_history'])
    
@app.route('/generate', methods=['POST'])
def generate():
    if 'chat_history' not in session:
        session['chat_history'] = []

    user_prompt = request.form['prompt']
    user_prompt = sanitize_text(user_prompt)

    # Analyze the sentiment of the user's input
    sentiment_analyzer = SentimentIntensityAnalyzer()
    sentiment = sentiment_analyzer.polarity_scores(user_prompt)
    sentiment_label = "neutral"

    if sentiment["compound"] >= 0.05:
        sentiment_label = "positive"
    elif sentiment["compound"] <= -0.05:
        sentiment_label = "negative"

    # Create GPT-2 input with the last user message and bot message
    last_message = session['chat_history'][-1] if session['chat_history'] else {"user": "", "bot": ""}
    
    # With more context GPT-2 can act strange
    gpt2_input = f"You said '{user_prompt}'. I respond with the following: "
    input_tokens = tokenizer.encode(gpt2_input, return_tensors='pt')

    # Create attention_mask for input tokens
    attention_mask = [1] * len(input_tokens[0])

    outputs = model.generate(
        input_tokens, 
        attention_mask=torch.tensor([attention_mask]),
        max_length=140,  # Increase max_length to generate longer responses
        num_return_sequences=1, 
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id,  # Set pad_token_id to eos_token_id for open-end generation
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    # Remove the input tokens from the generated response
    response = response[len(tokenizer.decode(input_tokens[0])):].strip()
    response = sanitize_text(response)
    response = truncate_to_last_sentence(response, 140)

    session['chat_history'].append({'user': user_prompt, 'bot': response})
    session.modified = True
    return jsonify(response)

def truncate_to_last_sentence(text, char_limit):
    if len(text) <= char_limit:
        return text

    truncated_text = text[:char_limit]
    last_period = truncated_text.rfind('.')
    last_question = truncated_text.rfind('?')
    last_exclamation = truncated_text.rfind('!')

    last_sentence_end = max(last_period, last_question, last_exclamation)
    
    if last_sentence_end == -1:
        return ""
    else:
        return truncated_text[:last_sentence_end + 1]

def sanitize_text(text):
    # Remove HTML tags and attributes
    clean_text = re.sub('<[^<]+?>', '', text)

    # Remove JavaScript code
    clean_text = re.sub('<script[^>]*>.*?</script>', '', clean_text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)

    # Remove CSS code
    clean_text = re.sub('<style[^>]*>.*?</style>', '', clean_text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)

    # Remove comments
    clean_text = re.sub('<!--.*?-->', '', clean_text, flags=re.DOTALL)

    # Replace special characters
    clean_text = clean_text.replace('&', '')
    clean_text = clean_text.replace('<', '')
    clean_text = clean_text.replace('>', '')
    clean_text = clean_text.replace('"', '')
    clean_text = clean_text.replace("'", '')
    clean_text = clean_text.replace("[", '')
    clean_text = clean_text.replace("]", '')
    clean_text = clean_text.replace("{", '')
    clean_text = clean_text.replace("}", '')
    clean_text = clean_text.replace("}", '')
    clean_text = clean_text.replace("】", '')
    clean_text = clean_text.replace("【", '')
    clean_text = clean_text.replace("_", '')
    clean_text = clean_text.replace("Fred:", '')
    clean_text = clean_text.replace(":", ' ')

    return clean_text

if __name__ == '__main__':
    app.run(debug=True)
