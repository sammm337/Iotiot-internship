import re
import Bots.s_extract_resume as extract_resume

def clean_resume_text(resume_text):
    """
    Removes URLs and unnecessary characters from resume text.
    """
    url_pattern = r"https?://[^\s]+"  # Matches URLs
    clean_text = re.sub(url_pattern, "", resume_text)  # Remove URLs
    return clean_text

def extract_claimed_ratings(resume_text):
    """
    Extracts claimed ratings from the cleaned resume text using regex patterns.
    """
    claimed_ratings = {}

    # First, clean the resume text to remove URLs
    cleaned_text = clean_resume_text(resume_text)

    # Updated regex patterns for different coding platforms
    patterns = {
        "Codeforces": r"Codeforces.*?(?:rating|score|:)?\s*(\d{3,4})",
        "LeetCode": r"LeetCode.*?(?:badge|rating|:)?\s*([A-Za-z]+)",
        "CodeChef": r"CodeChef.*?(?:stars?|rating|:)?\s*(\d{3,4})"
    }

    # Extract ratings using regex
    for platform, pattern in patterns.items():
        match = re.search(pattern, cleaned_text, re.IGNORECASE)
        if match:
            claimed_ratings[platform] = match.group(1)  # Extract first capturing group

    return claimed_ratings

if __name__ == "__main__":
    resume_path = "sample_resume.txt"  # Use a text-based resume file for debugging
    resume_text = "\n".join(extract_resume.extract_resume_info(resume_path))  # Convert extracted text to a string
    
    claimed_ratings = extract_claimed_ratings(resume_text)
    print("Extracted Claimed Ratings:", claimed_ratings)
