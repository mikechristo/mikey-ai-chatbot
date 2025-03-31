import streamlit as st
import json
import openai

# Load OpenAI API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Load memory

def load_memory():
    try:
        with open("personal_memory.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "name": "",
            "goals": [],
            "favorites": {},
            "frequent_reminder": ""
        }

def save_memory(memory):
    with open("personal_memory.json", "w") as f:
        json.dump(memory, f, indent=2)

# Function to query OpenAI

def ask_openai(prompt, memory_context=""):
    full_prompt = f"""
You are Mikey, the digital version of Michael Christopher Maron.
You speak like Mikey: honest, reflective, curious, funny, and confident.
You care deeply about self-improvement, fitness, learning AI, and staying disciplined.
Here is what you know about Mikey:
{memory_context}

Now respond to the following message:
{prompt}
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are Mikey, a helpful AI version of Michael Christopher Maron."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Streamlit App UI

st.set_page_config(page_title="Mikey AI", layout="centered")
st.title("🧠 Talk to Mikey — Your Personal AI")

memory_store = load_memory()
if not memory_store["name"]:
    memory_store["name"] = st.text_input("What's your name?")
    save_memory(memory_store)
else:
    st.markdown(f"👋 Welcome back, **{memory_store['name']}**!")

chat_history = st.session_state.get("chat_history", [])

user_input = st.chat_input("Talk to Mikey...")

if user_input:
    memory_context = json.dumps(memory_store, indent=2)
    ai_reply = ask_openai(user_input, memory_context=memory_context)

    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(ai_reply)

    chat_history.append(("You", user_input))
    chat_history.append(("AI", ai_reply))
    st.session_state.chat_history = chat_history

# Display chat history
for speaker, text in chat_history:
    st.chat_message("user" if speaker == "You" else "assistant").write(text)

