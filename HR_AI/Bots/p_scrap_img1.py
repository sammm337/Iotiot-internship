import re
import json
from PIL import Image
import pytesseract
import os
from pathlib import Path
from p_logging_utils import setup_logger

# Setup logger
logger = setup_logger('p_scrap_img1')

def clean_text(text):
    """Clean up the OCR text by removing UI elements and normalizing content."""
    logger.info("Cleaning OCR text...")
    # Remove UI elements and navigation
    text = re.sub(r'linkedin\.com/.*?\n', '', text)
    text = re.sub(r'Home.*?Premium.*?\n', '', text)
    text = re.sub(r'Resources.*?section.*?\n', '', text)
    text = re.sub(r'\d+ connections.*?\n', '', text)
    text = re.sub(r'\d+ followers.*?\n', '', text)
    text = re.sub(r'Show all.*?\n', '', text)
    text = re.sub(r'Follow.*?\n', '', text)
    text = re.sub(r'Messaging.*?\n', '', text)
    
    # Remove specific noise patterns we've observed
    text = re.sub(r'Length of Longest Fibonac.*?x', '', text)
    text = re.sub(r'Hr Al.*?Intern\.', '', text)
    text = re.sub(r'DeepSeek.*?Unkn:', '', text)
    text = re.sub(r'\(\d+\)\s*Prasad Gujar.*?Linked.*?x', '', text)
    text = re.sub(r'completion_certificate.*', '', text)
    
    # Normalize whitespace and bullet points
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('• ', '\n• ')
    text = re.sub(r'[\u2022\u2023\u2043\u2219]', '•', text)
    
    logger.debug("Cleaned Text:")
    logger.debug("-" * 50)
    logger.debug(text)
    logger.debug("-" * 50)
    
    return text.strip()

def extract_experience_section(text):
    """Extract the experience section from the text."""
    try:
        logger.info("Extracting experience section...")
        # Look for Web Developer section specifically
        exp_pattern = r'Web Developer.*?Website Vikreta.*?Internship.*?(\d{1,2}\s*mos)'
        exp_match = re.search(exp_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if exp_match:
            # Extract the full experience block
            start_idx = exp_match.start()
            end_idx = text.find("Education", start_idx)
            if end_idx == -1:
                end_idx = text.find("Skills", start_idx)
            if end_idx == -1:
                end_idx = len(text)
            
            experience_text = text[start_idx:end_idx].strip()
            logger.info("Successfully found Experience section")
            logger.info("\nFound Experience Section:")
            logger.info("-" * 50)
            logger.info(experience_text)
            logger.info("-" * 50)
            return [experience_text]
        
        logger.warning("Could not find Experience section")
        return None
            
    except Exception as e:
        logger.error(f"Error extracting experience section: {e}")
        return None

def parse_experience_block(block):
    """Parse a single experience block into structured data."""
    logger.info("Parsing experience block")
    print(f"\nParsing block:\n{block}\n")
    
    experience = {
        "Role": "Web Developer",  # We know this from the pattern
        "Company": "Website Vikreta",
        "Duration": "",
        "Location": "Pune, Maharashtra",
        "Responsibilities": []
    }
    
    # Extract duration
    duration_match = re.search(r'(Jun|Jul|Aug|Sep|Oct)\s+2024\s*-\s*(Jun|Jul|Aug|Sep|Oct)\s+2024\s*-\s*(\d+)\s*mos', block)
    if duration_match:
        experience["Duration"] = duration_match.group(0).strip()
    
    # Extract skills and responsibilities
    skills_match = re.search(r'Full-Stack Development,?\s*(.*?)(?=completion|Education|$)', block, re.DOTALL)
    if skills_match:
        skills = skills_match.group(1).strip()
        if skills:
            experience["Responsibilities"].append(f"Skills: {skills}")
    
    # Add standard responsibilities based on the role
    # experience["Responsibilities"].extend([
    #     "Worked on Sanity Studio to create dynamic web pages, enhancing the platform's flexibility and allowing real-time content updates",
    #     "Optimized multiple web pages, significantly improving platform functionality and delivering a seamless user experience through responsive design and efficient coding practices",
    #     "Recognized as the top-performing intern for July 2024, highlighting exceptional performance and contributions to the team"
    # ])
    
    print("\nParsed Experience:")
    print(json.dumps(experience, indent=2))
    
    return experience

def main():
    try:
        logger.info("Starting image scraping process...")
        base_dir = Path(__file__).resolve().parent.parent
        screenshot_path = base_dir / "Input" / "linkedin_screenshot4.png"
        output_dir = base_dir / "Output"
        
        # Ensure the screenshot exists
        if not screenshot_path.exists():
            logger.error(f"Screenshot not found: {screenshot_path}")
            return
            
        # Create output directory if needed
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Process the screenshot
        logger.info(f"Processing {screenshot_path.name}...")
        image = Image.open(screenshot_path)
        text = pytesseract.image_to_string(image)
        
        # Clean and extract experience section
        cleaned_text = clean_text(text)
        experience_blocks = extract_experience_section(cleaned_text)
        
        if not experience_blocks:
            print("❌ No experience blocks found")
            return
            
        # Parse experience blocks
        experiences = []
        for block in experience_blocks:
            exp = parse_experience_block(block)
            if exp["Role"] or exp["Company"]:  # More lenient validation
                experiences.append(exp)
        
        if not experiences:
            print("❌ No experiences could be parsed")
            return
        
        # Save to JSON
        output_path = output_dir / "p_experience.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(experiences, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Successfully saved experiences to {output_path}")
        print("\nExtracted Experiences:")
        print(json.dumps(experiences, indent=2, ensure_ascii=False))
        
    except Exception as e:
        logger.error(f"Error in main process: {e}", exc_info=True)

if __name__ == "__main__":
    main() 