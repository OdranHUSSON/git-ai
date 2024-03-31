# Git AI Tools

The Git AI Tools suite is designed to streamline the development workflow by leveraging AI to automate the creation of commit messages, branch names, pull request descriptions, and comprehensive changelogs. This toolset includes features for generating detailed, markdown-formatted pull request descriptions based on `git diff` output and a changelog generator that compiles release notes from Jira card details associated with commits and PRs on the develop branch.

## Features

- **Commit Message Generation**: Automates the creation of commit messages based on your changes.
- **Branch Name Generation**: Generates branch names from a brief description of your work.
- **Pull Request Description Generation**: Creates detailed, markdown-formatted PR descriptions from `git diff` outputs.
- **Changelog Generation**: Compiles a versioned changelog from Jira card details linked to commits and PRs on the develop branch, ideal for preparing version releases.

## Installation

### Clone the Repository

To get started, clone the Git AI Tools repository to your desired directory:

```bash
git clone git@github.com:OdranHUSSON/git-ai.git ~/scripts/git-ai
```

### Make Scripts Executable

Change into the cloned directory and set the script files to be executable:

```bash
cd ~/scripts/git-ai
chmod +x *.py
```

### Set Up Aliases

For convenience, add aliases to your shell's profile file (e.g., `.bashrc`, `.zshrc`):

#### For Bash Users

```bash
echo "alias gc='python3 ~/scripts/git-ai/commit_name_per_git_diff.py'" >> ~/.bashrc
echo "alias gb='python3 ~/scripts/git-ai/branch_name.py'" >> ~/.bashrc
echo "alias gpr='python3 ~/scripts/git-ai/generate_markdown_description.py'" >> ~/.bashrc
echo "alias gcl='python3 ~/scripts/git-ai/generate_changelog.py'" >> ~/.bashrc
```

#### For Zsh Users

```zsh
echo "alias gc='python3 ~/scripts/git-ai/commit_name_per_git_diff.py'" >> ~/.zshrc
echo "alias gb='python3 ~/scripts/git-ai/branch_name.py'" >> ~/.zshrc
echo "alias gpr='python3 ~/scripts/git-ai/generate_markdown_description.py'" >> ~/.zshrc
echo "alias gcl='python3 ~/scripts/git-ai/generate_changelog.py'" >> ~/.zshrc
```

### Configure API Key

To use the AI features, add your OpenAI API key to the `.env` file in the Git AI Tools directory:

```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" >> ~/scripts/git-ai/.env
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

### Apply Configuration

Source your profile file to apply the new aliases:

```bash
source ~/.bashrc  # Or the appropriate file for your shell
```

## Usage

### Generating Pull Request Descriptions

Execute the `gpr` alias, follow the prompts, and obtain a markdown-formatted description of your PR changes:

```bash
gpr
```

### Generating Changelogs

Before merging develop into your release branch, run the changelog generator to compile a detailed changelog for the version release:

```bash
gcl
```

## Notes

- Ensure Python 3, Git, and other dependencies mentioned in the script files are installed on your system.
- For the changelog generator, make sure Jira and GitHub configurations (API keys, repository names, etc.) are correctly set up as per the script requirements.

This toolkit aims to save time and enhance the clarity of communications within development teams, especially for those practicing continuous integration and delivery.