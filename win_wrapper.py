import os
import subprocess
import sys

SETUP_FLAG = ".setup_done"

def run_command(command, shell=False):
    try:
        result = subprocess.run(command, shell=shell, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def run_setup():
    print("Running first-time setup...")

    if not run_command(["where", "python"]):
        print("Python not found. Please install Python from https://www.python.org/downloads/")
        sys.exit(1)

    if not run_command(["ollama", "--version"]):
        print("Ollama not found. Install Ollama from https://ollama.com/download/")
            sys.exit(1)

    if not os.path.exists("venv"):
        run_command(["python", "-m", "venv", "venv"])

    if os.name == "nt":  # Windows
        activate_cmd = r"venv\Scripts\activate.bat"
        pip_install_cmd = f"{activate_cmd} && pip install -r requirements.txt"
        run_command(pip_install_cmd, shell=True)
    
    with open(SETUP_FLAG, "w") as f:
        f.write("Setup complete")

def run_app():
    print("Launching the app...")
    if os.name == "nt":
        activate_cmd = r"venv\Scripts\activate.bat"
        streamlit_cmd = f"{activate_cmd} && streamlit run app.py"
        run_command(streamlit_cmd, shell=True)

if __name__ == "__main__":
    if not os.path.exists(SETUP_FLAG):
        run_setup()
    run_app()
