from localstack.extensions.api import Extension, http, aws

import requests
from concurrent.futures import ThreadPoolExecutor


class AWSAudio(Extension):
    name = "awsaudio"

    def __init__(self):
        self.hashed_notes = {}
        self.pool = ThreadPoolExecutor()

    def update_request_handlers(self, handlers: aws.CompositeHandler):
        def inner(chain, ctx, response):
            if not ctx.request:
                return
            if not ctx.service:
                return

            # send in the background
            # self.pool.submit(self.send_request, service=ctx.service.service_name)
            self.send_request(ctx.service.service_name)

        print("ADDING HANDLER")
        handlers.append(inner)

    @staticmethod
    def send_request(service: str):
        requests.post("http://192.168.0.10:5000", json={"service": service})
