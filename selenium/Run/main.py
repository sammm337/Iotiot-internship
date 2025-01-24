import os
import subprocess
import logging

# Set up logging
logging.basicConfig(
    filename=os.path.join("Logs", "botactivity.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    logging.info("Starting all bots...")
    try:
        # Run LinkedIn post bot
        subprocess.run(
    ["python3", os.path.join("Bots", "linkedin_post_bot.py")],
    check=True
)

        logging.info("LinkedIn post bot completed.")
    except Exception as e:
        logging.error(f"An error occurred while running the bots: {e}")

if __name__ == "__main__":
    main()
