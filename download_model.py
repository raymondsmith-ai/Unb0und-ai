from huggingface_hub import hf_hub_download
from pathlib import Path

# Hugging Face repository
REPO_ID = "mradermacher/Qwen2.5-7B-Instruct-abliterated-GGUF"

# Exact model filename
FILENAME = "Qwen2.5-7B-Instruct-abliterated.Q4_K_M.gguf"

# Create the models folder if needed
models_folder = Path("models")
models_folder.mkdir(exist_ok=True)

print("Downloading OpenMind AI model...")
print("This may take several minutes.\n")

model_path = hf_hub_download(
    repo_id=REPO_ID,
    filename=FILENAME,
    local_dir=str(models_folder)
)

print("\nDownload complete!")
print(f"Model saved to: {model_path}")