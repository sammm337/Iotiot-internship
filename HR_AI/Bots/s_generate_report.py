import json

def generate_report(candidate_data, output_file="Output/s_report.json"):
    with open(output_file, "w") as f:
        json.dump(candidate_data, f, indent=4)
    print(f"Report saved as {output_file}")

if __name__ == "__main__":
    candidate_data = {
        "name": "Samruddhi Shinde",
        "profiles": {
            "Codeforces": "https://codeforces.com/profile/samruddhishinde222",
            "LeetCode": "https://leetcode.com/u/sam100oo/"
        },
        "ratings": {
            "Codeforces": 1500,
            "LeetCode": "Gold"
        }
    }
    generate_report(candidate_data)
