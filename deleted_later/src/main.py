import typer
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from doc_sync.core import DocumentSync
from doc_sync.cli import run_cli
from doc_sync.web import run_web

app = typer.Typer()
console = Console()

@app.command()
def cli():
    """Run the CLI version of the document sync tool"""
    run_cli()

@app.command()
def web():
    """Run the Streamlit web interface"""
    run_web()

if __name__ == "__main__":
    load_dotenv()
    app() 