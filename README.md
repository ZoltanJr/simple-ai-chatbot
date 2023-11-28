# simple-ai-chatbot

Freestyle chat app built on the pre-trained GPT-2 model(s).
Please be warned that the bots responses can and will be nonsensical, offensive and factually wrong.
This project was created for personal research and learning purposes. 


## How to use

- open terminal in project root
- create venv: ```python3 -m venv venv```
- start venv: ```source venv/bin/activate ```
    - exit venv: ```deactivate```
- install requirements: ```pip install -r requirements.txt```
- run app: ```flask run``` or ```python3 app.py```
- open app at at ```http://127.0.0.1:5000/```


## Dockerize and run the container

- build: ```docker build -t app-gpt2-chat .```
- run: ```docker run -p 5000:5000 --name app-gpt2-chat app-gpt2-chat```


## Parameters you can play with

- ```from_pretrained(«model»)```: try different gpt2 models
    - *gpt2-xl is not recommended on local machine*
- ```output_char_limit```: change output char limit
- ```gpt2_input```: modify model input
    - *observe different patterns in its answers*
    - *add conversation history to observe increasingly chaotic answers*
- ```model.generate(«params»)```: modify gpt2 output restrictions
- ```response```: change output formatting and restrictions as you wish

*Recommended Python version: 3.8*

pyenv global 3.8
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
