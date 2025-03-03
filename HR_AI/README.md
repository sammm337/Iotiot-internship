# HR Verification Project

## Overview

This project automates the verification of profiles and the generation of interview questions based on GitHub repositories, coding profiles, and LinkedIn data. The project is divided into three main phases:

1. **Verification of Coding Profiles**
2. **Verification of GitHub Repositories**
3. **Verification of LinkedIn Data**

---
## Dependencies
To install all necessary dependencies, run the following command.
```sh
pip install -r requirements.txt
```
---

## Part 1: Verification of Coding Profiles

### Step 1: Extract Resume Information  
- The script **`s_extract_resume.py`** extracts links from the resume.

### Step 2: Filter Coding Profiles  
- The script **`s_extract_profiles.py`** filters coding profiles from the extracted links.

### Step 3: Scrape Ratings from Profiles  
- The script **`s_scrape_ratings.py`** scrapes ratings from the filtered profiles.

### Step 4: Store Data  
- The script **`s_store_data.py`** stores the scraped data in a local file.

### Step 5: Generate Report  
- The script **`s_generate_report.py`** generates a report based on the stored data.

### Running Part 1  
To run all the steps in Phase 1, execute the following command:

```sh
python run_bot.py
```
## Part 2: Verification of GitHub Repositories

### Step 1: Extract Data from GitHub Repositories  
The script **`extraction.py`** extracts data from GitHub repositories.

### Step 2: Verify GitHub Repositories Against Resume Claims  
The script **`verification.py`** verifies the extracted data against the resume claims.

### Step 3: Generate Verification Questions  
The script **`v_generation.py`** generates verification questions based on the verification results.

### Running Part 2  
To run all the steps in Phase 2, execute the following scripts in sequence:

```sh
python Bots/extraction.py
python Bots/verification.py
python Bots/v_generation.py
```

## Part 3: Verification of LinkedIn Data

### Step 1: Test LinkedIn Data  
The script **`p_test.py`** tests the LinkedIn data.

### Step 2: Take Screenshots  
The script **`p_take_screenshots.py`** takes screenshots of the LinkedIn data.

### Step 3: Scrape Images  
The script **`p_scrapimg.py`** scrapes images from the LinkedIn data.

### Running Part 3  
To run all the steps in Phase 3, execute the following scripts in sequence:

```sh
python Bots/p_test.py
python Bots/p_take_screenshots.py
python Bots/p_scrapimg.py
```

## Environment Variables  
Create a `.env` file in the `Bots` directory with the following content:

```ini
GEMINI_API_KEY=your_gemini_api_key_here
AI_MODEL_NAME=gemini-1.5-pro
MAX_TOKENS=2048
TEMPERATURE=0.7
```

## Logs
Logs are stored in the Logs/ directory:

- `hr_verification.log`
- `v_botactivity.log`

## Output  
The output files are stored in the `Output/` directory:

- `fetchedData.json`
- `v_questions.json`
- `p_experience.json`
- `p_output.json`
- `p_hr_questions.md`

## Conclusion  
This project automates the verification of profiles and the generation of interview questions, streamlining the process of evaluating candidates based on their GitHub repositories, coding profiles, and LinkedIn data.
