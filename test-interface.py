import os
from typing import List, Optional

from llama_index.llms.huggingface import (
    HuggingFaceInferenceAPI,
    HuggingFaceLLM,
)
remotely_run = HuggingFaceInferenceAPI(
    model_name="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2", token='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'
)
completion_response = remotely_run.complete("To infinity, and")
print(completion_response)
# SEE: https://huggingface.co/docs/hub/security-tokens
# We just need a token with read permissions for this demo
# HF_TOKEN: Optional[str] = os.getenv("HUGGING_FACE_TOKEN")
# NOTE: None default will fall back on Hugging Face's token storage
# when this token gets used within HuggingFaceInferenceAPI