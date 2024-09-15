import os
import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory

# Set your API key for OpenAI
OPENAI_API_KEY = "your_openai_api_key"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Define the template for the prompt
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

# Define the prompt and memory
prompt = PromptTemplate(
    input_variables=["user_condition", "user_message"],
    template=template
)

memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize the language model and chain
llm_chain = LLMChain(
    llm=ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo"),
    prompt=prompt,
    verbose=True,
    memory=memory,
)

# Function to get health response based on user condition and query
def get_health_response(user_condition, user_message):
    response = llm_chain.predict(user_condition=user_condition, user_message=user_message)
    return response

# Set up Gradio interface
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

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()
