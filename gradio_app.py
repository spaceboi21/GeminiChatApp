import os
import tempfile
import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import gradio as gr

# Configure the API key (replace with your actual key)
os.environ['GOOGLE_API_KEY'] = "AIzaSyCvMhz_NYsHqgKWintdnrDpSO09xb3sy-Q"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Process and store Query and Response
def llm_function(text, images):
    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
    
    message_content = []
    if text:
        message_content.append({
            "type": "text",
            "text": text
        })
    
    if images:
        for image in images:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image.read())
                image_url = temp_file.name
                message_content.append({
                    "type": "image_url",
                    "image_url": image_url
                })

    response = llm.invoke([HumanMessage(content=message_content)])
    return response.content

# Create Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        text_input = gr.Textbox(show_label=False, placeholder="What's up?")
        image_input = gr.File(file_count="multiple", label="Upload images")
        submit_button = gr.Button("Submit")

    def submit_chat(text, images):
        response = llm_function(text, images)
        chatbot.append(("user", text))
        chatbot.append(("assistant", response))
        return chatbot

    submit_button.click(submit_chat, [text_input, image_input], chatbot)

# Launch the interface with a public link
demo.launch(share=True)
