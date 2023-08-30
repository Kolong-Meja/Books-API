# app/database/sql_tool.py

import os
import pathlib
import psycopg2
import rich
import sqlite3

from dotenv import load_dotenv


# load all variable from .env file.
load_dotenv()

# for postgresql only!.
postgre_database_url = os.environ.get("POSTGRES_DATABASE_URL")
postgre_database_connection = psycopg2.connect(postgre_database_url)

# for sqlite3 only!
database_path = os.path.join(pathlib.Path.cwd(), "books.db")
sqlite_database_connection = sqlite3.connect(database_path)


# used for catch exception.
def exception_factory(exception, message: str):
    return exception(message)

# used for execute SQL.
def query(query: str) -> None:
    try:
        cursor = sqlite_database_connection.cursor()
        cursor.execute(query)

        if query.lower().startswith('select'):
            if query.find('*'):
                records = cursor.fetchall()

                if records:
                    rich.print("[bold green]Data:[/bold green]")

                    for record in records:
                        rich.print(f"[bold yellow]{record}[/bold yellow]")
                    
                    rich.print("[bold green]Recorded[/bold green] :white_check_mark:")
                else:
                    rich.print("[bold red]Oops![/bold red] Books table is empty.")

                cursor.close()
                sqlite_database_connection.close()
            else:
                record = cursor.fetchmany()
                
                if record:
                    rich.print("[bold green]Data:/[/bold green]")
                    rich.print(f"[bold yellow]{record}[/bold yellow]")
                    rich.print("[bold green]Recorded[/bold green] :white_check_mark:")
                else:
                    rich.print("[bold red]Oops![/bold red] Books table is empty.")
                
                cursor.close()
                sqlite_database_connection.close()
        else:
            cursor.close()
            sqlite_database_connection.commit()
            rich.print(f"[bold yellow]{query}[/bold yellow] [bold green]executed[/bold green] :white_check_mark:")
    except psycopg2.Error as e:
        rich.print(f":red_circle: [bold red]Error[/bold red]: {e}")


