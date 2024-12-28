api:
	export PYTHONPATH=. && python3 src/service/app.py

request:
	export PYTHONPATH=. && python3 scripts/send_example_request.py

redis:
	export PYHTONPATH=. && bash scripts/run_redis.sh

postgres:
	export PYHTONPATH=. && bash scripts/run_postgres.sh

mongodb:
	export PYHTONPATH=. && bash scripts/run_mongodb.sh