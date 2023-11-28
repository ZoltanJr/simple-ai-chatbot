import os
import torch
import re
from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from dotenv import load_dotenv
from transformers import GPT2LMHeadModel, GPT2Tokenizer

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Choose from: gpt2, gpt2-medium, gpt2-large, gpt2-xl
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

output_char_limit = 140

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

    last_message = session['chat_history'][-1] if session['chat_history'] else {"user": "", "bot": ""}
    gpt2_input = f"You said '{user_prompt}'. I respond with the following: "
    input_tokens = tokenizer.encode(gpt2_input, return_tensors='pt')
    attention_mask = [1] * len(input_tokens[0])

    outputs = model.generate(
        input_tokens, 
        attention_mask=torch.tensor([attention_mask]),
        max_length=output_char_limit,
        num_return_sequences=1, 
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id
    )

    response = truncate_to_last_sentence(
        sanitize_text(
            tokenizer.decode(outputs[0], skip_special_tokens=True)
            .strip()[len(tokenizer.decode(input_tokens[0])):]
            .strip()
        ), 
        output_char_limit
    )


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
    patterns = [
        '<[^<]+?>',
        '<script[^>]*>.*?</script>',
        '<style[^>]*>.*?</style>',
        '<!--.*?-->'
    ]
    
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    
    special_chars = ['&', '<', '>', '"', "'", "[", "]", "{", "}", "】", "【", "_", ":"]
    for char in special_chars:
        text = text.replace(char, '')

    return text

if __name__ == '__main__':
    app.run(debug=True)
