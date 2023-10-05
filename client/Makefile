include .env

check:
	apollo client:check --includes="*.py"

check-contract:
	apollo client:check --includes="*.py" --variant internal-api

deploy:
	gcloud builds submit --substitutions=_ROUTER_CONNECTION_URL="${ROUTER_CONNECTION_URL}"

setup-traffic-gen:
	gcloud pubsub topics create traffic_gen || true
	gcloud scheduler jobs create pubsub traffic-gen  --schedule "*/5 * * * *" --location us-east1 --topic traffic_gen --message-body "Hello"