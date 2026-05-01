deploy:
	$(eval IMAGE_TAG := $(shell date +%s))
	docker build -t k8s-tests:$(IMAGE_TAG) .
	minikube image load k8s-tests:$(IMAGE_TAG)
	IMAGE_TAG=$(IMAGE_TAG) envsubst < deployment.yaml | kubectl apply -f -

pods:
	kubectl get pods

deploy-service:
	kubectl apply -f service.yaml

# forward:#
# 	kubectl port-forward service/k8s-tests 8000:8000

url:
	minikube service k8s-tests --url

