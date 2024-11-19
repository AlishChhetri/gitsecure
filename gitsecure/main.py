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
