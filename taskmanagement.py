import sqlite3
import datetime

def connect_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        deadline TEXT,
                        status TEXT CHECK(status IN ('pending', 'completed')) NOT NULL DEFAULT 'pending')''')
    conn.commit()
    return conn

def add_task(description, deadline):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, deadline) VALUES (?, ?)", (description, deadline))
    conn.commit()
    conn.close()
    print("Task added successfully!")

def view_tasks(status=None):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM tasks"
    if status:
        query += " WHERE status = ?"
        cursor.execute(query, (status,))
    else:
        cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        print(task)

def update_task(task_id, new_status=None, new_description=None):
    conn = connect_db()
    cursor = conn.cursor()
    if new_status:
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    if new_description:
        cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
    conn.commit()
    conn.close()
    print("Task updated successfully!")

def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Task deleted successfully!")

def main_menu():
    while True:
        print("\nTask Management System")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Update a task")
        print("6. Delete a task")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            desc = input("Enter task description: ")
            deadline = input("Enter deadline (YYYY-MM-DD) or leave blank: ")
            add_task(desc, deadline)
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            view_tasks("pending")
        elif choice == "4":
            view_tasks("completed")
        elif choice == "5":
            task_id = int(input("Enter task ID: "))
            status = input("Enter new status (pending/completed) or leave blank: ")
            desc = input("Enter new description or leave blank: ")
            update_task(task_id, status if status else None, desc if desc else None)
        elif choice == "6":
            task_id = int(input("Enter task ID: "))
            delete_task(task_id)
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()