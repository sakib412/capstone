from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
GENDER = (
    ('male','Male'),
    ('female','Female'),
    ('other','Other')
)


def post_thumb_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #https://docs.djangoproject.com/en/3.0/ref/models/fields/#filefield
    return 'user_{0}/{1}-{2}'.format(instance.author.id,instance.title, filename)

def user_avatar_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #https://docs.djangoproject.com/en/3.0/ref/models/fields/#filefield
    return 'avatar/{0}-avatar-{1}'.format(instance.user.id,filename)

class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_avatar_path, default="avatar.png")
    about = models.TextField()
    birthday = models.DateField()
    gender = models.TextField(choices=GENDER, default="male")
    def __str__(self):
        return f"{self.user}"




class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_slug = models.SlugField(unique=True, max_length=60)
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return f"{self.category_name}"



class Post(models.Model):
    category = models.ForeignKey(Category, verbose_name="Category",on_delete= models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=270, unique=True)
    author = models.ForeignKey(UserExtended, on_delete= models.CASCADE,related_name='blog_posts')
    thumbnail = models.ImageField(upload_to=post_thumb_path, blank=True)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(UserExtended, on_delete= models.CASCADE,related_name='comment_author')
    body = models.TextField()
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return f"{self.body[:10]}... by {self.name}"