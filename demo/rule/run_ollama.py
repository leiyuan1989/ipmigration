from ollama import Client
client = Client(
  host='http://10.6.126.115:11434',
  # headers={'x-some-header': 'some-value'}
)
response = client.chat(model='deepseek-r1:32b', messages=[
  {
    'role': 'system',
    'content': 'who are you?',
  },
])
print(response)

response = client.generate(model='deepseek-r1:32b', prompt='Why is the sky blue?')
