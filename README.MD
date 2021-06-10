![example workflow](https://github.com/Yanhenning/openai/actions/workflows/pipeline.yml/badge.svg) 
[![codecov](https://codecov.io/gh/Yanhenning/openai/branch/master/graph/badge.svg?token=KPXVj0KgXn)](https://codecov.io/gh/Yanhenning/openai)

### Como rodar o projeto

Para rodar o projeto local utilizando seu próprio ambiente você deve criar um arquivo
chamado `apiconfi.json` com as credenciais do seu projeto.

Rode `pip install -r requirements.txt` para instalar os pacotes necessários


#### Rodando com python:
`python main.py`

#### Rodando com gunicorn

`gunicorn -b localhost:8080 main:app`
