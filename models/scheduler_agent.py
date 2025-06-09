import ollama

# This function takes in free slots & tasks, builds the prompt, and calls Ollama
def generate_schedule(free_slots, todoist_tasks):

    # Build task string
    formatted_tasks = ""
    for task in todoist_tasks:
        formatted_tasks += f"- Task: {task['task']}, Priority: {task['priority']}, Due: {task['due']}, Duration: {task['duration']} hours\n"

    # Build free slot string
    formatted_slots = ""
    for slot in free_slots:
        formatted_slots += f"- {slot['date']}: {slot['start']}-{slot['end']}\n"

    # Final prompt
    prompt = f"""
You are a personal scheduler agent.

Here are my tasks:
{formatted_tasks}

Here are my free calendar slots:
{formatted_slots}

Please generate a schedule that:
- Prioritizes deadlines.
- Fills highest priority tasks first.
- Spreads work evenly across free slots.
- Avoids scheduling conflicts.

Output JSON like:
[{{"date": "...", "time": "...", "task": "..."}}]
"""

    response = ollama.chat(
      model="llama3",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )

    return response['message']['content']
