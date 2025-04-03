import Bots.s_extract_resume as extract_resume
import Bots.s_extract_profiles as extract_profiles
import Bots.s_scrape_ratings as scrape_ratings
import Bots.s_extract_claimed_ratings as s_extract_claimed_ratings
import Bots.s_assurance_calculator as s_assurance_calculator
import Bots.s_generate_report as generate_report
import Bots.s_generate_questions as s_generate_questions
import os
import json

# Ensure the Output folder exists
output_folder = "Output"
os.makedirs(output_folder, exist_ok=True)

def save_questions_to_json(questions_text, filename="s_generated_questions.json"):
    """ Save the generated questions to a JSON file in the Output folder. """
    output_path = os.path.join(output_folder, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"questions": questions_text}, f, indent=4)
    print(f"✅ Questions saved to {output_path}")

def main(resume_path):
    print("\n📄 Extracting resume information...")
    resume_text = "\n".join(extract_resume.extract_resume_info(resume_path))
    print("✅ Extracted Resume Text")

    print("\n🔍 Extracting claimed ratings...")
    claimed_ratings = s_extract_claimed_ratings.extract_claimed_ratings(resume_text)
    print("✅ Claimed Ratings:", claimed_ratings)

    print("\n🔍 Filtering coding profiles...")
    links = extract_resume.extract_resume_info(resume_path)
    profiles = extract_profiles.filter_coding_profiles(links)
    print("✅ Extracted Profiles:", profiles)

    print("\n📊 Scraping ratings from profiles...")
    actual_ratings = scrape_ratings.scrape_ratings(profiles)
    print("✅ Scraped Ratings:", actual_ratings)

    if not actual_ratings:
        print("❌ Error: No actual ratings found. Exiting.")
        return

    print("\n🔎 Calculating assurance percentage...")
    assurance = s_assurance_calculator.calculate_assurance(claimed_ratings, actual_ratings)
    print(f"✅ Assurance Percentage: {assurance}%")

    candidate_data = {
        "resume": resume_path,
        "profiles": profiles,
        "claimed_ratings": claimed_ratings,
        "actual_ratings": actual_ratings,
        "assurance_percentage": assurance
    }

    print("\n📄 Generating report...")
    generate_report.generate_report(candidate_data)

    # 🔥 Generate questions and save them
    try:
        questions_text = s_generate_questions.generate_questions(actual_ratings)
        print("\n✅ Generated Questions:", questions_text)

        # Save to Output folder
        save_questions_to_json(questions_text)

    except Exception as e:
        print(f"❌ Error generating questions: {e}")

    print("\n✅ All tasks completed successfully!")

if __name__ == "__main__":
    resume_file = "Input/s_resume.pdf"  # Change this to the actual resume file path
    main(resume_file)
