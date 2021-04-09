# coding:utf-8
from django.db import models
import hashlib

def hashPwd(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    return hashlib.md5(password).hexdigest().upper()

class ClientUser(models.Model):
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    avatar = models.CharField(max_length=500, default='')
    gender = models.CharField(max_length=20, default='')
    birthday = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField(default=True, db_index=True)
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'username: {}'.format(self.username)

    @classmethod
    def add(cls, username, password, avatar='', gender='', birthday=None):
        return cls.objects.create(
            username= username,
            password= hashPwd(password),
            avatar= avatar,
            gender= gender,
            birthday= birthday,
            status= True
        )

    @classmethod
    def get_user(cls, username, password):
        try:
            user = cls.objects.get(
                username=username,
                password = hashPwd(password)
            )
            return user
        except:
            return None

    def update_password(self, password, newpassword):
        password = hashPwd(password)
        if password != self.password:
            return False
        newpassword = hashPwd(newpassword)
        self.password = newpassword
        self.save()
        return True

    def update_status(self):
        try:
            self.status = not self.status
            self.save()
            return True
        except:
            return False