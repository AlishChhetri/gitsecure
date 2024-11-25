from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
import typer
from .github_utils import SecurityStatus
import os
from dotenv import load_dotenv

load_dotenv()

cli = typer.Typer()
console = Console()


@cli.command()
def gitsecure(
    repourl: str = typer.Option(
        ..., "--repourl", help="The URL of the GitHub repository to analyze."
    ),
    create_issue: bool = typer.Option(
        False, "--create-issue", help="Create a GitHub issue with the analysis report."
    ),
):
    """Analyze a GitHub repository for security compliance."""

    github_token = os.getenv("GITHUB_TOKEN")  # Get GitHub token from .env file
    if not github_token:
        console.print(
            "[bold red]Error:[/] GITHUB_TOKEN not found in the environment. Ensure it is set in a .env file."
        )
        return

    github_security = SecurityStatus(github_token)

    try:
        owner, repo = github_security.parse_github_url(repourl)
        report = {
            "repository": {
                "owner": owner,
                "name": repo,
                "url": repourl,
            },
            "security_features": {
                "security_policy": github_security.check_security_policy(owner, repo),
                "dependabot_alerts": github_security.check_dependabot_alerts(
                    owner, repo
                ),
                "code_scanning": github_security.check_code_scanning(owner, repo),
            },
        }
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        return

    # Panels and Table Output
    repo_text = (
        f"Repository: {report['repository']['owner']}/{report['repository']['name']}"
    )
    repo_panel = Panel(
        Align.center(repo_text), style="blue", width=60, title_align="center"
    )

    table = Table(
        width=50,
        show_lines=True,
        title="GitHub Security Compliance",
        title_style="cyan",
    )
    table.add_column("Feature", style="white", justify="center")
    table.add_column("Status", justify="center", style="white")

    features = report["security_features"]

    def format_status(status: bool) -> str:
        return "[green]✓[/green]" if status else "[red]✗[/red]"

    table.add_row(
        "Security Policy", format_status(features["security_policy"]["exists"])
    )
    table.add_row(
        "Dependabot Alerts", format_status(features["dependabot_alerts"]["enabled"])
    )
    table.add_row("Code Scanning", format_status(features["code_scanning"]["enabled"]))

    table_panel = Panel(
        Align.center(table), style="cyan", width=60, title_align="center"
    )

    recommendations = []
    if not features["security_policy"]["exists"]:
        recommendations.append("- Add a SECURITY.md file.")
    if not features["dependabot_alerts"]["enabled"]:
        recommendations.append("- Enable Dependabot alerts.")
    if not features["code_scanning"]["enabled"]:
        recommendations.append("- Enable code scanning.")

    recommendations_text = "\n".join(recommendations)
    recommendations_panel = Panel(
        Align.center(recommendations_text),
        title="Recommendations",
        style="yellow",
        width=60,
        title_align="center",
    )

    console.print(repo_panel)
    console.print(table_panel)
    console.print(recommendations_panel)

    # Create GitHub Issue if flag is enabled
    if create_issue:
        issue_title = "GitSecure Analysis Report"
        issue_body = (
            f"### Security Analysis for {repo}\n\n"
            "---\n\n"
            "#### Security Compliance Table\n\n"
            "| Feature           | Status |\n"
            "| ----------------- | ------ |\n"
            f"| Security Policy   | {'✓' if features['security_policy']['exists'] else '✗'} |\n"
            f"| Dependabot Alerts | {'✓' if features['dependabot_alerts']['enabled'] else '✗'} |\n"
            f"| Code Scanning     | {'✓' if features['code_scanning']['enabled'] else '✗'} |\n\n"
            "---\n\n"
            "#### Recommendations and Benefits\n\n"
            "1. **Add a Security Policy (`SECURITY.md`)**:\n"
            "   - **Why Enable**:\n"
            "     - A `SECURITY.md` file provides contributors and users with clear instructions on how to report vulnerabilities responsibly.\n"
            "     - Helps secure your repository by promoting responsible disclosure practices.\n"
            "   - **How to Enable**:\n"
            "     - Go to your repository on GitHub.\n"
            "     - Navigate to the **\"Security\"** section from the navigation bar.\n"
            "     - Under **\"Policy\"**, click **\"Set up a Security Policy\"** to create a `SECURITY.md` file.\n"
            "     - Add contact details or procedures for reporting vulnerabilities.\n"
            "   - **Learn More**: [GitHub Security Policies Documentation](https://docs.github.com/en/code-security/getting-started/github-security-features#adding-a-security-policy-to-your-repository)\n\n"
            "2. **Enable Dependabot Alerts**:\n"
            "   - **Why Enable**:\n"
            "     - Dependabot helps you identify and fix vulnerabilities in your dependencies automatically.\n"
            "     - Keeps your project secure by notifying you of outdated or vulnerable packages.\n"
            "   - **How to Enable**:\n"
            "     - Go to your repository on GitHub.\n"
            "     - Navigate to the **\"Security\"** section from the navigation bar.\n"
            "     - Look for the **\"Dependency Graph\"** section and enable **Dependabot Alerts**.\n"
            "   - **Learn More**: [GitHub Dependabot Alerts Documentation](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts)\n\n"
            "3. **Enable Code Scanning**:\n"
            "   - **Why Enable**:\n"
            "     - Code scanning automatically analyzes your code for potential security vulnerabilities.\n"
            "     - Integrates with tools like **CodeQL** to identify vulnerabilities in your codebase.\n"
            "   - **How to Enable**:\n"
            "     - Go to your repository on GitHub.\n"
            "     - Navigate to the **\"Security\"** section from the navigation bar.\n"
            "     - Under **\"Code Scanning Alerts\"**, click **\"Set up code scanning\"**.\n"
            "     - Choose **CodeQL Analysis** or configure a custom scanning tool.\n"
            "     - Optionally, set up a workflow for continuous scanning by configuring a `.yaml` file in your repository.\n"
            "   - **Learn More**: [GitHub Code Scanning Documentation](https://docs.github.com/en/code-security/code-scanning)\n\n"
            "---\n\n"
            "#### Why It Matters\n"
            "Enabling these security features helps protect your codebase from vulnerabilities, encourages best practices, and builds trust with your collaborators and users. GitHub provides tools to automate and simplify the security process, making it easy to safeguard your projects.\n\n"
            "---\n\n"
            "#### Generated by GitSecure\n"
            "For more information about this tool, visit the [GitSecure GitHub Repository](https://github.com/AlishChhetri/gitsecure).\n"
        )
        issue_response = github_security.create_issue(
            owner, repo, issue_title, issue_body
        )
        if issue_response["success"]:
            console.print(
                f"[bold green]GitHub Issue created successfully:[/] {issue_response['url']}"
            )
        else:
            console.print(
                f"[bold red]Failed to create GitHub Issue:[/] {issue_response['error']}"
            )
