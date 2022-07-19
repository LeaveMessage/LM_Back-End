from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    password = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name