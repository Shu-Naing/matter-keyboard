from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class QA(models.Model):
    question = models.TextField()
    answer = models.TextField()
    device_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class CheckDevice(models.Model):
    device_id = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    client_data = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

class RequestResponse(models.Model):
    request_text = models.TextField()
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ErrorLog(models.Model):
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.PositiveIntegerField()
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} ({self.status_code})"