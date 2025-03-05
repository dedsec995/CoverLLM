import os
import subprocess
import sys

# Change working directory to executable's directory if running as compiled
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

SETUP_FLAG = ".setup_done"

def is_command_available(command):
    """Check if a command is available on the system PATH."""
    result = subprocess.run(["where" if os.name == "nt" else "which", command],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller. """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def run_command(command, shell=False):
    try:
        result = subprocess.run(command, shell=shell, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Command not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def run_setup():
    print("Running first-time setup...")

    if not is_command_available("python"):
        print("Python not found. Please install Python from https://www.python.org/downloads/")
        sys.exit(1)

    if not is_command_available("ollama"):
        print("Ollama not found. Install Ollama from https://ollama.com/download/")
        sys.exit(1)
    else:
        print("Ollama is installed. Pulling deepseek-r1 model...")
        run_command(["ollama", "pull", "deepseek-r1"])

    if not os.path.exists("venv"):
        run_command(["python", "-m", "venv", "venv"])

    if os.name == "nt":  # Windows
        activate_cmd = r"venv\Scripts\activate.bat"
        requirements_path = get_resource_path("requirements.txt")
        pip_install_cmd = f"{activate_cmd} && pip install -r {requirements_path}"
        run_command(pip_install_cmd, shell=True)
    
    with open(SETUP_FLAG, "w") as f:
        f.write("Setup complete")

def run_app():
    print("Launching the app...")
    if os.name == "nt":
        activate_cmd = r"venv\Scripts\activate.bat"
        app_path = get_resource_path("app.py")
        streamlit_cmd = f"{activate_cmd} && streamlit run {app_path}"
        run_command(streamlit_cmd, shell=True)

if __name__ == "__main__":
    if not os.path.exists(SETUP_FLAG):
        run_setup()
    run_app()
