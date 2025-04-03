import re
import fitz  # PyMuPDF for reading PDFs
import json
import os
from pathlib import Path
from p_logging_utils import setup_logger

# Setup logger
logger = setup_logger('test')

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    try:
        logger.info(f"Extracting text from PDF: {pdf_path}")
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        doc.close()
        return text
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        return ""

def extract_linkedin(text):
    """Extracts LinkedIn profile URL from text."""
    linkedin_pattern = r"(https?://(?:www\.)?linkedin\.com/in/\S+|linkedin\.com/in/\S+)"
    match = re.search(linkedin_pattern, text)
    if match:
        link = match.group(0)
        if not link.startswith("http"):
            link = "https://" + link
        return link
    return None

def get_experience_text(full_text):
    """
    Extracts the Experience section from the full resume text.
    Takes text from the word 'Experience' until the next major header (e.g. Projects, Education).
    """
    lower_text = full_text.lower()
    exp_idx = lower_text.find("experience")
    if exp_idx == -1:
        return ""
    # Find next header among a few common ones
    headers = ["projects", "education", "technical skills", "achievements"]
    ends = [lower_text.find(header, exp_idx) for header in headers if lower_text.find(header, exp_idx) != -1]
    end_idx = min(ends) if ends else len(full_text)
    exp_text = full_text[exp_idx:end_idx]
    exp_text = re.sub(r'(?i)experience', '', exp_text, count=1).strip()
    return exp_text

def parse_experience_section(exp_text):
    """
    Parses the Experience section text into a list of dictionaries.
    It assumes each new experience entry is indicated by a non-bullet line that contains a duration.
    """
    # Split into lines and remove empties
    lines = [line.strip() for line in exp_text.splitlines() if line.strip()]
    entries = []
    current_entry = None

    # Duration regex that matches date ranges; allow different dash characters
    duration_regex = re.compile(
        r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|'
        r'Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}(?:\s*[–-—]\s*'
        r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|'
        r'Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4})?)',
        re.IGNORECASE
    )
    # Regex for location: looks for common location patterns
    location_regex = re.compile(r'(Pune,\s*Maharashtra|Dhule,\s*Maharashtra|India)', re.IGNORECASE)

    i = 0
    while i < len(lines):
        line = lines[i]
        # If the line starts with a bullet, it's a responsibility.
        if line.startswith("•"):
            if current_entry:
                bullet_text = line.lstrip("•").strip()
                current_entry["Responsibilities"].append(bullet_text)
            i += 1
            continue

        # For non-bullet lines, check if they contain a duration pattern (new experience entry)
        duration_match = duration_regex.search(line)
        if duration_match:
            # Save the previous entry if exists
            if current_entry:
                entries.append(current_entry)
            current_entry = {"Role": "", "Duration": "", "Company": "", "Location": "", "Responsibilities": []}
            duration = duration_match.group(0).strip()
            current_entry["Duration"] = duration
            # Role is the text before the duration
            role = line[:duration_match.start()].strip()
            current_entry["Role"] = role

            # Next line is expected to contain the Company (and possibly Location)
            if i + 1 < len(lines):
                comp_line = lines[i+1]
                loc_match = location_regex.search(comp_line)
                if loc_match:
                    loc_start = loc_match.start()
                    company = comp_line[:loc_start].strip()
                    location = comp_line[loc_start:].strip()
                    current_entry["Company"] = company
                    current_entry["Location"] = location
                else:
                    current_entry["Company"] = comp_line.strip()
                i += 2  # Skip the current role/duration line and company line
            else:
                i += 1
        else:
            # If a non-bullet line does not contain a duration, assume it's a continuation of the previous responsibility.
            if current_entry and current_entry["Responsibilities"]:
                current_entry["Responsibilities"][-1] += " " + line
            i += 1

    if current_entry:
        entries.append(current_entry)
    return entries

def extract_experience(full_text):
    """Extracts structured experience details from the full resume text."""
    exp_text = get_experience_text(full_text)
    if not exp_text:
        print("No Experience section found.")
        return []
    print("Extracted Experience Section:")
    print(exp_text)
    return parse_experience_section(exp_text)

def save_resume_info(output_json, pdf_path):
    """Extracts resume details and saves them to a JSON file."""
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return False

    logger.info("Starting resume information extraction...")
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return False

    linkedin = extract_linkedin(text)
    logger.info(f"Found LinkedIn URL: {linkedin}")
    
    experience = extract_experience(text)
    logger.info(f"Extracted {len(experience)} experience entries")

    result = {"LinkedIn": linkedin, "Experience": experience}

    # Create output directory if it doesn't exist
    Path(output_json).parent.mkdir(parents=True, exist_ok=True)

    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)
    
    logger.info(f"Data successfully saved to {output_json}")
    return True

# Update the paths as needed for cross-platform compatibility.
BASE_DIR = Path(__file__).resolve().parent.parent
pdf_path = str(BASE_DIR / "Input" / "candidate_resume.pdf")
output_json = str(BASE_DIR / "Output" / "p_output.json")

if not save_resume_info(output_json, pdf_path):
    print("❌ Failed to process resume")
