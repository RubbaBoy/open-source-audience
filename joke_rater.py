import openai
import re

api_key = ""
joke_prompt = """
I will give you a string that will either be a joke or not. If it is not,
respond with "NOT A JOKE". If it is, only respond with a number 1-10 rating
on how funny the joke is, 1 being not funny (i.e. overly complicated or mundane)
and 10 being funny (dumb stuff is considered funny). The response should only be 0-10 or
"NOT A JOKE". with no additional words or context The string is:

%s
"""
pattern = r'\b\d+\b'


def joke_rater(joke):
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": joke_prompt % joke}]
    )

    reply = chat.choices[0].message.content

    if reply in 'NOT A JOKE':
        return None

    match = re.search(pattern, reply)
    if match:
        return int(match.group())

    print(f'Invalid response by ChatGPT:\n\n{reply}')
    return None
