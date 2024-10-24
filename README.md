
# Book Recommendation Chatbot 

## Features

## Requirements
Before running the project, make sure you have the following installed:

- Python 3.7+
- PyTorch
- Transformers (for BERT-based tokenization)
- spaCy (for NER)
- Gradio (for the UI)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Hung-341/Book-recommender-system.git
   cd Book-recommender-system
   ```

2. **Install Required Packages**:
   Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the spaCy Language Model**:
   The chatbot uses `spaCy` for Named Entity Recognition. You need to download the English language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Prepare the Model**:
   Make sure you have the trained intent classification model available in the root directory as `intent_classification_model.pth`.

## How to Run

1. **Run the Application**:
   After setting up the environment, run the Gradio app to launch the chatbot:
   ```bash
   python app.py
   ```

2. **Using the Chatbot**:

## File Overview

- **`app.py`**: The main application file that runs the Gradio-based chatbot interface.
- **`model.py`**: Contains the PyTorch model for intent detection and functions to load the model and make predictions.
- **`validator.py`**: Handles the logic for validating user input, detecting intents, extracting entities (like book titles and authors), and generating responses.