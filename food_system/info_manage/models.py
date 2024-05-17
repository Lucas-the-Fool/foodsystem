from django.db import models


class UserInfoModel(models.Model):
    username = models.CharField(max_length=100, verbose_name='user name')
    password = models.CharField(max_length=100, verbose_name='password')
    address = models.CharField(max_length=100, verbose_name='address')
    phone = models.CharField(max_length=100, verbose_name='phone')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create_time')

    class Meta:
        db_table = 'db_user_info'
        verbose_name = 'user information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class CategoryModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')

    class Meta:
        db_table = 'db_category'
        verbose_name = 'category information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class FoodModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    image = models.ImageField(upload_to='', max_length=300, verbose_name='image')
    content = models.TextField(verbose_name='info')
    view_count = models.IntegerField(default=0, verbose_name='view count')

    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE, verbose_name='use category')

    class Meta:
        db_table = 'db_food'
        verbose_name = 'food information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class LikeModel(models.Model):
    food = models.ForeignKey('FoodModel', on_delete=models.CASCADE, verbose_name='use food')
    user = models.ForeignKey('UserInfoModel', on_delete=models.CASCADE, verbose_name='use user')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create time')

    class Meta:
        db_table = 'db_like'
        verbose_name = 'user like'
        verbose_name_plural = verbose_name


class HotModel(models.Model):
    food = models.ForeignKey('FoodModel', on_delete=models.CASCADE, verbose_name='hot food')

    class Meta:
        db_table = 'db_hot'
        verbose_name = 'hot food'
        verbose_name_plural = verbose_name


class CommentModel(models.Model):
    user = models.ForeignKey('UserInfoModel', on_delete=models.CASCADE, verbose_name='use user')
    food = models.ForeignKey('FoodModel', on_delete=models.CASCADE, verbose_name='use food')
    content = models.TextField(verbose_name='comment content')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create time')

    class Meta:
        db_table = 'db_comment'
        verbose_name = 'comment information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class MarkModel(models.Model):
    user = models.ForeignKey('UserInfoModel', on_delete=models.CASCADE, verbose_name='use user')
    item = models.ForeignKey('FoodModel', on_delete=models.CASCADE, verbose_name='use food')
    score = models.IntegerField(default=5, verbose_name='mark')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create_time')

    class Meta:
        db_table = 'db_mark'
        verbose_name = 'mark information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
