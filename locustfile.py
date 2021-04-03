import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    def on_start(self):
        self.client.get("/resource/123e4567-e89b-12d3-a456-426614174000")