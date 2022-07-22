from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, email,name, password):
        if not email:
            raise ValueError('must have user email')
        if not name:
            raise ValueError('must have user name')
        if not password:
            raise ValueError('must have user password')
        user = self.model(
            email = email,
            name = name,
            password = password
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default='', max_length=10, null=False, blank=False)
    email= models.EmailField(default='', unique=True)
    is_auth=models.BooleanField(default=False)
    token = models.TextField(default='')

    # User 모델의 필수 field
    lifecode=models.TextField(default='')
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 nickname으로 설정
    USERNAME_FIELD = 'email'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name