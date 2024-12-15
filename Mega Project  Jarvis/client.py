from openai import OpenAI

client = OpenAI(
    api_key="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"
)


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a  helpful virtual assistant named jarvis skilled in general task like Alexa and Google Cloud."},
        {
            "role": "user",
            "content": "Write is programming."
        }
    ]
)

print(completion.choices[0].message)