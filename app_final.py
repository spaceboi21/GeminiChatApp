import streamlit as st
import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import base64
from io import BytesIO
from PIL import Image

st.title("MUSA Assistant")

# Set up environment variable for API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCvMhz_NYsHqgKWintdnrDpSO09xb3sy-Q"  # replace with your actual key

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me Anything or upload an image."
        }
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], list) and any(item["type"] == "image_url" for item in message["content"]):
            for item in message["content"]:
                if item["type"] == "image_url":
                    image_data = base64.b64decode(item["image_url"].split(",")[1])
                    image = Image.open(BytesIO(image_data))
                    st.image(image)
        else:
            st.markdown(message["content"])

def llm_function(messages, use_vision_model):
    model_name = "gemini-pro-vision" if use_vision_model else "gemini-pro"
    llm = ChatGoogleGenerativeAI(model=model_name)
    response = llm.invoke([HumanMessage(content=messages)])
    disp = response.content
    
    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(disp)

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
            "content": disp
        }
    )

# Accept user input and uploaded files
query = st.chat_input("Hello! How may I help you today?")
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# System prompt to be prepended
system_prompt = "You are a medical help assistant and have to answer questions regarding the images uploaded in English. You have to talk about the disease and ways to reduce the symptoms and pain. "

# Calling the Function when Input is Provided
if query or uploaded_files:
    message_content = []
    use_vision_model = False  # Flag to decide which model to use

    if query:
        full_user_message = system_prompt + query
        message_content.append({
            "type": "text",
            "text": full_user_message
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
