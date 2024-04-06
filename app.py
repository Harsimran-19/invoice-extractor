from flask import Flask, request, jsonify
import json
from rag.pipeline import build_rag_pipeline
import warnings
import threading

def execute_query(query,chain):
    result=chain.query(query)
    return result
    # Simulate the query execution, replace with actual query execution code
    # In this example, simply printing the query is simulated
    # print("Executing query:", query)
    # # Replace this with actual query execution code and return result
    # return "Result for query: " + query
warnings.filterwarnings("ignore", category=DeprecationWarning)
# llm = Ollama(model=cfg.LLM,request_timeout=60.0, temperature=0)
def multi(query,chain):
    queries = [q.strip() for q in input_query.split(',')]
    results = []
    print(queries)
    # Define a function to be executed by each thread
    def execute_and_append(query):
        result = execute_query(query,chain)
        results.append(result)
    # Create and start a thread for each query
    threads = []
    for query in queries:
        thread = threading.Thread(target=execute_and_append, args=(query,))
        threads.append(thread)
        thread.start()
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Concatenate the results
    final_result = '\n'.join(results)

def get_rag_response(query, chain, debug=False):
    result=multi(query,chain)
    # print(query)
    # result=chain.query(query)
    # result = chain.query("give me the invoice data in json format give only json output no other text this json will include invoice number and number of items")
    print(result)
    try:
        # Convert and pretty print
        data = json.loads(str(result))
        data = json.dumps(data, indent=4)
        return result
    except (json.decoder.JSONDecodeError, TypeError):
        print("The response is not in JSON format.")

    return False

app = Flask(__name__)


@app.route('/ask', methods=['POST'])
def ask():
    query = request.json['query']
    rag_chain = build_rag_pipeline()
    answer = get_rag_response(query, rag_chain)
    return answer

if __name__ == '__main__':
    app.run(debug=True, port=3000)