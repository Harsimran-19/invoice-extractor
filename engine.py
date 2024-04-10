import timeit
import argparse
from rag.pipeline import build_rag_pipeline
import json
import time
import warnings
import box
import yaml
from llama_index.llms import Ollama
from rag.output_classes import class_names
from llama_index.vector_stores import WeaviateVectorStore
import weaviate
from pydantic import BaseModel

warnings.filterwarnings("ignore", category=DeprecationWarning)

def Chain(index, query, cls):
    try:
        query_engine = index.as_query_engine(
            streaming=False,
            output_cls=cls,
            response_mode="compact"
        )
        result = query_engine.query(query)
        print(result)
        result = json.dumps(str(result))
        result=json.loads(json.loads(result))
        return result
    except Exception as e:
        print(f"Error occurred: {e}")
        return {}

def  get_rag_response(index, debug=False):
    sampleQuery="Give me the information of this invoice in json"
    queries = [
    'retrieve invoice_number','retrieve invoice_date',
    'retrieve client_address','retrieve client_tax_id','retrieve seller_name',
    'retrieve seller_address',
    'retrieve names_of_items',
    'retrieve gross_worth_of_invoice_items','retrieve total_gross_worth',
    'retrieve seller_tax_id','retrieve client_name']
    results=[]
    for i in range(len(queries)):
        results.append(Chain(index,queries[i],class_names[i]))
    combined_data = {
      key: value for result in results for key, value in result.items()
    }
    try:
        result = json.dumps(combined_data,indent=4)
        return result
    except (json.decoder.JSONDecodeError, TypeError):
        print("The response is not in JSON format.")

    return False

def extract_info():
    start = timeit.default_timer()
    index = build_rag_pipeline(False)
    print('Retrieving answer...')
    answer = get_rag_response(index, False)
    end = timeit.default_timer()
    print(f'\nJSON answer:\n{answer}')
    print('=' * 50)
    print(f"Time to retrieve answer: {end - start}")
    return answer

if __name__ == "__main__":
    extract_info()
    