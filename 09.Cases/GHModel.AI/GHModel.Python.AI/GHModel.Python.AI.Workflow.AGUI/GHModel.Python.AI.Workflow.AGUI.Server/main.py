
import os

from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from workflow import workflow  # 🏗️ The AGUI workflow
from fastapi import FastAPI


app = FastAPI(title="Travel Agent AG-UI Server")

agent = workflow.as_agent(name="Travel Agent")

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8888)