from kubernetes import client, config

config.load_incluster_config()  # or load_kube_config() for local
v1 = client.CoreV1Api()

NAMESPACE = "default"
LABEL_SELECTOR = "app=k8s-tests"

def count_idle_pods():
    pods = v1.list_namespaced_pod(NAMESPACE, label_selector=LABEL_SELECTOR).items
    idle = 0
    for pod in pods:
        if pod.metadata.deletion_timestamp is not None:
            continue  # pod is terminating, ignore
        if pod.status.phase != "Running":
            continue
        # Ready condition = passing readiness probe = idle (per your setup)
        ready = next(
            (c for c in (pod.status.conditions or []) if c.type == "Ready"),
            None,
        )
        if ready and ready.status == "True":
            idle += 1
    return idle, len(pods)

import time

while True:
    start = time.monotonic()
    idle, total = count_idle_pods()
    elapsed_ms = (time.monotonic() - start) * 1000
    print(f"{idle} idle / {total} total ({elapsed_ms:.0f}ms)", flush=True)
    time.sleep(10)