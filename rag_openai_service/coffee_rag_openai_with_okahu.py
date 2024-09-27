import os
from langchain import hub
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import faiss
from langchain_core.runnables import RunnablePassthrough
from embeddings.embeddings_wrapper import HuggingFaceEmbeddings
from okahu_apptrace.instrumentor import setup_okahu_telemetry

vectorstore = None
prompt = None

def init():
    global vectorstore
    global prompt

    setup_okahu_telemetry(workflow_name = "langchain_openai_wf")
    embeddings = HuggingFaceEmbeddings(model_id = "multi-qa-mpnet-base-dot-v1")
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR", default=""),"coffee_embeddings")
    vectorstore = faiss.FAISS.load_local(model_path, embeddings, allow_dangerous_deserialization=True)
    prompt = hub.pull("rlm/rag-prompt")

def run(query):    
    retriever = vectorstore.as_retriever()

    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    def format_docs(docs):
        return "\n\n ".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    ragtext = rag_chain.invoke(query)
    return [ragtext]
    

if __name__ == '__main__':
     init()
     print(run('what is latte'))
