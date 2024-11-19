# GITSECURE

This tool is designed to analyze GitHub repositories and check if critical security configurations, such as Security Policies, Dependabot Alerts, and Code Scanning, are enabled.

## Features
- **Security Policy**: Checks if the repository has a `SECURITY.md` file to provide guidelines for reporting vulnerabilities.
- **Dependabot Alerts**: Verifies if Dependabot alerts are enabled for the repository.
- **Code Scanning**: Checks if GitHub Advanced Security's code scanning is enabled.

## Prerequisites
1. Python 3.12 or higher installed on your machine.
2. A GitHub Personal Access Token (PAT) with the necessary permissions:
   - `repo` (for private repositories).
   - `read:security_events` (for accessing security alerts).

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

### Command-Line Options
- `--repourl` or `-r`: The URL of the GitHub repository to analyze.

### Example
When you run the `gitsecure` tool, you will see output similar to the following:

```bash
poetry run gitsecure --repourl https://github.com/AlishChhetri/gitsecure
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

## Following Recommendations

1. **Add a SECURITY.md File**:
   - Go to your repository on GitHub.
   - Navigate to the **"Security"** section from the navigation bar.
   - Under **"Policy"**, click **"Set up a Security Policy"** to create a `SECURITY.md` file.
   - Use the following content as a starting point:
     ```markdown
     # Security Policy
     If you discover a security vulnerability, please contact [email] with details.
     ```

2. **Enable Dependabot Alerts**:
   - Go to your repository on GitHub.
   - Navigate to the **"Security"** section from the navigation bar.
   - Look for the **"Dependency Graph"** and enable **Dependabot Alerts**.

3. **Enable Code Scanning**:
   - Go to your repository on GitHub.
   - Navigate to the **"Security"** section from the navigation bar.
   - Under **"Code Scanning Alerts"**, click **"Set up code scanning"**.
   - Select **CodeQL Analysis** or integrate a custom code scanning tool.
   - You can optionally configure a workflow for continuous scanning by setting up a YAML file.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
