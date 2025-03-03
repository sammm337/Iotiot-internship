import google.generativeai as genai
import json
import logging
import os
from dotenv import load_dotenv
load_dotenv()
# File paths
OUTPUT_FILE = "./Output/s_generated_questions.json"
LOG_FILE = "./Logs/botactivity.log"

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API Key Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
    "response_mime_type": "application/json",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

def generate_questions(ratings):
    prompt = f"""
    I am an HR.
    Based on the following coding skill levels:
    {ratings}
    
    Generate 5 coding interview questions with solutions.
    I don't want the code, just the logic.
    Present the output in a structured JSON format with "interviewQuestions" as the root key, and each question-answer pair as objects with keys "Question" and "Answer".
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Parse response as JSON
        structured_data = json.loads(response.candidates[0].content.parts[0].text)
        
        return structured_data.get("interviewQuestions", [])
    except (json.JSONDecodeError, AttributeError, IndexError) as e:
        logging.error(f"Failed to parse LLM response: {e}")
        return None
    except Exception as e:
        logging.error(f"Error querying Gemini: {e}")
        return None

def save_questions_to_json(questions_data, filename=OUTPUT_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(questions_data, f, indent=4)
        print("✅ Questions saved successfully!")
    except Exception as e:
        print(f"❌ Error saving questions: {e}")

if __name__ == "__main__":
    ratings = {"Codeforces": 1500, "LeetCode": "Gold"}
    questions_data = generate_questions(ratings)
    
    if questions_data:
        save_questions_to_json(questions_data)
    else:
        print("❌ No questions generated.")
