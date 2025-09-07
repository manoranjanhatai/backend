from django.db import models

class DisasterAlert(models.Model):  # Renamed Model
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} - {self.timestamp}"
