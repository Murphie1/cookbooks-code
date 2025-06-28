import os
import subprocess
import redis
import json
from openhands.agent import run_agent

# Environment config
TASK = os.getenv("TASK")
REPO_URL = os.getenv("REPO_URL")
MODEL = os.getenv("MODEL", "devstral")
TASK_ID = os.getenv("TASK_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
WORKSPACE = "/workspace"
REDIS_HOST = os.getenv("REDIS_HOST", "host.docker.internal")

# Redis setup
r = redis.Redis(host=REDIS_HOST, port=6379, db=0)

def update_status(status, data=None):
    payload = {"status": status}
    if data:
        payload.update(data)
    r.hset(f"task:{TASK_ID}", mapping=payload)

def clone_or_init_repo():
    os.chdir(WORKSPACE)
    if REPO_URL:
        subprocess.run(["git", "clone", REPO_URL, "."], check=True)
    else:
        subprocess.run(["git", "init"], check=True)

def commit_and_push():
    subprocess.run(["git", "config", "--global", "user.email", "bot@agent.com"])
    subprocess.run(["git", "config", "--global", "user.name", "AgentBot"])
    subprocess.run(["git", "checkout", "-b", "agent-patch"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Automated patch from OpenHands"], check=True)
    subprocess.run(["git", "push", "origin", "agent-patch"], check=True)

def create_github_pr():
    repo = subprocess.run(["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True).stdout.strip()
    repo_path = repo.split("github.com/")[-1].replace(".git", "")
    api_url = f"https://api.github.com/repos/{repo_path}/pulls"
    data = {
        "title": "OpenHands AI Patch",
        "head": "agent-patch",
        "base": "main",
        "body": f"Automated changes from OpenHands agent.\n\nTask: {TASK}"
    }
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    subprocess.run(["curl", "-X", "POST", api_url,
                    "-H", f"Authorization: Bearer {GITHUB_TOKEN}",
                    "-H", "Accept: application/vnd.github+json",
                    "-d", json.dumps(data)])

def main():
    try:
        update_status("in-progress")
        clone_or_init_repo()

        # Set OpenHands LLM settings via env or kwargs
        os.environ["LLM_PROVIDER"] = "ollama"
        os.environ["LLM_BASE_URL"] = os.getenv("LLM_BASE_URL", "http://host.docker.internal:11434")
        os.environ["LLM_MODEL"] = MODEL

        # Run the OpenHands agent loop
        run_agent(prompt=TASK, repo_path=WORKSPACE)

        if GITHUB_TOKEN and REPO_URL:
            commit_and_push()
            create_github_pr()
            update_status("complete", {"result": "PR created"})
        else:
            update_status("complete", {"result": "Patch ready"})

    except Exception as e:
        update_status("error", {"error": str(e)})

if __name__ == "__main__":
    main()
