import streamlit as st
import requests

st.set_page_config(page_title="Legal Assistant Interface")

def get_chat_response(input_text, system_prompt):
    API_URL = "https://api-inference.huggingface.co/models/gpt-3.5-turbo"  # Replace with the model you are using
    headers = {"Authorization": f"Bearer YOUR_HUGGINGFACE_API_TOKEN"}  # Replace with your rag llm API token

    payload = {
        "inputs": f"{system_prompt}\nUser: {input_text}\nAssistant:",
        "parameters": {
            "max_new_tokens": 150,  
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        response_json = response.json()
        generated_text = response_json[0]["generated_text"]
        response_start = generated_text.find("Assistant:") + len("Assistant:")
        output_text = generated_text[response_start:].strip()
        return output_text
    else:
        return "Error: Unable to get response from the model."

def main():
    st.title('Legal Assistant Interface')
    st.subheader("“Your Legal Advisor, Available 24/7—Because Justice Never Sleeps.”" )

   
    with st.sidebar:
        st.title("Configuration")
        system_prompt = st.text_input("Enter System Prompt", value="You are a helpful assistant.")

   
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Dear Sir/Madam How may I assist you today?"}]

   
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

   
    if user_input := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

      
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_chat_response(user_input, system_prompt)
                    st.write(response)
           
            st.session_state.messages.append({"role": "assistant", "content": response})

    
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

if __name__ == '__main__':
    main()
