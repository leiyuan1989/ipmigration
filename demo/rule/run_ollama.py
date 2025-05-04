from ollama import Client
client = Client(
  host='http://10.6.126.115:11434',
  # headers={'x-some-header': 'some-value'}
)
# response = client.chat(model='deepseek-r1:32b', messages=[
#   {
#     'role': 'system',
#     'content': 'your are an IC designer',
#   },
# ])


# response = client.generate(model='deepseek-r1:32b', system='your are an IC designer')
# response = client.generate(model='deepseek-r1:32b', 
#                            prompt='who are you',
#                            format="json",
#                            stream=False)

response = client.generate(model='deepseek-r1:32b', 
                           system='your are an IC designer',
                           format="json",
                           stream=False)


import json


# 系统消息
system = "你是一个专业的美食推荐师，使用友好、热情的语言进行回复。"

# 模板消息
template = "请为我推荐适合 {occasion} 的 {cuisine} 美食。"

# 动态数据
data = {
    "occasion": "家庭聚会",
    "cuisine": "意大利"
}

response = client.generate(model='deepseek-r1:32b', 
                           system = system,
                           template = template,
                            prompt='请推荐美食?',
                            format="json",
                            stream=False)
print(response.response)

# 调用 generate 方法
result = client.generate(system, template, data)
print(result)