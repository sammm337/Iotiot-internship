import re  # Add this line to fix the error
import Bots.s_extract_resume as extract_resume
def filter_coding_profiles(links):
    platforms = {
        "LeetCode": r"https?://leetcode\.com/[\w-]+/?",
        "Codeforces": r"https?://codeforces\.com/profile/[\w-]+",
        "AtCoder": r"https?://atcoder\.jp/users/[\w-]+",
        "GitHub": r"https?://github\.com/[\w-]+/?",
        "CodeChef": r"https?://(?:www\.)?codechef\.com/users/[\w-]+/?"
    }

    extracted_profiles = {}
    for platform, pattern in platforms.items():
        for link in links:
            if re.match(pattern, link):  # Now 're' is defined
                extracted_profiles[platform] = link
                break  # Take the first link found

    return extracted_profiles

if __name__ == "__main__":
    links = extract_resume.extracted_links
    
    profiles = filter_coding_profiles(links)
    print("Extracted Profiles:", profiles)