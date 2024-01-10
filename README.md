# Git AI aliases

This tool assists in generating commit messages, branch names, and pull request descriptions based on `git diff` output, using an AI model.

## Installation

### 1. Clone the Repository

Clone the `git-ai` repository into your desired directory. For example, to clone it into `~/scripts/git-ai`:

```bash
git clone git@github.com:OdranHUSSON/git-ai.git ~/scripts/git-ai
```

### 2. Make the Scripts Executable

Navigate to the `git-ai` directory and make the scripts executable:

```bash
cd ~/scripts/git-ai
chmod +x commit_name_per_git_diff.py branch_name.py generate_markdown_description.py
```

### 3. Set Up Aliases

Add aliases to your shell profile file (`.bashrc`, `.bash_profile`, `.zshrc`, etc.):

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

Activate the aliases without restarting the terminal by sourcing your profile file:

```bash
source ~/.bashrc  # or the appropriate file for your shell
```

## Usage

### Commit Message Generation

```bash
gc
```

Generates a commit message based on the output of `git diff`. Confirm the message, and upon confirmation, the script will execute `git add .` and `git commit -m "your_commit_message"`.

### Branch Name Generation

```bash
gb
```

Generates a branch name based on your description. Confirm the name, and upon confirmation, the script will execute `git checkout -b "branch_name"`.

### Pull Request Description Generation

```bash
gpr
```

Generates a markdown description for a pull request. Confirm the description, and you can then use it to create a PR manually or copy it to the clipboard.

## Notes

- Ensure that Python 3 and Git are installed on your system.
- If the scripts have additional Python dependencies, make sure to install them, preferably in a virtual environment.