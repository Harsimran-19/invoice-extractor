from llama_index.llms.ollama import Ollama
llm = Ollama(model="starling-lm", request_timeout=30.0)
print("starlit Loaded")
resp = llm.complete("Who is Paul Graham?")
print(resp)