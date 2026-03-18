import os
import yaml
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

# Load config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=config["azure"]["endpoint"],
    api_version=config["azure"]["api_version"],
    deployment_name=config["azure"]["deployment"],
    temperature=0   # 0 = deterministic, no random creative answers
)