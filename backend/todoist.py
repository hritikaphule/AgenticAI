from todoist_api_python.api import TodoistAPI

api = TodoistAPI("4f5aa927f4ab0033682658141e0fcb4c22799a4e")

def get_tasks():
    tasks = api.get_tasks()
    print("RAW TASK RESPONSE:", tasks)

    for task in tasks:
        print("TYPE OF TASK:", type(task))
        print("TASK OBJECT:", task)
    return tasks