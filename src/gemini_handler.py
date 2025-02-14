import requests
import random
import re
from src.config import GEMINI_API_KEY


def preprocess_raw_text(raw_text):
    """
    Cleans up the raw OCR text before sending it to Gemini API.
    Removes leading "QUIZ TIME" or similar prefixes.
    """
    # Remove common "QUIZ TIME" patterns (case-insensitive)
    cleaned_text = re.sub(r"(?i)^quiz\s*time[:\- ]*", "", raw_text.strip())
    return cleaned_text


def clean_quiz_text_with_gemini(raw_text):
    """
    Use Gemini API to clean and correct noisy OCR-extracted quiz text.
    """
    prompt = f"""
    The following is a quiz question extracted from an image. It may contain spelling errors or be incomplete.
    Please correct any mistakes and complete the quiz if necessary.
    Ensure the output is in this format:
    
    Question?

    A) Option 1
    B) Option 2
    C) Option 3
    D) Option 4

    Here is the quiz text to fix:
    {raw_text}

    Return only the corrected and completed quiz text in the exact format specified above.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    cleaned_text = result['candidates'][0]['content']['parts'][0]['text'].strip()

    return cleaned_text


def extract_title_description_tags_from_quiz_text(cleaned_text):
    """
    Generate YouTube Title, Description, and Tags based on cleaned quiz text.
    """
    lines = cleaned_text.splitlines()

    # Extract the question from the first line
    question = lines[0].strip()

    # Generate Title (Ensure it's under 100 characters)
    base_title = f"Quiz time: {question}"
    title = f"{base_title} #shorts"
    if len(title) > 100:
        title = base_title[:90] + " #shorts"

    # Generate Description
    description = f"{question}\n\n"
    description += "\n".join(lines[1:]) + "\n\n"
    description += "Comment your answer below!\n"
    description += "Like and subscribe for more quizzes and coding challenges!\n\n"
    description += "#Quiz #CodingQuiz #Programming #Learning #Shorts"

    # Randomized Tags
    tag_pool = [
        'quiz', 'programming', 'coding', 'learning', 'shorts',
        'computer science', 'data structures', 'coding challenge',
        'programming quiz', 'cs basics', 'algorithms', 'tech quiz'
    ]
    tags = random.sample(tag_pool, 5)

    return title, description, tags


if __name__ == '__main__':
    raw_ocr_text = """
    QUIZ TIME:
    Hw is n elemnt accesd in an rray?

    A) By usng the elemnt value dirctly
    B) By usng an index numbr
    C) By usng te array sze
    D) By usng a point
    """

    try:
        # 1. Preprocess OCR text to remove "QUIZ TIME"
        preprocessed_text = preprocess_raw_text(raw_ocr_text)

        # 2. Clean the quiz text
        cleaned_text = clean_quiz_text_with_gemini(preprocessed_text)
        print(f"✅ Cleaned Quiz Text:\n{cleaned_text}\n")

        # 3. Generate metadata
        title, description, tags = extract_title_description_tags_from_quiz_text(cleaned_text)

        # 4. Display output
        print(f"✅ Title: {title}")
        print(f"✅ Description:\n{description}")
        print(f"✅ Tags: {tags}")

    except Exception as e:
        print(f"❌ Error: {e}")
