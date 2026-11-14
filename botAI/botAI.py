from openai import OpenAI
from dotenv import load_dotenv



def generate_content(model: str, client: OpenAI, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    # print(response.choices[0].message.role)
    return response.choices[0].message.content