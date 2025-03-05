VENV := venv
REQUIREMENTS := requirements.txt
PYTHON := $(shell command -v python3 2>/dev/null)
ifeq ($(PYTHON),)
    $(error "Python3 is not installed. Please install Python3.")
endif
PIP := $(shell command -v pip3 2>/dev/null)
ifeq ($(PIP),)
    $(error "pip3 is not installed. Please install pip3.")
endif
STREAMLIT := $(shell command -v streamlit 2>/dev/null)
OLLAMA := $(shell command -v ollama 2>/dev/null)

.PHONY: all
all: setup run

.PHONY: setup
setup: venv/bin/activate requirements.txt
	@echo "Setting up the project..."
ifeq ($(OLLAMA),)
	@echo "Ollama not found. Installing Ollama..."
	@curl -sSfL https://ollama.com/download/Ollama-linux.zip -o ollama.zip
	@unzip -o ollama.zip -d /usr/local/bin
	@rm ollama.zip
	@echo "Ollama installed."
endif
	@echo "Pulling deepseek-r1 model..."
	@ollama pull deepseek-r1
	@echo "Setup completed."

venv/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV)
	@echo "Installing dependencies..."
	@$(VENV)/bin/pip install -r requirements.txt
	@touch venv/bin/activate

.PHONY: run
run:
	@echo "Giving execute permission to run.sh..."
	@chmod +x run.sh
	@echo "Starting Streamlit app using run.sh..."
	@./run.sh

.PHONY: clean
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV) __pycache__ coverLetter details.json
	@echo "Cleanup done."

.PHONY: install
install:
	@$(VENV)/bin/pip install -r requirements.txt
