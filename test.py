import torch
from model import load_model, predict_intent
import json

# Load the model and tokenizer
model, tokenizer = load_model()  # Đảm bảo rằng đường dẫn đến mô hình là chính xác

# Load intent mapping from intent.json
with open('intent.json', 'r') as f:
    intent_data = json.load(f)
intents = [intent['intent'] for intent in intent_data['intents']]

def test_intent_detection(user_input):
    # Dự đoán ý định từ đầu vào của người dùng
    predicted_intent_index = predict_intent(model, tokenizer, user_input)
    return predicted_intent_index

if __name__ == "__main__":
    while True:
        user_input = input("Nhập câu để kiểm tra ý định (hoặc 'exit' để thoát): ")
        if user_input.lower() == 'exit':
            break
        intent_index = test_intent_detection(user_input)
        intent_label = intents[intent_index] if intent_index < len(intents) else "Unknown"
        print(f"Ý định được dự đoán: {intent_index} - {intent_label}")