import spacy
import re
from model import load_model, predict_intent
from data.book import search_books_by_title, search_books_by_author, search_books_by_genre
import json

# Load pre-trained spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Predefined list of genres
GENRES = ["fiction", "mystery", "fantasy", "science fiction", "romance", "thriller", "non-fiction"]

# Load intent mapping from intent.json
with open('intent.json', 'r') as f:
    intent_data = json.load(f)
intents = [intent['intent'] for intent in intent_data['intents']]

# Load the model and tokenizer
model, tokenizer = load_model()  

# Function to extract named entities (book titles, authors) using spaCy NER
def extract_entities(user_input):
    doc = nlp(user_input)
    entities = {"book_titles": [], "authors": [], "genres": []}

    for ent in doc.ents:
        if ent.label_ == "WORK_OF_ART":  # Book titles
            entities['book_titles'].append(ent.text)
        elif ent.label_ == "PERSON":  # Author names
            entities['authors'].append(ent.text)

    # Simple genre matching
    for genre in GENRES:
        if genre.lower() in user_input.lower():
            entities['genres'].append(genre)

    return entities

# Function to validate user input and handle detected intent
def validate_user_input(user_input):
    user_input = user_input.strip().lower()

    if not user_input:
        return "I'm here to help! Could you please provide more details?"

    # Use the trained model to detect the intent
    predicted_intent_index = predict_intent(model, tokenizer, user_input)
    detected_intent = intents[predicted_intent_index]

    if detected_intent == "Author Search":
        author_results = search_books_by_author(user_input)
        if author_results:
            response = f"Books by {author_results[0]['author']}: '{author_results[0]['title']}'."
        else:
            response = "Sorry, I couldn't find books by that author."
        return response

    elif detected_intent == "Recommendation Request":
        genre_results = search_books_by_genre(user_input)
        if genre_results:
            response = f"I recommend '{genre_results[0]['title']}' by {genre_results[0]['author']}."
        else:
            response = "Sorry, I couldn't find any recommendations."
        return response

    elif detected_intent == "CurrentHumanQuery":
        return "I believe you are the user I’m interacting with. How can I help you?"

    elif detected_intent == "CourtesyGreetingResponse":
        return "Great! How can I assist you further?"

    elif detected_intent == "Thanks":
        return "You're welcome! Let me know if you need anything else."

    elif detected_intent == "Greeting":
        return "Hello! How can I assist you today?"

    elif detected_intent == "Ask for Information About Book":
        title_results = search_books_by_title(user_input)
        if title_results:
            response = f"'{title_results[0]['title']}' by {title_results[0]['author']} is about {title_results[0]['description']}."
        else:
            response = "Sorry, I don't have information about that book."
        return response

    elif detected_intent == "GoodBye":
        return "Goodbye! Come back again soon."

    elif detected_intent == "Genre Search":
        genre_results = search_books_by_genre(user_input)
        if genre_results:
            response = f"Here are some popular books in that genre: '{genre_results[0]['title']}' by {genre_results[0]['author']}."
        else:
            response = "Sorry, I couldn't find books in that genre."
        return response

    elif detected_intent == "Search for Book":
        return "Sure! Can you provide a title, genre, or author?"

    elif detected_intent == "TimeQuery":
        return "I can't provide the time at the moment, but I can help with book recommendations."

    elif detected_intent == "NotTalking2U":
        return "OK, let me know when you need my assistance."

    elif detected_intent == "GreetingResponse":
        return "Great! How can I help you?"

    elif detected_intent == "CourtesyGoodBye":
        return "You're welcome! Goodbye!"

    elif detected_intent == "Ask for Book":
        title_results = search_books_by_title(user_input)
        if title_results:
            response = f"Yes, we have '{title_results[0]['title']}' by {title_results[0]['author']} available."
        else:
            response = "Sorry, I couldn't find the book you're asking for."
        return response

    elif detected_intent == "Discuss Book Genres":
        return "Great! I love discussing genres. What kind of books do you like?"

    elif detected_intent == "UnderstandQuery":
        return "Yes, I understand! How can I assist you further?"

    elif detected_intent == "RealNameQuery":
        return "You can call me Book Helper. How can I assist you?"

    elif detected_intent == "NameQuery":
        return "You can call me Book Helper!"

    elif detected_intent == "Swearing":
        return "Please refrain from using offensive language."

    elif detected_intent == "CourtesyGreeting":
        return "Hello! How can I help you today?"

    else:
        return "I'm not sure I understand. Could you please clarify your request?"