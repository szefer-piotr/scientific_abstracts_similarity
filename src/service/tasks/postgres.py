def write_to_postgres(postgres_client, request, response):
    postgres_client.write(request=request, response=response)