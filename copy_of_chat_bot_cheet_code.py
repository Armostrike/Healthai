# -*- coding: utf-8 -*-
"""Copy of Chat_Bot_Cheet_Code.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AgCKTfNdvvetq0oraV0rlF3m0WnWC_Py
"""

!pip install langchain
!pip freeze
!pip install langchain-community
!pip install openai
!pip install gradio
!pip install huggingface_hub

import os
import gradio as gr
from langchain.chat_models import ChatOpenAI

from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory

"""**How to get Open AI API Key?**
- Go to https://platform.openai.com/account/api-keys
- Create a new Secret Key
- Copy the Secret Key for your use.
"""

OPENAI_API_KEY="api key"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

template = """
You are a health assistant specialized in nutrition and fitness. Based on the user's condition, provide personalized recommendations that include:
1. Essential vitamins, minerals, and amino acids for their health.
2. Suggested fruits, vegetables, and non-veg sources for these nutrients.
3. Exercise recommendations to improve their condition.

Condition: {user_condition}

For reference, here are some common conditions and their corresponding recommendations:

1. **Diabetes**:
   - **Nutrients**: Fiber, magnesium, omega-3 fatty acids, Vitamin D, Vitamin C, B Vitamins.
   - **Foods**: Berries, leafy greens, fatty fish, whole grains.
   - **Exercises**: Walking, cycling, strength training.

2. **Hypertension**:
   - **Nutrients**: Potassium, magnesium, fiber, omega-3s.
   - **Foods**: Bananas, sweet potatoes, spinach, fatty fish.
   - **Exercises**: Aerobic exercises, swimming, brisk walking.

3. **Anemia**:
   - **Nutrients**: Iron, Vitamin B12, folic acid, Vitamin C.
   - **Foods**: Red meat, spinach, beans, citrus fruits.
   - **Exercises**: Low-impact exercises, yoga, walking.

4. **Osteoporosis**:
   - **Nutrients**: Calcium, Vitamin D, magnesium, Vitamin K.
   - **Foods**: Dairy products, leafy greens, almonds, sardines.
   - **Exercises**: Weight-bearing exercises, yoga, resistance training.

Now based on the user's condition, provide a detailed plan:
User Condition: {user_condition}
User Query: {user_message}
Chatbot Response:
"""

# Define the prompt with the input variables for condition and user query
prompt = PromptTemplate(
    input_variables=["user_condition", "user_message"],
    template=template
)

memory = ConversationBufferMemory(memory_key="chat_history")

"""
- Similar to Open AI Mondel we can also use HuggingFace Transformer Models.
- Reference links: https://python.langchain.com/docs/integrations/providers/huggingface , https://python.langchain.com/docs/integrations/llms/huggingface_hub.html

"""

# from langchain.llms import HuggingFacePipeline
# hf = HuggingFacePipeline.from_model_id(
#     model_id="gpt2",
#     task="text-generation",)

llm_chain = LLMChain(
    llm=ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo"),
    prompt=prompt,
    verbose=True,
    memory=memory,
)

def get_health_response(user_condition, user_message):
    response = llm_chain.predict(user_condition=user_condition, user_message=user_message)
    return response

demo = gr.Interface(
    fn=get_health_response,
    inputs=[
        gr.Textbox(label="Condition (e.g., Diabetes, Hypertension, Anemia, Osteoporosis)", placeholder="Enter your condition"),
        gr.Textbox(label="User Query", placeholder="Ask a question or request specific advice")
    ],
    outputs="text",
    title="Health and Nutrition Assistant",
    description="Get personalized health, nutrition, and fitness advice based on your condition."
)

if __name__ == "__main__":
    demo.launch(debug=True)

"""##**Publishing your code to Hugging Face**"""

from huggingface_hub import notebook_login

notebook_login()

from huggingface_hub import HfApi
api = HfApi()

HUGGING_FACE_REPO_ID = "Ameenux/healthai"

"""**Adding Secret Variables in Hugging Face Account:**

- Open your Space
- Click on Settings Button
- Checkout to **Variables and secrets** section
- Create New Secrets

*Note*: Make sure to add your **OPENAI_API_KEY** in Secret key
"""

# Commented out IPython magic to ensure Python compatibility.
# %mkdir /content/ChatBotWithOpenAI
!wget -P  /content/ChatBotWithOpenAI/ https://s3.ap-south-1.amazonaws.com/cdn1.ccbp.in/GenAI-Workshop/ChatBotWithOpenAIAndLangChain/app.py
!wget -P /content/ChatBotWithOpenAI/ https://s3.ap-south-1.amazonaws.com/cdn1.ccbp.in/GenAI-Workshop/ChatBotWithOpenAIAndLangChain/requirements.txt

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/ChatBotWithOpenAI

api.upload_file(
    path_or_fileobj="./requirements.txt",
    path_in_repo="requirements.txt",
    repo_id=HUGGING_FACE_REPO_ID,
    repo_type="space")

api.upload_file(
    path_or_fileobj="./app.py",
    path_in_repo="app.py",
    repo_id=HUGGING_FACE_REPO_ID,
    repo_type="space")

