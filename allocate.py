import httpx

KUBE_PROXY = "http://localhost:8001"
NAMESPACE = "default"
FLEET = "k8s-tests"

ALLOCATE_URL = f"{KUBE_PROXY}/apis/allocation.agones.dev/v1/namespaces/{NAMESPACE}/gameserverallocations"

allocation = httpx.post(ALLOCATE_URL, json={
    "apiVersion": "allocation.agones.dev/v1",
    "kind": "GameServerAllocation",
    "spec": {
        "selectors": [{"matchLabels": {"agones.dev/fleet": FLEET}}],
    },
}).json()

status = allocation["status"]
address = status["address"]
port = status["ports"][0]["port"]
print(f"Allocated {status['gameServerName']} at {address}:{port}")

import subprocess
result = subprocess.run(
    ["minikube", "ssh", "--", "curl", "-s", f"http://localhost:{port}/"],
    capture_output=True, text=True, timeout=30,
)
print(f"Response: {result.stdout}")
