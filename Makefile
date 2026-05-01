build:
	docker build -t k8s-tests .

run:
	docker run -p 8000:8000 k8s-tests
