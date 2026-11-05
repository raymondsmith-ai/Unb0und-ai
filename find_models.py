from huggingface_hub import HfApi

api = HfApi()

models = api.list_models(
    search="Qwen2.5-7B-Instruct-abliterated-GGUF",
    limit=10
)

print("Available AI Models:\n")

for model in models:
    print(model.id)
    