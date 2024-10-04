import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    # Add subparsers such that several command-line commands can be added to the same line
    subparsers = parser.add_subparsers(title="Enables subcommands for the task manager", dest='command')

    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument(
        "task_name",
        type=str,
        help='The name of the task to add, for example "Buy Groceries". Returns task ID.',
    )

    update_parser = subparsers.add_parser("update", help="Update an existing task.")
    update_parser.add_argument(
        "task_id", type=int, help="The ID of the task to be updated."
    )
    update_parser.add_argument(
        "updated_task_name",
        type=str,
        help='The name of the updated task, for example "Buy groceries and cook dinner."',
    )

    delete_parser = subparsers.add_parser("delete", help="Delete an existing task.")
    delete_parser.add_argument(
        "task_id", type=int, help="The ID of the task to be deleted."
    )

    progress_parser = subparsers.add_parser("mark-in-progress")
    progress_parser.add_argument(
        "task_id", type=int, help="The ID of the task to be marked in progress."
    )

    done_parser = subparsers.add_parser("mark-done")
    done_parser.add_argument(
        "task_id", type=int, help="The ID of the task to be marked as done."
    )

    list_parser = subparsers.add_parser("list", help="List all tasks.")
    list_parser.add_argument(
        "filter",
        type=str,
        choices=["done", "todo", "in-progress"],
        help="List all tasks based on a specific filter.",
    )

    return parser



if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    # If no subcommand is provided, print help
    if not vars(args)['command']:
        parser.print_help()
