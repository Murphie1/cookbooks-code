from tempfile import NamedTemporaryFile
from subprocess import run

def launch_k8s_job(task: str, repo_url: str, model: str, token: str):
    task_id = str(uuid.uuid4())

    with open("k8s/jobs/openhands-job.yaml") as f:
        job_template = f.read()

    job_yaml = job_template.replace("{{TASK_ID}}", task_id)\
                           .replace("{{TASK}}", task)\
                           .replace("{{REPO_URL}}", repo_url or "")\
                           .replace("{{MODEL}}", model or "devstral")\
                           .replace("{{GITHUB_TOKEN}}", token or "")

    with NamedTemporaryFile("w+", suffix=".yaml", delete=False) as tmp:
        tmp.write(job_yaml)
        tmp_path = tmp.name

    run(["kubectl", "apply", "-f", tmp_path])
    return task_id
