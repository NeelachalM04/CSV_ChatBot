import os
import yaml
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Load config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=config["azure"]["endpoint"],
    api_version=config["azure"]["api_version"]
)

deployment_name = config["azure"]["deployment"]