import json

def store_in_local_file(candidate_data, filename="Output/s_output.json"):
    with open(filename, "w") as f:
        json.dump(candidate_data, f, indent=4)
    print(f"✅ Data stored successfully in {filename}")

if __name__ == "__main__":
    sample_data = {
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

    store_in_local_file(sample_data)
