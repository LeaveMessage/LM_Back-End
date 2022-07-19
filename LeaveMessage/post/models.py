from django.db import models


class Post(models.Model):
    description = models.TextField()
    deadline_date = models.DateTimeField(auto_now_add=True)
    cycle = models.IntegerField()
    count = models.IntegerField()
    user_id = models.ForeignKey("User", related="user", on_delete=models.CASCADE, db_column="user_id")

    def __str__(self):
        return self.description
