# Nutrition-Rag Project

A simple app for managing and tracking nutrition tips using Retrieval-Augmented Generation (RAG).

## Features

- Add, edit, and delete nutrition tips
- Search tips using RAG-based retrieval
- User-friendly interface

## Requirements

- Python 3.8+
- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI API](https://platform.openai.com/)
- [Streamlit](https://streamlit.io/)
- [FAISS](https://github.com/facebookresearch/faiss) (for vector search)

## Installation

```bash
git clone https://github.com/Youssef-Ai1001/Rag-Nutrition.git
cd Rag-Nutrition
```

### Install the required packages

```bash
pip install -r requirements.txt
```

### Setup the environment variables

```bash
cp .env.example .env
```
Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.




## Run the FastAPI server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection
Download the POSTMAN collection from [/assets/mini-rag-app.postman_collection.json](assets/RAG-APP.postman_collection.json)

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## License

Apache-2.0 license