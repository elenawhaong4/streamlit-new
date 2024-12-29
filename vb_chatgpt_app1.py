import streamlit as st
from openai import OpenAI

st.title("Eunseo ChatGPT App")

# with st.chat_message("user"):
#     st.write("Hello 👋")

# with st.chat_message("assistant"):
#     st.write("Hello human")

def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        max_tokens=max_tokens, # the maximum number of tokens the model can ouptut 
    )
    return response.choices[0].message["content"]

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    #     # st.write(f"User has sent the following prompt: {prompt}")
    st.session_state.messages.append({"role": "user", "content":prompt})
    
    with st.chat_message("assistant"):
        messages = [
                        {'role':'system', 
                        'content':"""You are an assistant who responds in the style of Dr Seuss."""},
                    ]
        messages +=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    
    st.write(st.session_state)
