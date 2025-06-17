import os

# export USE_BEDROCK=true
USE_BEDROCK = os.getenv("USE_BEDROCK", "false").lower() == "true"

if USE_BEDROCK:
    from src.bedrock_model import generate_response_with_bedrock as generate_response
    MODEL_SOURCE = "Bedrock"
else:
    from src.chatbot import generate_response_with_openai as generate_response
    MODEL_SOURCE = "OpenAI"
