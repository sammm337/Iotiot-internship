def calculate_assurance(claimed_ratings, actual_ratings):
    matches = 0
    total = len(claimed_ratings)

    for platform, claimed in claimed_ratings.items():
        actual = actual_ratings.get(platform, "Not Found")
        if str(claimed).lower() == str(actual).lower():
            matches += 1

    assurance_percentage = (matches / total) * 100 if total > 0 else 0
    return round(assurance_percentage, 2)

if __name__ == "__main__":
    claimed_ratings = {
        "Codeforces": 1500,
        "LeetCode": "Gold"
    }
    actual_ratings = {
        "Codeforces": 1500,
        "LeetCode": "Gold"
    }
    assurance = calculate_assurance(claimed_ratings, actual_ratings)
    print("Assurance Percentage:", assurance, "%")
