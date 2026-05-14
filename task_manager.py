"""Study Task Manager.

A command-line program for students to manage study tasks, deadlines,
priorities, and completion status. Task data is saved in tasks.txt.
"""

from datetime import datetime, date
from pathlib import Path


TASKS_FILE = Path("tasks.txt")
PRIORITIES = ("High", "Medium", "Low")
STATUSES = ("Not completed", "Completed")


def parse_task_line(line):
    """Convert one tasks.txt line into a task dictionary."""
    parts = line.strip().split("|")
    if len(parts) != 6:
        return None

    task_id, title, course, deadline, priority, status = parts
    if not task_id.isdigit():
        return None

    return {
        "id": int(task_id),
        "title": title,
        "course": course,
        "deadline": deadline,
        "priority": priority,
        "status": status,
    }


def task_to_line(task):
    """Convert a task dictionary into one line for tasks.txt."""
    return (
        f"{task['id']}|{task['title']}|{task['course']}|"
        f"{task['deadline']}|{task['priority']}|{task['status']}"
    )


def load_tasks(filename=TASKS_FILE):
    """Load all tasks from a text file."""
    path = Path(filename)
    if not path.exists():
        return []

    tasks = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                task = parse_task_line(line)
                if task is not None:
                    tasks.append(task)
    return tasks


def save_tasks(tasks, filename=TASKS_FILE):
    """Save all tasks to a text file."""
    path = Path(filename)
    with path.open("w", encoding="utf-8") as file:
        for task in tasks:
            file.write(task_to_line(task) + "\n")


def get_next_id(tasks):
    """Return the next available task ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def validate_date(date_text):
    """Return True if date_text is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_task(tasks, title, course, deadline, priority):
    """Add a new task and return the created task."""
    title = title.strip()
    course = course.strip()
    priority = priority.capitalize().strip()

    if not title:
        raise ValueError("Task title cannot be empty.")
    if not course:
        raise ValueError("Course cannot be empty.")
    if not validate_date(deadline):
        raise ValueError("Deadline must use YYYY-MM-DD format.")
    if priority not in PRIORITIES:
        raise ValueError("Priority must be High, Medium, or Low.")

    task = {
        "id": get_next_id(tasks),
        "title": title,
        "course": course,
        "deadline": deadline,
        "priority": priority,
        "status": "Not completed",
    }
    tasks.append(task)
    return task


def find_task(tasks, task_id):
    """Find a task by ID."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def complete_task(tasks, task_id):
    """Mark a task as completed."""
    task = find_task(tasks, task_id)
    if task is None:
        return False
    task["status"] = "Completed"
    return True


def delete_task(tasks, task_id):
    """Delete a task by ID."""
    task = find_task(tasks, task_id)
    if task is None:
        return False
    tasks.remove(task)
    return True


def search_tasks(tasks, keyword):
    """Search tasks by title or course."""
    keyword = keyword.lower().strip()
    return [
        task
        for task in tasks
        if keyword in task["title"].lower() or keyword in task["course"].lower()
    ]


def filter_by_priority(tasks, priority):
    """Return tasks that match a selected priority."""
    priority = priority.capitalize().strip()
    return [task for task in tasks if task["priority"] == priority]


def sort_tasks_by_deadline(tasks):
    """Return tasks sorted by deadline."""
    return sorted(tasks, key=lambda task: task["deadline"])


def get_summary(tasks):
    """Return summary statistics for all tasks."""
    total = len(tasks)
    completed = len([task for task in tasks if task["status"] == "Completed"])
    not_completed = total - completed
    today = date.today().isoformat()
    overdue = len(
        [
            task
            for task in tasks
            if task["deadline"] < today and task["status"] != "Completed"
        ]
    )
    return {
        "total": total,
        "completed": completed,
        "not_completed": not_completed,
        "overdue": overdue,
    }


def display_tasks(tasks):
    """Print tasks in a readable table."""
    if not tasks:
        print("No tasks found.")
        return

    print("-" * 92)
    print(f"{'ID':<4} {'Title':<28} {'Course':<12} {'Deadline':<12} {'Priority':<8} Status")
    print("-" * 92)
    for task in sort_tasks_by_deadline(tasks):
        print(
            f"{task['id']:<4} "
            f"{task['title'][:27]:<28} "
            f"{task['course'][:11]:<12} "
            f"{task['deadline']:<12} "
            f"{task['priority']:<8} "
            f"{task['status']}"
        )
    print("-" * 92)


def ask_task_id():
    """Ask the user for a task ID."""
    try:
        return int(input("Enter task ID: ").strip())
    except ValueError:
        print("Please enter a valid number.")
        return None


def add_task_menu(tasks):
    """Handle user input for adding a task."""
    title = input("Task title: ")
    course = input("Course name: ")
    deadline = input("Deadline (YYYY-MM-DD): ")
    priority = input("Priority (High/Medium/Low): ")

    try:
        task = add_task(tasks, title, course, deadline, priority)
        save_tasks(tasks)
        print(f"Task added with ID {task['id']}.")
    except ValueError as error:
        print(f"Could not add task: {error}")


def complete_task_menu(tasks):
    """Handle user input for completing a task."""
    task_id = ask_task_id()
    if task_id is None:
        return
    if complete_task(tasks, task_id):
        save_tasks(tasks)
        print("Task marked as completed.")
    else:
        print("Task not found.")


def delete_task_menu(tasks):
    """Handle user input for deleting a task."""
    task_id = ask_task_id()
    if task_id is None:
        return
    if delete_task(tasks, task_id):
        save_tasks(tasks)
        print("Task deleted.")
    else:
        print("Task not found.")


def search_task_menu(tasks):
    """Handle user input for searching tasks."""
    keyword = input("Enter search keyword: ")
    results = search_tasks(tasks, keyword)
    display_tasks(results)


def priority_filter_menu(tasks):
    """Handle user input for filtering tasks by priority."""
    priority = input("Priority to filter (High/Medium/Low): ")
    results = filter_by_priority(tasks, priority)
    display_tasks(results)


def summary_menu(tasks):
    """Display task statistics."""
    summary = get_summary(tasks)
    print("\nTask Summary")
    print(f"Total tasks: {summary['total']}")
    print(f"Completed: {summary['completed']}")
    print(f"Not completed: {summary['not_completed']}")
    print(f"Overdue: {summary['overdue']}")


def show_menu():
    """Print the main menu."""
    print("\nStudy Task Manager")
    print("1. Add task")
    print("2. View all tasks")
    print("3. Mark task as completed")
    print("4. Delete task")
    print("5. Search tasks")
    print("6. Filter by priority")
    print("7. Show summary")
    print("8. Exit")


def main():
    """Run the command-line task manager."""
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            add_task_menu(tasks)
        elif choice == "2":
            display_tasks(tasks)
        elif choice == "3":
            complete_task_menu(tasks)
        elif choice == "4":
            delete_task_menu(tasks)
        elif choice == "5":
            search_task_menu(tasks)
        elif choice == "6":
            priority_filter_menu(tasks)
        elif choice == "7":
            summary_menu(tasks)
        elif choice == "8":
            save_tasks(tasks)
            print("Tasks saved. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 8.")


if __name__ == "__main__":
    main()
