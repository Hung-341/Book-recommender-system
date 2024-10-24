import torch
import torch.nn as nn
from transformers import AutoTokenizer, BertModel

# Define the BERT classifier model
class BertClassifier(nn.Module):
    def __init__(self, dropout=0.2, num_classes=21):  # Thay đổi num_classes thành 21
        super(BertClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-cased')
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, num_classes)  # Sử dụng kích thước đầu ra của BERT

    def forward(self, input_id, mask):
        _, pooled_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        return linear_output

# Load the model and tokenizer
def load_model(model_path='intent_classification_model.pth'):
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')  # Thay đổi thành 'bert-base-cased'

    # Load the trained model
    model = BertClassifier(num_classes=21)  # Thay đổi num_classes thành 21
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')), strict=False)
    model.eval()  # Set to evaluation mode
    
    return model, tokenizer

# Predict the intent from user input
def predict_intent(model, tokenizer, user_input):
    # Tokenize user input
    tokens = tokenizer(user_input, return_tensors='pt', padding=True, truncation=True)

    # Forward pass through the model
    with torch.no_grad():
        outputs = model(tokens['input_ids'], tokens['attention_mask'])  # Sử dụng input_ids và attention_mask
        predicted_intent = torch.argmax(outputs, dim=1).item()

    return predicted_intent