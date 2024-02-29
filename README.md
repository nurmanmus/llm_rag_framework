# llm base service

# for new llm chains 

if you want to create new chain  you simply create another folder like llm/chains/hf_chain and add your chain to llm/chains/__init__.py for easy import

import it to llm/router.py and add it to router


# local development


install requirements
```bash
pip3 install -r core/requirements/dev.txt
pip3 install -r llm/requirements.txt
python3 -m spacy download en_core_web_sm
```

```bash
cp .env.example .env
```
and fill .env file essipecially HUGGINGFACE_API_KEY

embedding functions defined as constant in chain.py. and ingest.py you can change it to your own function from any huggerface model. reason is this different chains may need different embedding functions. 


add your hugging face api key to llm/chains/mesolitica/chain.py

```python

from llm.factory import LLMFactory, LLMType
from llm.schemas import HuggingFaceEndpointConfig, Question

HUGGINGFACEHUB_API_TOKEN = "hf_yourtoken"
```

fill HUGGINGFACEHUB_API_TOKEN with your hugging face api key

RAG NOTES:

create vector database with ingest.py. you can run this command when you add new pdfs and txts to chain folders.
you MUST run this command before starting fast api server once. if you runned it before you do not need to run it again.
when you run this processed files will be saved to vector database and moved under processed folder. 
after every ingest operation you should restart fast api server.  since they are loaded to memory and not updated in memory and database.

```bash
python3 llm/chains/mesolitica/ingest.py
python3 llm/chains/hf_chain/ingest.py
```

delete single file from vector database. make sure it is in processed folder. 
delete command it will delete file from vector database and move it to data folder. 

file_name includes file extension: *.pdf, *.txt

```bash
python3 llm/chains/mesolitica/ingest.py --delete "file_name"
```

```bash
python3 llm/chains/hf_chain/ingest.py --delete "file_name"
```

reset vector database. it will delete all files from vector database and move them to data folder. 

```bash
python3 llm/chains/mesolitica/ingest.py --reset
```

```bash
python3 llm/chains/hf_chain/ingest.py --reset

```

then run mlflow server on other terminal
```bash
mlflow server --host 0.0.0.0 --port 5000
```

mlflow dashboar located at [http://localhost:5000](http://localhost:5000)

You can check mlflow runs under experiment name mistral and mixtral. short time requests are saved under same run. so check different artifacts for different requests

Then finally run the FastAPI endpoint

```bash
uvicorn main:app --reload
```
optional:
app.log contains error logs if you need to debug.

# RAG data storage

rag data storage is done with chromadb. you can use chromadb to store and retrieve data from rag. 

the logic of rag llm chains is. you can inject your own data with semantic search and add to in your prompt and get the results.

example 

prompt: " help the user with following context {context} and answer the question {question}"


context is retrieved from semantic search and added to prompt and question is added to prompt. 


there is a chunck size setting in chain.py it means it split the context into chuncks and add to prompt. 

add any pdf file to related chain folder. for example for malaysian_mistral chain add pdf to mesolitica/data folder. 

for myth chain add pdf to hf_chain/data folder. 

I added example pdfs and text. 

When you start fast api vectorstore will be done and you can test in notebook.

You can add more pdfs.


# test endpoints

open langchain_test.ipynb and run all cells. make sure service up and running and url is correct


with curl

mistral test

```bash
curl -X 'POST' \
  'http://localhost:8000/llm/mistral-api' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "vikings"
}'
```

curl -X POST "http://localhost:8000/llm/mistral-api" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"query\": \"elon musk\"}"


mixtral test

```bash
curl -X 'POST' \
  'http://localhost:8000/llm/mixtral-api' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "vikings"
}'
```

## test RAG english
curl -X POST "http://localhost:8000/llm/rag_mixtral-api" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"query\": \"How did badang become so strong??\"}"

curl -X POST "http://localhost:8000/llm/rag_mixtral-api" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"query\": \"How many TRAYS of betel nuts did the princess of gunung ledang wanted from the Sultan????\"}"



## test RAG malaysian
curl -X POST "http://localhost:8000/llm/malaysian_mistral-api" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"query\": \"anwar ibrahim\"}"




## extra info if you use ollama models
install ollama for ollama models

pull models
```bash
ollama pull model_name
```


## docker development

```bash
docker-compose up -d
```


mistral test

```bash
curl -X 'POST' \
  'http://localhost/llm/mistral-api' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "vikings"
}'
```

mixtral test

```bash
curl -X 'POST' \
  'http://localhost/llm/mixtral-api' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "vikings"
}'
```

check mlflow runs under experiment name mistral and mixtral. short time requests are saved under same run. so check different artifacts for different requests

mlflow dashboar located at [http://localhost:5000](http://localhost:5000)



## dependencies
ollama installation: ollama should be installed and model should be downloaded for ollama

install ollama and pull models with
```bash
ollama pull model_name
```


## deployment

1. install docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

post installation steps
```bash
sudo usermod -aG docker $USER
newgrp docker
```


2. install docker-compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. start docker-compose

```bash
docker-compose up -d
```

# Deploy Hugging Face Endpoint

1. click to deploy button which model you want to deploy on hugging face

docs/Screenshot 2024-01-28 at 14.55.21.png
<img width="1440" alt="Screenshot 2024-01-28 at 14 55 21" src="docs/Screenshot 2024-01-28 at 14.55.21.png">

2. After clicking make sure your payment methods set on Hugging face otherwise you can not see below screen and you can not deploy model.

3. Set your model configurations MAKE SURE scale to zero is selected otherwise you will pay for model even if it is not used. 

<img width="1440" alt="step2" src="docs/Screenshot 2024-01-28 at 14.56.51.png">

4. After clicking deploy button you will see below screen. You can check your model status on this screen.

<img width="1440" alt="step3" src="docs/Screenshot 2024-01-28 at 14.58.03.png">

IMPORTANT: check your usage and stop model if you do not use it. otherwise you will pay for it even if you do not use it.

<img width="1440" alt="step4" src="docs/Screenshot 2024-01-28 at 15.06.33.png">

