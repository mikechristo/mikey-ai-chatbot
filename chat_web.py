import streamlit as st
import json
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
import streamlit as st

llm = OpenAI(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model_name="gpt-4",  # You can also use "gpt-3.5-turbo"
    temperature=0.7
)

# Load memory
def load_memory():
    try:
        with open("personal_memory.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"name": "", "goals": []}

def save_memory(memory):
    with open("personal_memory.json", "w") as f:
        json.dump(memory, f, indent=2)

# UI
st.set_page_config(page_title="Personal AI Chatbot", layout="centered")
st.title("🧠 Your Personal AI")

memory_store = load_memory()
if not memory_store["name"]:
    memory_store["name"] = st.text_input("What's your name?")
    save_memory(memory_store)
else:
    st.markdown(f"👋 Welcome back, **{memory_store['name']}**!")

chat_history = st.session_state.get("chat_history", [])

llm = Ollama(model="mistral")
buffer_memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=buffer_memory)

user_input = st.chat_input("Talk to your AI...")

if user_input:
    if "my goal is" in user_input.lower():
        goal = user_input.split("is", 1)[1].strip()
        memory_store["goals"].append(goal)
        save_memory(memory_store)
        ai_reply = "🧠 Got it! I’ll remember that goal."
    else:
        persona = f"""
        You are Mikey - an AI version of Michael Maron 
        You speak like Mikey: honest, reflective, curious, funny, and confident. 
        You care deeply about self-improvement, fitness, learning AI, and staying disciplined.
        You know Mikey's life details: {json.dumps(memory_store, indent=2)}
        If you're talking to someone else, respond as if you are Mikey.
        If you're talking to Mikey himself, reflect his thoughts, encourage his goals, and hold him accountable.
        """
        ai_reply = conversation.run(f"{persona} \n {user_input}")

    chat_history.append(("You", user_input))
    chat_history.append(("AI", ai_reply))
    st.session_state.chat_history = chat_history

# Display chat
for speaker, text in chat_history:
    st.chat_message("user" if speaker == "You" else "assistant").write(text)
