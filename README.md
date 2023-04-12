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
- run app: ```python3 app.py```
- open app at at ```http://127.0.0.1:5000/```


## Dockerize and run the container

- build: ```docker build -t app-pig-chat .```
- run: ```docker run -p 5000:5000 --name app-pig-chat app-pig-chat```


## Customization opportunities

- app.py L20-21: try different gpt2 models
    - *gpt2-xl is not recommended on local machine*
- app.py L23: change output char limit
- app.py L51: modify gpt2_input
    - *observe different patterns in its answers*
    - *pass sentiment_label along to add context*
    - *add conversation history to observe increasingly chaotic answers*
- app.py L60: modify gpt2 output restrictions
- app.py L71-73: change output formatting as you wish

*Recommended Python version: 3.8*
