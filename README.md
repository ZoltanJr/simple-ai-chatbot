# gpt2-chat
Freestyle chat app built on GPT-2. Have fun!
You need Google Chrome to support Speech-2-Text functionality and to talk with GPT2 Chat!

(Supported Python version: 3.8)

## How to use
 - create venv: python3 -m venv venv
 - start venv: source venv/bin/activate (exit with 'deactivate' command)
 - install requirements: pip install -r requirements.txt
 - run app: python3 app.py

 ## Dockerize and run the container
 - docker build -t app-pig-chat .
 - docker run -p 5000:5000 --name app-pig-chat app-pig-chat
