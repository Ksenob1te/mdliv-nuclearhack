from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama

'''class NeuroRequest(BaseModel):
    webhook: str
    content: str
    base_prompt: str
    ray_id: str'''

request = {"webhook": "hook228-omg",
           "content": "Какой пассажиропоток был на станции некрасовка 20.04.2024 в обед?",
           "ray_id": 123}

date = "20.04.2024"
station = "Некрасовка"
passengers = 50

prompt_category = \
f"""
You are a worker in the call center
You've got a request from your client: "{request['content']}", - first of all you need to classify what parameters user provided for you. 
You know, that in your prompt can be the name of selected metro station, metro line or it's number. 

Now your task is to fill the information from user request to our system.
Provide JSON file with corresponding format:
[{'{'}'station': 'station_name1', 'line': 'line1', 'line_number': number1 {'}'}, ..., ..., ...]
you need to answer with ONLY Json file, also there can be as much elements in the array as you think needed (from 1 to 5 for each station)
for every station that you think is right for user request, if user didn't provide some information corresponding field should be None,
be careful, you need to provide only true information, you will be greatly paid if you do it right!
"""

# prompt_category = f"Отнеси это сообщение: \"{request['content']}\" к одной из категорий:" \
#                   f"1. В сообщении есть время, день и станция" \
#                   f"2. В сообщении есть время и день, но нет станции" \
#                   f"3. В сообщении есть время и станция, но нет дня" \
#                   f"4. В сообщении есть станция и день, но нет времени" \
#                   f"5. В сообщении есть станция, но нет дня и времени" \
#                   f"6. В сообщении есть день, но нет времени и станции" \
#                   f"7. В сообщении есть время, но нет станции и дня" \
#                   f"8. В сообщении нет ни дня, ни станции, ни времени" \
#                   f"К времени также относится время суток, к дню относятся понятия вчера, сегодня, завтра"

prompt = f"В качестве ответа на {request['content']} сформируй json файл в формате \"webhook\": {request['webhook']}, \"result\": your response, \"ray_id\": {request['ray_id']}" \
         f"значение в поле result пиши на русском языке" \
         f"Зная, что в дату {date} на станции {station} пассажиропоток был {passengers}."

llm = Llama(
    # model_path="./ggml-vic7b-uncensored-q4_0.bin",
    model_path="codellama-7b-instruct.Q4_K_S.gguf",
    n_gpu_layers=-1,
    split_mode=0,
    use_mlock=True,
    n_batch=256,
    n_ctx=1024,
    n_threads=10
)

llm_response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "Ты отлично классифицируешь сообщения по категориям."},
        {
            "role": "user",
            "content": prompt_category
        }
    ],
)
first_response = llm_response['choices'][0]['message']['content']
print(first_response)
# for i in range(2, 9):
#     if i in llm_response:
#         print("incorrect question")
#         print(first_response)
llm_response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "Ты отлично классифицируешь сообщения по категориям."},
        {
            "role": "user",
            "content": prompt_category
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
)
second_response = llm_response['choices'][0]['message']['content']
print(second_response)
# print(llm_response['choices'][0]['message']['content'])
