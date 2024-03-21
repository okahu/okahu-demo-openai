import time
import sys
import os
import ray
import numpy as np
from ray_on_aml.core import Ray_On_AML
from azureml.core import Run
from langchain.document_loaders import BSHTMLLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from embeddings_wrapper import HuggingFaceEmbeddings

DB_SHARDS = 8


@ray.remote(num_cpus=2)
def process_shard(shard):
    print(f"Starting process_shard of {len(shard)} chunks.")
    st = time.time()
    embeddings = HuggingFaceEmbeddings("multi-qa-mpnet-base-dot-v1")
    result = FAISS.from_documents(shard, embeddings)
    et = time.time() - st
    print(f"Shard completed in {et} seconds.")
    return result


if __name__ == "__main__":
    input_data_dir = sys.argv[1]
    output_data_dir = sys.argv[2]

    print("===== DATA =====")
    print("INPUT DATA PATH: " + input_data_dir)
    print("LIST FILES IN DATA DIR...")
    print(os.listdir(input_data_dir))
    print("================")

    run = Run.get_context()
    ws = run.experiment.workspace
    ray_on_aml = Ray_On_AML()
    ray = ray_on_aml.getRay()

    if ray:
        print("head node detected")
        print("test distributed vectorization")
        ray.init(address="auto")
        print("resources for ray cluster ", ray.cluster_resources())

        # load the html files from the input directory
        loader = DirectoryLoader(
            path=input_data_dir, glob="**/*.html", loader_cls=BSHTMLLoader
        )

        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        # Stage one: read all the docs, split them into chunks.
        st = time.time()
        print("Loading documents ...")
        docs = loader.load()
        print(f"The total docs are {len(docs)}")
        # Theoretically, we could use Ray to accelerate this, but it's fast enough as is.
        chunks = text_splitter.create_documents(
            [doc.page_content for doc in docs], metadatas=[doc.metadata for doc in docs]
        )
        et = time.time() - st
        print(f"Time taken: {et} seconds. {len(chunks)} chunks generated")

        # Stage two: embed the docs.
        print(f"Loading chunks into vector store ... using {DB_SHARDS} shards")
        st = time.time()
        shards = np.array_split(chunks, DB_SHARDS)
        futures = [process_shard.remote(shards[i]) for i in range(DB_SHARDS)]
        results = ray.get(futures)
        et = time.time() - st
        print(f"Shard processing complete. Time taken: {et} seconds.")

        st = time.time()
        print("Merging shards ...")
        # Straight serial merge of others into results[0]
        db = results[0]
        for i in range(1, DB_SHARDS):
            db.merge_from(results[i])
        et = time.time() - st
        print(f"Merged in {et} seconds.")

        st = time.time()
        print("Saving faiss index")
        db.save_local(output_data_dir)

        print("===== DATA =====")
        print("OUTPUT DATA PATH: " + output_data_dir)
        print("LIST FILES IN DATA DIR...")
        print(os.listdir(output_data_dir))
        print("================")

        et = time.time() - st
        print(f"Saved in: {et} seconds.")
    else:
        print("in worker node")
