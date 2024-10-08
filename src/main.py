import argparse
import json
import time

from enum import StrEnum
from functools import partial
from pathlib import Path

PATH_TO_JSON = Path("./tasks.json")


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


def create_unique_id() -> int:
    # ensures that IDs are sequential
    return int(time.time() * 1000)


class NewTask:
    def __init__(self, task_name: str) -> None:
        self.task_id = create_unique_id()
        self.description = task_name
        self.status = TaskStatus.TODO
        self.created_at = time.time()
        self.updated_at = self.created_at


def load_tasks_from_json() -> dict[str, dict[str, str]]:
    if PATH_TO_JSON.exists():
        with open(PATH_TO_JSON, "r") as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                return {}
    else:
        return {}


def save_tasks_to_json(tasks: dict[str, dict[str, str]]) -> bool:
    with open(PATH_TO_JSON, "w") as json_file:
        json.dump(tasks, json_file, indent=4)
        return True
    return False


def write_task_to_json(new_task: NewTask) -> bool:
    tasks = load_tasks_from_json()
    tasks[new_task.task_id] = vars(new_task)
    return save_tasks_to_json(tasks)


def add_task(args: argparse.Namespace) -> int:
    new_task = NewTask(args.task_name)
    result = write_task_to_json(new_task)
    if result:
        print(new_task.task_id)
        return new_task.task_id
    return -1


def change_dict(action: str, args: argparse.Namespace, **kwargs) -> bool:
    tasks = load_tasks_from_json()
    task_id = str(args.task_id)
    if task_id in tasks:
        match action:
            case "delete_task":
                del tasks[task_id]
            case "update_task":
                tasks[task_id]["description"] = args.updated_task_name
            case "update_task_status":
                tasks[task_id]["status"] = kwargs["status"]
            case _:
                return False
    else:
        return False
    return save_tasks_to_json(tasks)


def delete_task(args: argparse.Namespace) -> bool:
    return change_dict("delete_task", args)


def update_task(args: argparse.Namespace) -> bool:
    return change_dict("update_task", args)


def update_task_status(args: argparse.Namespace, *, status: str) -> bool:
    return change_dict("update_task_status", args, status=status)


def list_tasks(args: argparse.Namespace) -> None:
    tasks = load_tasks_from_json()
    if args.filter is not None:
        tasks = [task for task in tasks.values() if task.get("status") == args.filter]

    tasks = json.dumps(tasks, indent=4)
    print(tasks)


def create_parser():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    # Add subparsers such that several command-line commands can be added to the same line
    subparsers = parser.add_subparsers(
        title="Enables subcommands for the task manager", dest="command", required=True
    )

    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.set_defaults(func=add_task)
    add_parser.add_argument(
        "task_name",
        type=str,
        help='The name of the task to add, for example "Buy Groceries". Returns task ID.',
    )

    update_parser = subparsers.add_parser("update", help="Update an existing task.")
    update_parser.set_defaults(func=update_task)
    update_parser.add_argument(
        "task_id", type=int, help="The ID of the task to be updated."
    )
    update_parser.add_argument(
        "updated_task_name",
        type=str,
        help='The name of the updated task, for example "Buy groceries and cook dinner."',
    )

    delete_parser = subparsers.add_parser("delete", help="Delete an existing task.")
    delete_parser.set_defaults(func=delete_task)
    delete_parser.add_argument(
        "task_id", type=int, help="The ID of the task to be deleted."
    )

    progress_parser = subparsers.add_parser("mark-in-progress")
    progress_parser.set_defaults(func=partial(update_task_status, status=TaskStatus.IN_PROGRESS))
    progress_parser.add_argument(
        "task_id", type=int, help="The ID of the task to be marked in progress."
    )

    done_parser = subparsers.add_parser("mark-done")
    done_parser.set_defaults(func=partial(update_task_status, status=TaskStatus.DONE))
    done_parser.add_argument(
        "task_id", type=int, help="The ID of the task to be marked as done."
    )

    list_parser = subparsers.add_parser("list", help="List all tasks.")
    list_parser.set_defaults(func=list_tasks)
    list_parser.add_argument(
        "filter",
        nargs="?",
        type=str,
        choices=[TaskStatus.DONE, TaskStatus.TODO, TaskStatus.IN_PROGRESS],
        help="List all tasks based on a specific filter.",
    )

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    # args knows the default functions and arguments
    args.func(args)
