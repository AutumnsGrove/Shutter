"""
CLI interface using Typer.
"""

import typer
from typing import Optional

app = typer.Typer()


@app.command()
def main(
    url: str,
    query: Optional[str] = typer.Option(None, "--query", "-q", help="What to extract"),
    model: str = typer.Option("fast", "--model", "-m", help="Model preference"),
    max_tokens: int = typer.Option(500, "--max-tokens", help="Max output tokens"),
):
    """
    Shutter - Web Content Distillation Service

    Open. Capture. Close.
    """
    # TODO: Implement CLI logic
    typer.echo(f"Shutter CLI - url: {url}, query: {query}")


if __name__ == "__main__":
    app()
