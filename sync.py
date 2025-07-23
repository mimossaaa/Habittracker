
import subprocess
from datetime import datetime

def sync_data():
    """
    Adds, commits, and pushes the habits.json file to the remote repository.
    """
    try:
        # Add the habits.json file to the staging area
        subprocess.run(["git", "add", "habits.json"], check=True)

        # Commit the changes with a timestamp
        commit_message = f"Update habit data for {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes to the remote repository
        subprocess.run(["git", "push"], check=True)

        print("Successfully synced habit data to the remote repository.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while syncing data: {e}")
    except FileNotFoundError:
        print("Git is not installed or not in your PATH. Please install Git and try again.")

if __name__ == "__main__":
    sync_data()
