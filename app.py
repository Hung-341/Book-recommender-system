import gradio as gr
from chatbot.validator import validate_user_input  # Updated to reflect the actual module name

# Function to handle user input and return the response
def recommend_book_ui(user_input, history):
    response = validate_user_input(user_input)  # Validate input using NER and intent detection
    history.append((user_input, response))  # Append user input and response to history
    return "", history  # Clear the input and return the updated history

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Book Recommendation System")
    chatbot = gr.Chatbot(label="Book Recommendation Chatbot")  # Create chatbot UI
    user_input = gr.Textbox(label="Enter your book preferences (genre, book title, or author):", 
                             placeholder="Type your question here...")  # Input field
    submit_btn = gr.Button("Send")

    # Initialize history state
    state = gr.State([])

    # Connect components: Input from textbox, output to chatbot history
    submit_btn.click(recommend_book_ui, inputs=[user_input, state], outputs=[user_input, chatbot])
    user_input.submit(recommend_book_ui, inputs=[user_input, state], outputs=[user_input, chatbot])

# Launch the Gradio app
demo.launch(share=True)
