# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps

import streamlit as st
from time import sleep
import requests

def role_write(message_data):

    role, content, img_src, buttons = [message_data["role"] if "role" in message_data else None,
                                      message_data["content"] if "content" in message_data else None,
                                      message_data["img_src"] if "img_src" in message_data else None,
                                      message_data["buttons"] if "buttons" in message_data else None]

    with st.chat_message(role):
        st.markdown(content)

        if img_src:
            st.html("<img style='width: 300px; height: 300px' alt='[Erro]: Falha ao carregar imagem' src='{src}' >".format(src = img_src))


def stream_response_generator(text):
    for word in text.split(' '):
        yield word + " "
        sleep(0.05)


def send_summary_choice(choice):
    st.session_state.messages.append({
        "role": "user",
        "content": choice
    })

    response_post = requests.post("http://localhost:5005/webhooks/rest/webhook", json={"user": "user", "message": choice}).json()

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_post[0]["text"],
        "img_src": response_post[1]["image"] if len(response_post) > 1 else None,
        "buttons": response_button[0]["buttons"] if "buttons" in response_button[0] else None
    })


st.set_page_config(page_title="Pokechat")
st.title("Pokechat")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    role_write(message)

if prompt := st.chat_input("Diga algo..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.html(prompt)


    response_post = requests.post("http://localhost:5005/webhooks/rest/webhook", json={"user": "user", "message": prompt}).json()
    response_text = response_post[0]["text"]
    response_button = response_post[0]["buttons"] if "buttons" in response_post[0] else None
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})


    with st.chat_message("assistant"):
        st.write(response_text)

        if response_button:
            columns = st.columns(len(response_button))
            
            with columns[0]:
                st.button(response_button[0]['title'], type="primary", use_container_width=True, on_click=lambda: send_summary_choice( response_button[0]['payload'] ))
            with columns[1]:
                st.button(response_button[1]['title'], type="primary", use_container_width=True, on_click=lambda: send_summary_choice( response_button[1]['payload'] ))
            with columns[2]:
                st.button(response_button[2]['title'], type="primary", use_container_width=True, on_click=lambda: send_summary_choice( response_button[2]['payload'] ))
            with columns[3]:
                st.button(response_button[3]['title'], type="primary", use_container_width=True, on_click=lambda: send_summary_choice( response_button[3]['payload'] ))
            with columns[4]:
                st.button(response_button[4]['title'], type="primary", use_container_width=True, on_click=lambda: send_summary_choice( response_button[4]['payload'] ))