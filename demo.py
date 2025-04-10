from llama_cpp import Llama

llm = Llama(model_path="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf", n_ctx=512)
output = llm("Q: How are you?\nA:", max_tokens=50)
print(output["choices"][0]["text"])
