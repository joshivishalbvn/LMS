import time
from django.db import connection

class DebuggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print("================= >> Duration Details << =====================")
        print(f"{'*' * 10} {request.path} took {duration:.2f} seconds {'*' * 10}")
        print("==============================================================")
        print()
        return response


class DatabaseQueryLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clear previous query logs
        connection.queries_log.clear()
        
        # Process the request and get the response
        response = self.get_response(request)

        # Log database queries with details
        query_count = len(connection.queries)
        total_time = sum(float(query['time']) for query in connection.queries)
        
        print("================== >> Execution Details << ===================")
        print(f"{'*' * 13} Executed {query_count} queries in {total_time:.2f} seconds {'*' * 13}")
        print("==============================================================")
        print()
        
        return response