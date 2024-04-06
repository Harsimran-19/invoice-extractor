import timeit
import argparse
from rag.pipeline import build_rag_pipeline
import json
import time
import warnings
import box
import yaml
from llama_index.llms import Ollama

from llama_index.vector_stores import WeaviateVectorStore
import weaviate


warnings.filterwarnings("ignore", category=DeprecationWarning)

# llm = Ollama(model=cfg.LLM,request_timeout=60.0, temperature=0)


def  get_rag_response(chain, debug=False):
    sampleQuery="Give me the information of this invoice in json"
    # print(query)
    query1="retrieve invoice_number,invoice_date,client_address,client_tax_id,seller_name,seller_address in json format"
    query2="names_of_invoice_items in json format"
    query3="gross_worth_of_invoice_items,total_gross_worth json format"
    query4="seller_tax_id,iban,client_name in json format"
    result=chain.query(query1)
    result2=chain.query(query2)
    result3=chain.query(query3)
    result4=chain.query(query4)
    # result = chain.query("give me the invoice data in json format give only json output no other text this json will include invoice number and number of items")
    print(result)
    print(result2)
    print(result3)
    print(result4)
    try:
        # Convert and pretty print
        # data = json.loads(str(result))
        # data = json.dumps(data, indent=4)
        return result
    except (json.decoder.JSONDecodeError, TypeError):
        print("The response is not in JSON format.")

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('input',
    #                     type=str,
    #                     default='What is the invoice number value?',
    #                     help='Enter the query to pass into the LLM')
    parser.add_argument('--debug',
                        action='store_true',
                        default=True,
                        help='Enable debug mode')
    args = parser.parse_args()

    start = timeit.default_timer()

    rag_chain = build_rag_pipeline(False)

    step = 0
    answer = False
    while not answer:
        step += 1
        if step > 1:
            print('Refining answer...')
            # add wait time, before refining to avoid spamming the server
            time.sleep(5)
        if step > 3:
            # if we have refined 3 times, and still no answer, break
            answer = 'No answer found.'
            break
        print('Retrieving answer...')
        answer = get_rag_response(rag_chain, False)

    end = timeit.default_timer()

    print(f'\nJSON answer:\n{answer}')
    print('=' * 50)

    print(f"Time to retrieve answer: {end - start}")