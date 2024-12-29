def write_to_redis(redis_client, request, response):
    redis_client.write(request=request, response=response)