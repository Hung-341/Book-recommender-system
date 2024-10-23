import os
import functools
import random
import google.generativeai as genai
from dotenv import load_dotenv
from data.book import load_books, search_books_by_title, search_books_by_author, search_books_by_genre

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-002")

# Load book data
books = load_books()

@functools.lru_cache(maxsize=1000)
def categorize_input(message):
    prompt = f"""
    Categorize the following message into one of these categories:
    1. Book Recommendation
    2. Greeting
    3. General Conversation
    4. Unclear (hard to understand or ambiguous)
    5. Off-topic (not related to books)

    Respond with only the category number.

    Message: {message}
    """
    try:
        response = model.generate_content(prompt)
        category = response.text.strip()

        categories = ["book_recommendation", "greeting", "general", "unclear", "off-topic"]
        return categories[int(category) - 1]
    except Exception as e:
        print(f"Error in categorize_input: {str(e)}")
        return "general"  # Default to general conversation on error

def validate_input(message):
    try:
        category = categorize_input(message)

        if category in ["book_recommendation", "greeting", "general", "unclear"]:
            return True, category, None
        else:
            return False, "off-topic", None
    except Exception as e:
        print(f"Error in validate_input: {str(e)}")
        return True, "general", None  # Default to general conversation on error

def validate_user_input(user_input):
    user_input = user_input.strip().lower()
    
    if not user_input:
        return "I'm here to help! Could you please provide more details?"

    is_valid, category, _ = validate_input(user_input)

    if category == "greeting":
        return "Hello! How can I assist you today?"
    
    if category == "book_recommendation":
        # Check for specific book requests
        title_results = search_books_by_title(user_input)
        author_results = search_books_by_author(user_input)
        genre_results = search_books_by_genre(user_input)

        recommendations = []
        if title_results:
            recommendations.extend(title_results)
        if author_results:
            recommendations.extend(author_results)
        if genre_results:
            recommendations.extend(genre_results)

        if recommendations:
            # Format the response to include title, author, and description
            response = "I found the following recommendations:\n"
            for book in recommendations:
                response += f"- Title: {book['title']}, Author: {book['author']}, Description: {book['description']}\n"
            return response.strip()
        else:
            # Recommend 3 random books if no matches found
            random_books = random.sample(books, min(3, len(books)))  # Ensure we don't exceed the number of available books
            response = "I'm sorry, but I couldn't find any books matching your request. Here are 3 random book recommendations:\n"
            for book in random_books:
                response += f"- Title: {book['title']}, Author: {book['author']}, Description: {book['description']}\n"
            return response.strip()

    # General conversation
    if category == "general":
        return "That's interesting! What else would you like to discuss?"

    # Unclear conversation
    return "I'm not sure I understand. Could you please clarify your request?"

    # Off-topic conversation
    return "I'm here to help with book recommendations. How can I assist you with that?"