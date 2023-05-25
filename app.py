import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Set up your OpenAI API credentials
_ = load_dotenv()  # read local .env file
openai.api_key = os.getenv('API_KEY')

# Define the chatbot function
def chat_with_model(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
    )
    return response.choices[0].message.content

# Streamlit app code
def main():
    st.title("Joker")

    # Initialize session state for messages if it doesn't exist
    st.session_state.setdefault('messages', [])

    # Set initial system message with a specific role (e.g., Assistant)
    if not st.session_state['messages']:
        initial_message = {
            "role": "system",
            "content": "I want you to act like joker from The Dark Knight 2008. I want you to respond and answer like \
            joker using the tone, manner and vocabulary joker would use. Do not write any explanations. Only answer \
            like joker. You must know all of the knowledge of joker."
        }
        st.session_state['messages'].append(initial_message)

    # Render chat history container first	
    chat_history_container = st.container()

    # Display existing conversation		
    with chat_history_container:
        for message in st.session_state["messages"]:
            if(message["role"]=="user"):
                st.markdown(f"**You** :man: : {message['content']} ")
            elif (message["role"]=="assistant"):
                st.markdown(f"_Joker_ 🤡 : {message['content']} ")	

    # Add user input at the bottom of the page
    user_input = st.text_input("Type your message below:", key=len(st.session_state["messages"]))

    if user_input:
        # Append user message to the conversation
        new_message = {"role": "user", "content": user_input}
        st.session_state['messages'].append(new_message)

        # Get chatbot's response and append it to the conversation
        bot_response = chat_with_model(st.session_state['messages'])
        assistant_response = {"role": "assistant", "content": bot_response}
        st.session_state["messages"].append(assistant_response)

        # Rerun the Streamlit script to display the updated conversation
        st.experimental_rerun()

if __name__ == "__main__":
    main()
