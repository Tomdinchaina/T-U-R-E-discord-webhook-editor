import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from pyfiglet import Figlet

console = Console()

def display_banner():
    fig = Figlet(font='slant')
    console.print(f"[bold white]\n{fig.renderText('T U R E')}[/bold white]")
    console.print("[bold white]by tomdelamare[/bold white]\n")

def get_webhook_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        table = Table(title="Webhook Info")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        table.add_row("Name", data.get("name", "N/A"))
        table.add_row("Avatar URL", data.get("avatar", "N/A"))
        table.add_row("Channel ID", str(data.get("channel_id", "N/A")))
        console.print(table)
    else:
        console.print("[bold red]Failed to fetch webhook info![/bold red]")

def delete_webhook(url):
    response = requests.delete(url)
    if response.status_code == 204:
        console.print("[bold green]Webhook deleted successfully![/bold green]")
    else:
        console.print("[bold red]Failed to delete webhook![/bold red]")

def spam_webhook(url, message, count):
    payload = {"content": message}
    for _ in range(count):
        requests.post(url, json=payload)
    console.print("[bold green]Spam complete![/bold green]")

def edit_webhook(url, name, avatar):
    payload = {"name": name, "avatar": avatar}
    response = requests.patch(url, json=payload)
    if response.status_code == 200:
        console.print("[bold green]Webhook updated successfully![/bold green]")
    else:
        console.print("[bold red]Failed to update webhook![/bold red]")

def main():
    display_banner()
    webhook_url = Prompt.ask("Enter Webhook URL")
    while True:
        option = Prompt.ask("Choose an option", choices=["info", "delete", "message", "edit", "exit"], default="info")
        
        if option == "info":
            get_webhook_info(webhook_url)
        elif option == "delete":
            delete_webhook(webhook_url)
        elif option == "message":
            message = Prompt.ask("Enter message to send")
            count = int(Prompt.ask("How many times?", default="1"))
            spam_webhook(webhook_url, message, count)
        elif option == "edit":
            name = Prompt.ask("Enter new name", default="")
            avatar = Prompt.ask("Enter new avatar URL", default="")
            edit_webhook(webhook_url, name, avatar)
        elif option == "exit":
            break

if __name__ == "__main__":
    main()
