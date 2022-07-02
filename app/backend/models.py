from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    昵称      nickname
    用户名    username
    密码      password
    邮箱      email
    头像      avatar
    描述      describe
    是否删除   is_delete
    创建时间   create_time
    更新时间   update_time
    """

    # 基础字段
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    avatar = models.ImageField(upload_to='user_avatar/', default='user_avatar/default.png', verbose_name='用户头像')
    describe = models.CharField(max_length=255, verbose_name='简介')

    # 外键字段

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'blog_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
