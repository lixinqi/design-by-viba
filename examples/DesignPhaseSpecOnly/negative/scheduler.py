"""Schedule tasks after the tasks they depend on."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    name: str
    duration: int
    depends_on: list[str]


@dataclass(frozen=True)
class Plan:
    order: list[Task]
    finish_seconds: int


def schedule(path: str, parse) -> Plan:
    """Read the task list, order the tasks, and add up the makespan."""
    tasks = parse(path)
    by_name = {task.name: task for task in tasks}

    order: list[Task] = []
    state: dict[str, str] = {}

    def visit(task: Task) -> None:
        if state.get(task.name) == "done":
            return
        if state.get(task.name) == "visiting":
            raise ValueError(f"dependency cycle at {task.name}")
        state[task.name] = "visiting"
        for name in task.depends_on:
            visit(by_name[name])
        state[task.name] = "done"
        order.append(task)

    for task in tasks:
        visit(task)

    finish: dict[str, int] = {}
    for task in order:
        start = max((finish[name] for name in task.depends_on), default=0)
        finish[task.name] = start + task.duration

    return Plan(order=order, finish_seconds=max(finish.values(), default=0))
