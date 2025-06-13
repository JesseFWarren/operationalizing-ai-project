import os
import faiss
import numpy as np
from openai import OpenAI
from src.retrieval import search

# OpenAI API key and Client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set OPENAI_API_KEY as an environment variable.")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_response_with_openai(user_query, context):
    """
    Uses OpenAI GPT-4 to generate a response to a health-related query using provided context.
    """
    prompt = f"""
    You are a medical assistant trained on Mayo Clinic data. Use the provided medical context to suggest possible condition, treatment options, 
    and guide the user, but do NOT provide a formal diagnosis. Instead, suggest consulting a healthcare professional. Keep responses to a list of the top 3 likely diseases
    from the provided context. Put spaces/next line inbetween numbers. And before the list introduce that these are the most likely conditions based on reported 
    symptoms. Keep responses concise. 
    Additionally, if the user's symtoms below is just a message without any symptoms listed please ignore the context and reply to the message in a friendly manner.

    Context:
    {context}

    User's Symptoms: {user_query}

    Answer:
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a medical assistant providing guidance based on Mayo Clinic data. You do NOT diagnose users."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


#if __name__ == "__main__":
    #user_input = input("Describe your symptoms: ")
    #print(generate_response_with_openai(user_input))
