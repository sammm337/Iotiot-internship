import json
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import os
from p_logging_utils import setup_logger

# At the start of your file, after imports
logger = setup_logger('generate_hr_questions')

def load_experiences():
    """Load both experience files and return their contents."""
    try:
        base_dir = Path(__file__).resolve().parent.parent
        
        # Load LinkedIn experience
        linkedin_exp_path = base_dir / "Output" / "p_experience.json"
        with open(linkedin_exp_path, 'r', encoding='utf-8') as f:
            linkedin_exp = json.load(f)
            
        # Load Resume experience
        resume_exp_path = base_dir / "Output" / "p_output.json"
        with open(resume_exp_path, 'r', encoding='utf-8') as f:
            resume_exp = json.load(f)['Experience']
            
        logger.info("[SUCCESS] Successfully loaded experience files")
        logger.info(f"LinkedIn Experience: {json.dumps(linkedin_exp, indent=2, ensure_ascii=False)}")
        logger.info(f"Resume Experience: {json.dumps(resume_exp, indent=2, ensure_ascii=False)}")
            
        return linkedin_exp, resume_exp
    except Exception as e:
        logger.error(f"❌ Error loading experience files: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def configure_gemini():
    """Configure the Gemini API with the key from environment variables."""
    try:
        # Load environment variables
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        model_name = os.getenv('AI_MODEL_NAME')
        max_tokens = int(os.getenv('MAX_TOKENS', 2048))
        temperature = float(os.getenv('TEMPERATURE', 0.7))
        
        if not api_key:
            logger.error("❌ AI_API_KEY not found in environment variables")
            return None

        genai.configure(api_key=api_key)
        
        # Configure model settings for Gemini 2.0 Flash
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
            "candidate_count": 1,
        }

        # Use Gemini 2.0 Flash model
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )

        logger.info("[SUCCESS] Successfully configured Gemini model")
        logger.info(f"Model: {model_name}")
        logger.info(f"Max Tokens: {max_tokens}")
        logger.info(f"Temperature: {temperature}")
        return model
    except Exception as e:
        logger.error(f"❌ Error configuring Gemini API: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_questions(model, linkedin_exp, resume_exp):
    """Generate HR questions based on the experiences."""
    try:
        # Prepare the prompt with clear instructions
        prompt = f"""
        Task: Analyze candidate experiences and generate interview questions.

        LinkedIn Experience:
        {json.dumps(linkedin_exp, indent=2, ensure_ascii=False)}

        Resume Experience:
        {json.dumps(resume_exp, indent=2, ensure_ascii=False)}

        Required Analysis:
        1. Compare experiences for discrepancies
        2. Generate technical questions based on mentioned skills
        3. Create behavioral questions based on responsibilities
        4. Provide evaluation criteria for answers

        Format output as markdown with these sections:
        1. Discrepancies Analysis
        2. Technical Questions
        3. Project Questions
        4. Behavioral Questions

        Each question should include:
        - Main question
        - Expected answer points
        - Follow-up questions
        - Red flags to watch for
        """

        logger.info("Generating questions...")
        response = model.generate_content(prompt)
        
        if response.text:
            logger.info("[SUCCESS] Successfully generated questions")
            return response.text
        else:
            logger.error("❌ No response generated")
            return None

    except Exception as e:
        logger.error(f"❌ Error generating questions: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_questions(questions, output_file):
    """Save the generated questions to a file."""
    try:
        with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(questions)
        logger.info(f"[SUCCESS] Questions saved to {output_file}")
    except Exception as e:
        logger.error(f"❌ Error saving questions: {e}")
        import traceback
        traceback.print_exc()

def main():
    # Configure paths
    base_dir = Path(__file__).resolve().parent.parent
    output_file = base_dir / "Output" / "p_hr_questions.md"
    
    # Load experiences
    linkedin_exp, resume_exp = load_experiences()
    if not linkedin_exp or not resume_exp:
        return
    
    # Configure Gemini
    model = configure_gemini()
    if not model:
        return
    
    # Generate questions
    questions = generate_questions(model, linkedin_exp, resume_exp)
    if not questions:
        return
    
    # Save questions
    save_questions(questions, output_file)

if __name__ == "__main__":
    main() 