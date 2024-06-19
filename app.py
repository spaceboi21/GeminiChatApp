import streamlit as st
import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import base64

st.title("Gemini Bot")

os.environ['GOOGLE_API_KEY'] = "AIzaSyCvMhz_NYsHqgKWintdnrDpSO09xb3sy-Q"  # replace with your actual key
# genai.configure(api_key=os.environ['GOOGLE_API_KEY'])  # Assuming genai.configure is handled internally

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me Anything or upload an image."
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process and store Query and Response
def llm_function(messages, use_vision_model):
    model_name = "gemini-pro-vision" if use_vision_model else "gemini-pro"
    llm = ChatGoogleGenerativeAI(model=model_name)
    response = llm.invoke([HumanMessage(content=messages)])

    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response.content)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": messages
        }
    )

    # Storing the Assistant Message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.content
        }
    )

# Accept user input
query = st.chat_input("What's up?")
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Calling the Function when Input is Provided
if query or uploaded_files:
    message_content = []
    use_vision_model = False  # Flag to decide which model to use

    if query:
        message_content.append({
            "type": "text",
            "text": query
        })
        
        # Displaying the User Message
        with st.chat_message("user"):
            st.markdown(query)

    if uploaded_files:
        use_vision_model = True  # Use vision model if there's an uploaded image
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            base64_image = base64.b64encode(bytes_data).decode()
            data_url = f"data:image/png;base64,{base64_image}"  # Convert to data URL
            message_content.append({
                "type": "image_url",  # Change to image_url instead of image_base64
                "image_url": data_url
            })
            
            # Displaying the Uploaded Image
            st.image(data_url)

    llm_function(message_content, use_vision_model)

