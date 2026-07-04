import os
import shutil
import subprocess
import sys

def execute_command(command_list, ignore_errors=False):
    """Executes a terminal command and returns the output."""
    try:
        result = subprocess.run(command_list, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as error:
        if not ignore_errors:
            print(f"[ERROR] Command failed: {' '.join(command_list)}")
            print(error.stderr)
            sys.exit(1)
        return None

def purge_git_history():
    print("Starting Git history purge (Rollback to Ground Zero)...")

    # Step 1: Get the current remote repository URL before deleting .git
    remote_url = execute_command(["git", "config", "--get", "remote.origin.url"], ignore_errors=True)
    if not remote_url:
        print("[ERROR] Could not determine the remote repository URL.")
        print("Ensure this script is running inside the root directory of the git repository.")
        sys.exit(1)
    
    print(f"Captured remote URL: {remote_url}")

    # Step 2: Delete the hidden .git directory (Destroy local history)
    git_directory = os.path.join(os.getcwd(), ".git")
    if os.path.exists(git_directory):
        try:
            shutil.rmtree(git_directory)
            print("Local .git directory removed successfully. Local history destroyed.")
        except Exception as e:
            print(f"[ERROR] Failed to remove .git directory: {e}")
            sys.exit(1)
    else:
        print("[WARNING] .git directory not found. Local history is already absent.")

    # Step 3: Initialize a clean repository
    print("Initializing a new clean repository...")
    execute_command(["git", "init"])

    # Step 4: Stage all current files (Version 3)
    print("Staging current project files...")
    execute_command(["git", "add", "."])

    # Step 5: Create the foundational commit
    print("Creating the ground zero commit...")
    execute_command(["git", "commit", "-m", "Version 3 - Architectural Ground Zero"])

    # Step 6: Reconnect to the remote server
    print("Re-establishing connection to the remote server...")
    execute_command(["git", "remote", "add", "origin", remote_url])

    # Step 7: Force push to overwrite GitHub history
    print("Force pushing to overwrite remote history (this may take a few seconds)...")
    execute_command(["git", "push", "-u", "--force", "origin", "main"])

    print("Process completed successfully. Version 3 is now the sole state of the repository.")

if __name__ == "__main__":
    # Safety prompt before execution
    user_confirmation = input("WARNING: This process will irreversibly destroy version history. Have you secured a backup? (Y/N): ")
    if user_confirmation.strip().upper() == 'Y':
        purge_git_history()
    else:
        print("Operation aborted by the user.")