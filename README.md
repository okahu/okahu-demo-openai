# Okahu demo with OpenAI + Langchain
This repo includes a demo chat application built using OpenAI & Langchain that is pre-instrumented for observation with Okahu AI Observability cloud. 
You can fork this repo and run the app in Github Codespaces to get started quickly. 


## Try Okahu with this OpenAI app

To try this chatbot 
- Fork this repo and run in the Github Codespace 

You'll need 
- An OpenAI subscription and an API key to [OpenAI developer platform](https://platform.openai.com/overview)
- An Okahu tenant and API key to [Okahu AI Observability Cloud](https://www.okahu.ai)  

## Configure the demo environment
- Copy the file config/config.ini.template to config/config.ini
- Edit the config/config.ini file to add the OpenAI API Key and Okahu API key and save

## Run the interactive chatbot 
This application is an interactive chatbot that answers questions about coffee and built with a RAG design pattern.
Workflow is a python program using Langchain LLM orchestration framework. 
The vector dataset is built using multi-qa-mpnet-base-dot-v1 embedding model from Huggingface from a set of Wikipedia articles. The vector data is stored in a local filebased faiss vectorDB. 
The app uses OpenAI gpt-3.5-turbo model for inference.

To try Okahu from the Github Codespace 

1. Run the pre-instrumented chatbot app with following command from top level directory

   ```./coffee_client_openai_with_okahu.sh```
   
2. View the workflow discovered by Okahu AI Observability Cloud with following commands with your Okahu API key
    - Discover all components
      ```curl --location --request PUT 'https://api.okahu.ai/api/v1/discovery' --header 'x-api-key: <YOUR_OKAHU_API_KEY>;' ```
    - Get discovered components
      ```curl --location 'https://api.okahu.ai/api/v1/components' --header 'x-api-key: <YOUR_OKAHU_API_KEY>;' ```

    Check out Okahu AI Observability Cloud API docs [here](https://apidocs.okahu.ai)

### Example output 

To do 

### Okahu instrumentation

To run the chatbot app without Okahu instrumentation, use the command ```./coffee_client_openai.sh```

To understand how Okahu instrumentation works, compare the [coffee_rag_openai.py](rag_openai_service/coffee_rag_openai.py) and [coffee_rag_openai_with_okahu.py](rag_openai_service/coffee_rag_openaiwith_okahu.py)
