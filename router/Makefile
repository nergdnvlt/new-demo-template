include .env

deploy:
	@echo "Running Google Cloud Build"
	@gcloud builds submit --substitutions=_APOLLO_KEY=${APOLLO_KEY},_APOLLO_GRAPH_REF=${APOLLO_GRAPH_REF}

build-docker:
	docker build . -f Dockerfile -t router

run-docker:
	docker run --env-file=.env -p 4000:4000 router 

# Mainly a convenience for testing and developing Rhai/Rust plugins
build-and-run-docker:
	make build-docker
	make run-docker

build-docker-unmanaged:
	docker build . -f Dockerfile.unmanaged -t router-unmanaged

run-docker-unmanaged:
	docker run -p 4000:4000 router-unmanaged
