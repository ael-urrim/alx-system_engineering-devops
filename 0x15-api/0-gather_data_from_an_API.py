#!/usr/bin/python3
"""Returns to-do list information for a given employee ID."""
import requests

def get_employee_todo_progress(employee_id):
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch employee information
    employee_url = f"{base_url}/users/{employee_id}"
    employee_response = requests.get(employee_url)
    employee_data = employee_response.json()
    employee_name = employee_data["name"]

    # Fetch employee's TODO list
    todos_url = f"{base_url}/todos?userId={employee_id}"
    todos_response = requests.get(todos_url)
    todos_data = todos_response.json()

    # Count completed tasks
    completed_tasks = [task for task in todos_data if task["completed"]]
    num_completed_tasks = len(completed_tasks)
    total_tasks = len(todos_data)

    # Print TODO list progress
    print(f"Employee {employee_name} is done with tasks ({num_completed_tasks}/{total_tasks}):")
    for task in completed_tasks:
        print(f"\t{task['title']}")
