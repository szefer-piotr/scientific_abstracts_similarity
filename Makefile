api:
	export PYTHONPATH=. && python3 src/app.py

request:
	export PYTHONPATH=. && python3 scripts/send_example_request.py

redis:
	export PYHTONPATH=. && bash scripts/run_redis.sh