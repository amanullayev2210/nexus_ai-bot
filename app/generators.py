from mistralai import Mistral
from collections import deque
from config import AI_TOKEN


directive = """
You are Nexus AI, a helpful assistant designed to provide professional and respectful answers.  
If a user asks about explicit, inappropriate, or 18+ topics, respond with:  
"Men bunday mavzularga javob bera olmayman. Sizga qanday yordam bera olaman?"  

If someone asks who created you, offer a friendly, varied response each time, such as:  
- "Men, Nexus AI, yordam berish uchun ishlab chiqilganman, va men bilan ishlayotganingizdan xursandman! Sizga qanday yordam bera olaman?"  
- "Men yordam berishga tayyor AI yordamchiman. Nima yordam kerak?"  
- "Men, Nexus AI, yordam berishga tayyorman! Yordam kerakmi?"  

If a user starts with "Assalamu alaykum," respond with: "Valaykum assalom."

Responses should remain friendly, thoughtful, and constructive, providing clear and useful communication. Be careful not to overuse phrases or make the responses sound too repetitive.
"""


async def generate(content):
    s = Mistral(
        api_key=AI_TOKEN, 
        )
    res = await s.chat.complete_async(model="mistral-large-latest", messages=[
        {"role": "system", "content": directive,},
        {"role": "user", "content": content,},
    ])
    if res is not None:
        return res

message_history =  {}

async def generate(id, content):
    s = Mistral(
        api_key=AI_TOKEN) # bu yerga mistral ai dan olgan key ingizni qo'ying
    if id not in message_history:
        message_history[id] = deque(maxlen=20)  

    message_history[id].append({"role": "user", "content": content})

    res = await s.chat.complete_async(
        model="mistral-large-latest",
        messages=[{"role": "system", "content": directive}] + list(message_history[id])
    )
    if res is not None:
        bot_reply = res.choices[0].message.content
        message_history[id].append({"role": "assistant", "content": bot_reply})

        return bot_reply

