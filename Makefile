deploy:
	$(eval IMAGE_TAG := $(shell date +%s))
	docker build -t k8s-tests:$(IMAGE_TAG) .
	minikube image load k8s-tests:$(IMAGE_TAG)
	IMAGE_TAG=$(IMAGE_TAG) envsubst < fleet.yaml | kubectl apply -f -

deploy-autoscaler:
	kubectl apply -f fleetautoscaler.yaml

pods:
	kubectl get pods

url:
	minikube service k8s-tests --url
