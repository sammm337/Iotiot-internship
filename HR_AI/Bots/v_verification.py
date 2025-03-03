import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
INPUT_FILE = "./Input/v_input.json"
OUTPUT_FILE = "./Output/v_output.json"
FETCHED_DATA_FILE = "./Config/v_fetchedData.json"
QUESTIONS_FILE = "./Output/v_questions.json"
LOG_FILE = "./Logs/v_botactivity.log"

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if the API key is available
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set in the environment variables.")

# Configure Gemini API
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
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

def load_json(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {file_path}")
        return None

def generate_question_prompt(resume_project, github_data, verification_result):
    """Generate a prompt for the LLM to create interview questions."""
    prompt = f"""
    You are an HR assistant tasked with generating interview questions based on a candidate's resume and GitHub repository.
    
    **Resume Claim:**
    - Project Name: {resume_project["name"]}
    - Description: {resume_project["description"]}
    - Claimed Skills: {', '.join(resume_project["skills"])}
    
    **GitHub Data:**
    - Repository Name: {github_data["repo_name"]}
    - Languages Used: {', '.join(github_data["languages"].keys())}
    - Commit Count: {len(github_data["commits"])}
    - Main Contributors: {', '.join([c['username'] for c in github_data["contributors"]])}
    
    **Verification Results:**
    - Score: {verification_result["score"]}
    - Matched Skills: {', '.join(verification_result["matched_skills"])}
    - Missing Skills: {', '.join(verification_result["missing_skills"])}
    - Main Contributor: {verification_result["main_contributor"]}
    
    **Task:**
    Generate a JSON response containing:
    - One or Two technical questions relevant to the project domain.
    - One or Two discrepancy-based question if there are missing skills, low commit count, or other inconsistencies.
    - Provide pointers to the HR that will help them verify the candidate's answer, don't give complete answer, just concise pointers like keywords or critical concepts.
    
    Return JSON in the format:
    {{
        "questions": [
            {{"question": "...", "answer": "...", "type": "technical"}},
            {{"question": "...", "answer": "...", "type": "technical"}},
            {{"question": "...", "answer": "...", "type": "discrepancy"}}
        ]
    }}
    """
    return prompt.strip()

def query_gemini(prompt):
    """Query Gemini API to generate questions."""
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except json.JSONDecodeError:
        logging.error("Failed to parse LLM response.")
        return None
    except Exception as e:
        logging.error(f"Error querying Gemini: {str(e)}")
        return None

def main():
    """Main function to generate interview questions."""
    logging.info("Starting question generation process...")
    
    input_data = load_json(INPUT_FILE)
    github_data_list = load_json(FETCHED_DATA_FILE)
    verification_results = load_json(OUTPUT_FILE)
    
    if not input_data or not github_data_list or not verification_results:
        logging.error("Missing required input data. Aborting process.")
        return
    
    repos = input_data.get("repos", [])
    if not repos:
        logging.error("No repository data found in input. Aborting process.")
        return
    
    all_questions = []
    
    for repo_info, github_data, verification_result in zip(repos, github_data_list, verification_results):
        resume_project = repo_info.get("resume_project")
        if not resume_project:
            logging.error(f"No resume project data found for repo {repo_info.get('repo_name')}. Skipping.")
            continue
        
        prompt = generate_question_prompt(resume_project, github_data, verification_result)
        questions_response = query_gemini(prompt)
        
        if questions_response:
            all_questions.append({
                "repo_name": repo_info.get("repo_name"),
                "questions": questions_response["questions"]
            })
        else:
            logging.error(f"Question generation failed for repo {repo_info.get('repo_name')}. No valid response from LLM.")
    
    if all_questions:
        with open(QUESTIONS_FILE, "w") as file:
            json.dump(all_questions, file, indent=4)
        logging.info("Question generation process completed successfully.")
    else:
        logging.error("Question generation failed. No valid responses from LLM.")

if __name__ == "__main__":
    main()