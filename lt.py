from litellm import completion
import os

# os.environ["HUGGINGFACE_API_KEY"] = "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"

# e.g. Call 'WizardLM/WizardCoder-Python-34B-V1.0' hosted on HF Inference endpoints
response = completion(
  model="huggingface/WizardLM/WizardCoder-Python-34B-V1.0",
  messages=[{ "content": "Hello, how are you?","role": "user"}],
  api_base="https://my-endpoint.huggingface.cloud"
)

print(response)