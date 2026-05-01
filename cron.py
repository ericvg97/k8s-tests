import time
from kubernetes import client, config

config.load_incluster_config()  # or load_kube_config() for local
v1 = client.CoreV1Api()
apps = client.AppsV1Api()

NAMESPACE = "default"
DEPLOYMENT = "k8s-tests"
LABEL_SELECTOR = "app=k8s-tests"
TARGET_IDLE = 2
MIN_REPLICAS = 2
MAX_REPLICAS = 20
COOLDOWN_SECONDS = 5

def count_idle_pods():
    pods = v1.list_namespaced_pod(NAMESPACE, label_selector=LABEL_SELECTOR).items
    idle = 0
    for pod in pods:
        if pod.metadata.deletion_timestamp is not None:
            continue
        if pod.status.phase != "Running":
            continue
        ready = next(
            (c for c in (pod.status.conditions or []) if c.type == "Ready"),
            None,
        )
        if ready and ready.status == "True":
            idle += 1
    return idle, len(pods)

def scale_deployment(desired: int):
    clamped = max(MIN_REPLICAS, min(MAX_REPLICAS, desired))
    apps.patch_namespaced_deployment_scale(
        name=DEPLOYMENT,
        namespace=NAMESPACE,
        body={"spec": {"replicas": clamped}},
    )
    return clamped

last_scale_time = 0.0

while True:
    start = time.monotonic()
    idle, total = count_idle_pods()
    elapsed_ms = (time.monotonic() - start) * 1000

    desired = total - idle + TARGET_IDLE
    cooldown_remaining = COOLDOWN_SECONDS - (time.monotonic() - last_scale_time)

    if desired != total and cooldown_remaining <= 0:
        actual = scale_deployment(desired)
        last_scale_time = time.monotonic()
        print(f"{idle} idle / {total} total -> scaled to {actual} ({elapsed_ms:.0f}ms)", flush=True)
    else:
        msg = f"{idle} idle / {total} total ({elapsed_ms:.0f}ms)"
        if desired != total:
            msg += f" (want {desired}, cooldown {cooldown_remaining:.0f}s)"
        print(msg, flush=True)

    time.sleep(1)