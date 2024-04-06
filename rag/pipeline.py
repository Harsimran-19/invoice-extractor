from llama_index import VectorStoreIndex, ServiceContext
from llama_index.embeddings import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.llms import Ollama
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.vector_stores.chroma import ChromaVectorStore
import weaviate
from pydantic import BaseModel
from typing import List
import box
import yaml


class InvoiceInfo(BaseModel):
    invoice_number: int
    invoice_date: str
    client_name: str
    client_address: str
    client_tax_id: str
    seller_name: str
    seller_address: str
class InvoiceInfo2(BaseModel):
    names_of_invoice_items: List[str]
class InvoiceInfo3(BaseModel):
    gross_worth_of_invoice_items: List[float]
    total_gross_worth: str
class InvoiceInfo4(BaseModel):
    seller_tax_id: str
    iban: str



def load_embedding_model(model_name):
    embeddings = LangchainEmbedding(
        HuggingFaceEmbeddings(model_name=model_name)
    )
    return embeddings


def build_index(chunk_size, llm, embed_model, weaviate_client, index_name):
    service_context = ServiceContext.from_defaults(
        chunk_size=chunk_size,
        llm=llm,
        embed_model=embed_model,
        num_output=512,
        # context_window=3900
    )

    vector_store = WeaviateVectorStore(weaviate_client=weaviate_client, index_name=index_name)
    # vector_store=ChromaVectorStore

    index = VectorStoreIndex.from_vector_store(
        vector_store, service_context=service_context
    )

    return index


def build_rag_pipeline(debug=False):
    # Import config vars
    with open('config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))
    print("Loading embedding model...")
    embeddings = load_embedding_model(model_name=cfg.EMBEDDINGS)
    print("Connecting to Weaviate")
    client = weaviate.Client(cfg.WEAVIATE_URL)
    print("Loading Ollama...")
    # llm = Ollama(model=cfg.LLM,request_timeout=60.0, temperature=0)
    llm = HuggingFaceInferenceAPI(
        # model_name="HuggingFaceH4/zephyr-7b-beta",
        # model_name="meta-llama/Llama-2-7b-chat-hf",
        model_name="mistralai/Mistral-7B-Instruct-v0.2",
        # model_name="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
        # berkeley-nest/Starling-LM-7B-alpha
        # model_name="https://api-inference.huggingface.co/models/berkeley-nest/Starling-LM-7B-alpha",
        token='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',
        context_window=32000,
        max_new_tokens=1024,
        tokenizer_kwargs={"max_length": 4096},
        generate_kwargs={"temperature": 0.1, "do_sample": True},
    )
    print("Building index...")
    index = build_index(cfg.CHUNK_SIZE, llm, embeddings, client, cfg.INDEX_NAME)

    print("Constructing query engine...")
    # query_engine = index.as_query_engine(
    #     streaming=False,
    #     output_cls=InvoiceInfo,
    #     response_mode="compact"
    # )

    query_engine = index.as_query_engine(
        streaming=False,
        # output_cls=InvoiceInfo,
        response_mode="compact"
    )

    return query_engine
