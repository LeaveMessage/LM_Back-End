from django.db import models
from sympy import content
from user.models import User


class Post(models.Model):
    content = models.TextField()
    deadline_date = models.DateTimeField(auto_now_add=True)
    cycle = models.IntegerField()
    count = models.IntegerField()
    user_id = models.ForeignKey("user.User", related_name="user", on_delete=models.CASCADE, db_column="user_id")

    def __str__(self):
        return self.content