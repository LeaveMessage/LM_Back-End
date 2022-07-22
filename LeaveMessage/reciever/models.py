from django.db import models
from post.models import Post

class Reciever(models.Model):
    email = models.EmailField(null=True)
    post_id = models.ForeignKey("post.Post",related_name="post", on_delete=models.CASCADE,db_column="post_id",default="")

    def __str__(self):
        return self.email