from openai import OpenAI

client = OpenAI()


def gpt3_chat(content):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": content,
            },
        ],
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    result = gpt3_chat(content="what is a solar eclipse?")
    print(result)
