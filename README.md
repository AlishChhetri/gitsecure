# GITSECURE

This tool is designed to analyze GitHub repositories and check if critical security configurations, such as Security Policies, Dependabot Alerts, and Code Scanning, are enabled. Additionally, it allows you to create a GitHub issue with the analysis report to help collaborators track and address missing security configurations.


## Features
- **Security Policy**: Checks if the repository has a `SECURITY.md` file to provide guidelines for reporting vulnerabilities.
- **Dependabot Alerts**: Verifies if Dependabot alerts are enabled for the repository.
- **Code Scanning**: Checks if GitHub Advanced Security's code scanning is enabled.
- **GitHub Issue Creation**: Optionally creates a GitHub issue with the analysis report and actionable recommendations.


## Prerequisites
1. Python 3.12 or higher installed on your machine.
2. A GitHub Personal Access Token (PAT) with the necessary permissions:
   - `repo` (for private repositories).
   - `read:security_events` (for accessing security alerts).
   - `write:issues` (to create issues in repositories).


## Setup
1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/gitsecure.git
   cd gitsecure
   ```

2. **Install Dependencies**:

   Use [Poetry](https://python-poetry.org/) to manage dependencies:
   ```bash
   poetry install
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project directory with the following content:

   ```env
   GITHUB_TOKEN='your_personal_access_token'
   ```


## Usage
### Run the Tool
To analyze a repository, use the `gitsecure` command:

```bash
poetry run gitsecure --repourl https://github.com/owner/repo
```

### Optional: Create a GitHub Issue
To automatically create a GitHub issue with the analysis report, use the `--create-issue` flag:

```bash
poetry run gitsecure --repourl https://github.com/owner/repo --create-issue
```


### Command-Line Options
- `--repourl` or `-r`: The URL of the GitHub repository to analyze.
- `--create-issue`: Creates a GitHub issue in the analyzed repository with the security analysis and recommendations.


### Example
When you run the `gitsecure` tool with the `--create-issue` flag, you will see output similar to the following:

```bash
poetry run gitsecure --repourl https://github.com/AlishChhetri/gitsecure --create-issue
```

**Output**:

```
╭──────────────────────────────────────────────────────────╮
│            Repository: AlishChhetri/gitsecure            │
╰──────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────╮
│                GitHub Security Compliance                │
│    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓    │
│    ┃             Feature              ┃   Status    ┃    │
│    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩    │
│    │         Security Policy          │      ✗      │    │
│    ├──────────────────────────────────┼─────────────┤    │
│    │        Dependabot Alerts         │      ✗      │    │
│    ├──────────────────────────────────┼─────────────┤    │
│    │          Code Scanning           │      ✗      │    │
│    └──────────────────────────────────┴─────────────┘    │
╰──────────────────────────────────────────────────────────╯
╭──────────────────── Recommendations ─────────────────────╮
│               - Add a SECURITY.md file.                  │
│               - Enable Dependabot alerts.                │
│               - Enable code scanning.                    │
╰──────────────────────────────────────────────────────────╯
[bold green]GitHub Issue created successfully:[/] https://github.com/AlishChhetri/gitsecure/issues/1
```


### Output Explanation
The tool provides three main sections in its output:

1. **Repository Panel**:
   Displays the repository owner and name for context.

2. **Security Compliance Table**:
   | Feature           | Status |
   | ----------------- | ------ |
   | Security Policy   | ✓ or ✗ |
   | Dependabot Alerts | ✓ or ✗ |
   | Code Scanning     | ✓ or ✗ |

   - **✓**: The feature is enabled or exists.
   - **✗**: The feature is missing or not enabled.

3. **Recommendations Panel**:
   Lists actions you should take if certain features are not enabled:
   - `- Add a SECURITY.md file.`: Guidance to add a `SECURITY.md` file.
   - `- Enable Dependabot alerts.`: Instructions to enable Dependabot alerts.
   - `- Enable code scanning.`: Steps to enable GitHub's code scanning feature.

4. **GitHub Issue Creation**:
   If the `--create-issue` flag is used, the tool creates a GitHub issue in the repository with:
   - Detailed analysis.
   - Benefits of enabling the missing features.
   - Steps to enable these features, with links to GitHub documentation.


## Following Recommendations

1. **Add a SECURITY.md File**:
   - **Why Enable**: A `SECURITY.md` file provides contributors with clear instructions on how to report vulnerabilities responsibly.
   - **How to Enable**:
     - Go to your repository on GitHub.
     - Navigate to the **"Security"** section from the navigation bar.
     - Under **"Policy"**, click **"Set up a Security Policy"** to create a `SECURITY.md` file.
   - **Documentation**: [GitHub Security Policies](https://docs.github.com/en/code-security/getting-started/github-security-features#adding-a-security-policy-to-your-repository)

2. **Enable Dependabot Alerts**:
   - **Why Enable**: Dependabot helps you automatically identify and fix vulnerabilities in your dependencies.
   - **How to Enable**:
     - Go to your repository on GitHub.
     - Navigate to the **"Security"** section from the navigation bar.
     - Enable **Dependabot Alerts** under the "Dependency Graph" section.
   - **Documentation**: [GitHub Dependabot Alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts)

3. **Enable Code Scanning**:
   - **Why Enable**: Code scanning automatically analyzes your code for security vulnerabilities.
   - **How to Enable**:
     - Go to your repository on GitHub.
     - Navigate to the **"Security"** section from the navigation bar.
     - Under **"Code Scanning Alerts"**, click **"Set up code scanning"**.
     - Choose **CodeQL Analysis** or integrate a custom scanning tool.
   - **Documentation**: [GitHub Code Scanning](https://docs.github.com/en/code-security/code-scanning)


## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
