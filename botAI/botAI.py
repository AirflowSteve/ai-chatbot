from openai import OpenAI




def generate_content(client: OpenAI, messages):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )
    # print(response.choices[0].message.role)
    return response.choices[0].message.content