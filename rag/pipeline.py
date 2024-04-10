from llama_index import VectorStoreIndex, ServiceContext
from llama_index.embeddings import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.llms import Ollama
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.vector_stores.chroma import ChromaVectorStore
import logging
import weaviate
from pydantic import BaseModel
from typing import List
import box
import yaml


def load_embedding_model(model_name):
    embeddings = LangchainEmbedding(
        HuggingFaceEmbeddings(model_name=model_name)
    )
    return embeddings


def build_index(chunk_size, llm, embed_model, weaviate_client, index_name):
    try:
        service_context = ServiceContext.from_defaults(
            chunk_size=chunk_size,
            llm=llm,
            embed_model=embed_model,
            num_output=512,
        )

        vector_store = WeaviateVectorStore(weaviate_client=weaviate_client, index_name=index_name)
        index = VectorStoreIndex.from_vector_store(
            vector_store, service_context=service_context
        )

        return index
    except Exception as e:
        print(f"Error building index: {e}")
        return None

def build_rag_pipeline(debug=False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    try:
        with open('config.yml', 'r', encoding='utf8') as ymlfile:
            cfg = box.Box(yaml.safe_load(ymlfile))
    except FileNotFoundError:
        logging.error("Config file 'config.yml' not found.")
        return None
    logging.info("Loading embedding model...")
    try:
        embeddings = load_embedding_model(model_name=cfg.EMBEDDINGS)
    except Exception as e:
        logging.error(f"Error loading embedding model: {e}")
        return None

    logging.info("Connecting to Weaviate")
    try:
        client = weaviate.Client(cfg.WEAVIATE_URL)
    except Exception as e:
        logging.error(f"Error connecting to Weaviate: {e}")
        return None

    logging.info("Loading Mistral...")
    llm = HuggingFaceInferenceAPI(
        model_name="mistralai/Mistral-7B-Instruct-v0.2",
        token='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',
        context_window=4096,
        max_new_tokens=1024,
        tokenizer_kwargs={"max_length": 4096},
        generate_kwargs={"temperature": 0.1, "do_sample": True},
    )
    logging.info("Building index...")
    index = build_index(cfg.CHUNK_SIZE, llm, embeddings, client, cfg.INDEX_NAME)
    logging.info("Constructing query engine...")
    return index