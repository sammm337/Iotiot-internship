import subprocess
import sys
import time

def run_script(script_path):
    """Run a Python script and handle errors."""
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        sys.exit(1)

def main():
    print("\n🔄 Running s_ scripts via run_bot.py...")
    run_script("run_bot.py")
    time.sleep(10)  # Delay of 5 seconds

    print("\n🔄 Running v_ scripts in sequence...")
    run_script("Bots/v_extraction.py")
    time.sleep(10)  # Delay of 5 seconds
    run_script("Bots/v_verification.py")
    time.sleep(10)  # Delay of 5 seconds
    run_script("Bots/v_generation.py")
    time.sleep(10)  # Delay of 5 seconds

    print("\n🔄 Running p_ scripts in sequence...")
    run_script("Bots/p_test.py")
    time.sleep(10)  # Delay of 5 seconds
    run_script("Bots/p_take_screenshots.py")
    time.sleep(10)  # Delay of 5 seconds
    run_script("Bots/p_scrapimg1.py")
    time.sleep(10)  # Delay of 5 seconds

    print("\n✅ All tasks completed successfully!")

if __name__ == "__main__":
    main()