import os
import sqlite3
from rich.console import Console
from rich.table import Table

def clear_terminal():
    # Clear the terminal screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')
# Connect to the SQLite database (this will create the database file if it doesn't exist)
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Create the 'todos' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed BOOLEAN NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')
conn.commit()

def addTodo():
    task = input("Enter a task: ")
    cursor.execute("INSERT INTO todos (task, completed) VALUES (?, 0)", (task,))
    conn.commit()
    print("Task added successfully")

def viewTodo():
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("==> No tasks available")
    else:
        table = Table(title="Todo List")
        table.add_column("[#c5e0bf]S. No [/].", style="#ccc1ad")
        table.add_column("[#c5e0bf] Task [/]", style="#c3e3bc")
        table.add_column("Status", justify="right", style="green")

        for i, row in enumerate(rows):
            status = "✅" if row[2] else "❌"
            table.add_row(str(i + 1), row[1], status)

        console = Console()
        console.print(table)

def edit_status():
    viewTodo()

    choice = int(input("Enter the number of the task to edit: "))

    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()

    if 1 <= choice <= len(rows):
        task_id = rows[choice - 1][0]
        cursor.execute("UPDATE todos SET completed = NOT completed WHERE id = ?", (task_id,))
        conn.commit()
        print("Task edited")
        viewTodo()
    else:
        print("Invalid task number. Please try again.")

def deleteTodo():
    viewTodo()

    choice = int(input("Enter a number to delete a task (enter 0 to clear the list): "))

    if choice == 0:
        confirm = input("Are you sure you want to clear the entire list? (y/n): ")
        if confirm.lower() == 'y':
            cursor.execute("DELETE FROM todos")
            conn.commit()
            print("Entire list cleared")
        else:
            print("Operation canceled")
    else:
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()

        if 1 <= choice <= len(rows):
            task_id = rows[choice - 1][0]
            cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
            conn.commit()
            print("Task deleted")
        else:
            print("Invalid task number. Please try again.")


def main():
    while True:
        clear_terminal()
        viewTodo()
        console = Console()
        console.print("****** Welcome to PyTodo ******", style="bold #9ed9ae")
        console.print("[#c5e0bf]1:[/] Add Task", style="#a9cfb3")
        console.print("[#c5e0bf]2:[/] View Tasks", style="#a9cfb3")
        console.print("[#c5e0bf]3:[/] Delete Task", style="#a9cfb3")
        console.print("[#c5e0bf]4:[/] Edit status", style="#a9cfb3")
        console.print("[#c5e0bf]5:[/] Quit", style="#a9cfb3")

        choice = input("Enter your choice: ")

        if choice == "1":
            addTodo()
        elif choice == "2":
            viewTodo()
        elif choice == "3":
            deleteTodo()
        elif choice == "4":
            edit_status()
        elif choice == "5":
            cursor.close()
            conn.close()
            exit()

if __name__ == "__main__":
    main()
