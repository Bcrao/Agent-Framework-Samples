import asyncio
from dotenv import load_dotenv
from workflow import workflow  # 🏗️ The content workflow



from agent_framework.observability import setup_observability
from agent_framework import setup_logging, WorkflowEvent




# Load environment variables first, before importing agents
load_dotenv()
setup_observability()
setup_logging()

class DatabaseEvent(WorkflowEvent): ...


async def main():
    print("Enter a prompt and the workflow will respond; type 'exit' to quit.")
    while True:
        prompt = input("\nYou: ").strip()
        if not prompt:
            continue
        if prompt.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        result = ''
        async for event in workflow.run_stream(prompt):
            if isinstance(event, DatabaseEvent):
                print(f"{event}")
            if isinstance(event, WorkflowEvent):
                result += str(event.data)

        result = result.replace("None", "")

        print(f"\nAssistant:\n{result}\n")

    


if __name__ == "__main__":
    asyncio.run(main())