import time

from django.utils.deprecation import MiddlewareMixin


class MeasureTimeExecution(MiddlewareMixin):
    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        print(f"Total execution time: {total_time}")
        return response



