from fastapi import FastAPI

app = FastAPI(title="Task Manager API")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/tasks")
def get_tasks():
    return {
        "tasks": [
            {"id": 1, "title": "Изучить Docker Compose", "done": True},
            {"id": 2, "title": "Настроить KVM", "done": True},
            {"id": 3, "title": "Автоматизировать запуск через Ansible", "done": True},
        ]
    }
