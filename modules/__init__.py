import argparse
import json

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from modules.domain_intel import check_email_breach, resolve_dns, whois_lookup
from modules.metadata_extractor import extract_file_metadata
from modules.username_search import check_username

console = Console()


def display_disclaimer():
    panel = Panel(
        "[bold red]DISCLAIMER[/bold red]\n\n"
        "هذا التطبيق مخصص فقط للاستخدام التعليمي أو المصرح به.\n"
        "لا تستخدمه في جمع بيانات خاصة أو غير مصرح بها.\n"
        "تأكد من وجود إذن مناسب قبل أي فحص أو تحليل.\n\n"
        "[bold yellow]Use only for authorized or educational purposes.[/bold yellow]",
        title="[bold cyan]Ethical Use[/bold cyan]",
        border_style="red"
    )
    console.print(panel)


def format_username_results(results):
    table = Table(title="Username Enumeration Results", show_lines=True)
    table.add_column("Platform", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("URL", style="green")
    table.add_column("HTTP", style="yellow")

    for item in results:
        table.add_row(
            item["platform"],
            item["result"],
            item["url"],
            str(item.get("status_code", "n/a"))
        )

    console.print(table)


def format_domain_results(domain: str, dns_info: dict, whois_info: dict):
    table = Table(title=f"Domain Intelligence: {domain}", show_lines=True)
    table.add_column("Record Type", style="cyan")
    table.add_column("Value", style="green")

    for record_type in ["A", "AAAA", "MX", "NS", "TXT"]:
        values = dns_info.get(record_type, [])
        if values:
            joined = ", ".join(values)
            table.add_row(record_type, joined)
        else:
            table.add_row(record_type, "Not found")

    console.print(table)

    if "error" in whois_info:
        console.print(f"[red]WHOIS Error: {whois_info['error']}[/red]")
    else:
        whois_table = Table(title="WHOIS Information", show_lines=True)
        whois_table.add_column("Field", style="cyan")
        whois_table.add_column("Value", style="green")

        for key, value in whois_info.items():
            whois_table.add_row(str(key), str(value))

        console.print(whois_table)


def format_metadata_results(data: dict):
    console.print(Panel(
        f"[bold green]{data.get('file', 'Unknown File')}[/bold green]\n"
        f"[yellow]{data.get('type', 'unknown')}[/yellow]",
        title="Metadata Extraction"
    ))

    if "error" in data:
        console.print(f"[red]{data['error']}[/red]")
        return

    if "metadata" in data:
        pretty = json.dumps(data["metadata"], ensure_ascii=False, indent=2)
        console.print(pretty)
    else:
        console.print("[yellow]No metadata available.[/yellow]")


def run_username_check(username: str, timeout: int = 10):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task(f"Checking username: {username}", total=None)
        results = check_username(username, timeout=timeout)
        progress.update(task, completed=True)

    format_username_results(results)


def run_domain_check(domain: str, timeout: int = 10):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task(f"Gathering domain data for: {domain}", total=None)
        dns_info = resolve_dns(domain)
        whois_info = whois_lookup(domain)
        progress.update(task, completed=True)

    format_domain_results(domain, dns_info, whois_info)


def run_email_breach_check(email: str, timeout: int = 10):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task(f"Checking breaches for: {email}", total=None)
        result = check_email_breach(email, timeout=timeout)
        progress.update(task, completed=True)

    console.print(Panel(str(json.dumps(result, ensure_ascii=False, indent=2)), title="Email Breach Check"))


def run_metadata_check(file_path: str):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task(f"Extracting metadata from: {file_path}", total=None)
        result = extract_file_metadata(file_path)
        progress.update(task, completed=True)

    format_metadata_results(result)


def main():
    parser = argparse.ArgumentParser(description="Ethical OSINT Toolkit")
    parser.add_argument("--username", help="Check a username across public platforms")
    parser.add_argument("--domain", help="Perform domain intelligence")
    parser.add_argument("--email", help="Check public breach data for an email address")
    parser.add_argument("--file", help="Extract metadata from image or PDF file")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds")

    args = parser.parse_args()

    display_disclaimer()

    if args.username:
        run_username_check(args.username, args.timeout)
    elif args.domain:
        run_domain_check(args.domain, args.timeout)
    elif args.email:
        run_email_breach_check(args.email, args.timeout)
    elif args.file:
        run_metadata_check(args.file)
    else:
        console.print("[bold yellow]No input provided.[/bold yellow]")
        console.print("Examples:")
        console.print("  python main.py --username octocat")
        console.print("  python main.py --domain github.com")
        console.print("  python main.py --email someone@example.com")
        console.print("  python main.py --file ./sample.jpg")


if __name__ == "__main__":
    main()
