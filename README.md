# Git AI Commit Helper

This tool assists in generating commit messages based on `git diff` output, using an AI model.

## Installation

### 1. Clone the Repository

Clone the `git-ai` repository into your desired directory. For example, to clone it into `~/scripts/git-ai`:

```bash
git clone git@github.com:OdranHUSSON/git-ai.git ~/scripts/git-ai
```

### 2. Make the Script Executable

Navigate to the `git-ai` directory and make the main script executable:

```bash
cd ~/scripts/git-ai
chmod +x commit_name_per_git_diff.py
```

### 3. Set Up an Alias

Add an alias to your shell profile file (`.bashrc`, `.bash_profile`, `.zshrc`, etc.):

For Bash:
```bash
echo "alias gc='python3 ~/scripts/git-ai/commit_name_per_git_diff.py'" >> ~/.bashrc
echo "alias gb='python3 ~/scripts/git-ai/branch_name.py'" >> ~/.bashrc
echo "alias gpr='python3 ~/scripts/git-ai/generate_markdown_description.py'" >> ~/.bashrc
```

For Zsh:
```zsh
echo "alias gc='python3 ~/scripts/git-ai/commit_name_per_git_diff.py'" >> ~/.zshrc
echo "alias gb='python3 ~/scripts/git-ai/branch_name.py'" >> ~/.zshrc
echo "alias gpr='python3 ~/scripts/git-ai/generate_markdown_description.py'" >> ~/.zshrc
```

### 4. Configure API Key

Add your OpenAI API key to the `.env` file in the `git-ai` directory:

```bash
echo "OPENAI_API_KEY='yourapikey'" >> ~/scripts/git-ai/.env
```

Replace `'yourapikey'` with your actual OpenAI API key.

### 5. Apply the Changes

Activate the alias without restarting the terminal by sourcing your profile file:

```bash
source ~/.bashrc  # or the appropriate file for your shell
```

## Usage

Run the script using the alias:

```
git-ai
```

The script will interactively generate a commit message based on the output of `git diff`. You'll be asked to confirm the message, and upon confirmation, the script will execute `git add .` and `git commit -m "your_commit_message"`.

## Notes

- Ensure that Python 3 and Git are installed on your system.
- If the script has additional Python dependencies, make sure to install them, preferably in a virtual environment.