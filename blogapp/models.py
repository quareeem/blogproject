from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User 
from mptt.models import MPTTModel, TreeForeignKey

def user_dir_path(instance, filename):
    return f'posts/{instance.id}/{filename}'



class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Post(models.Model):

    class CustomManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')


    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    image = models.ImageField(upload_to=user_dir_path, default='posts/default.jpg')
    status = models.CharField(max_length=10, choices=options, default='draft')

    objects = models.Manager()
    custom_manager = CustomManager()


    class Meta:
        ordering = ('-publish_date',)

    def get_absolute_url(self):
        return reverse("blog:post_single", args=[self.slug])
    

    def __str__(self) -> str:
        return self.title



class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta: 
        order_insertion_by = ['publish',]
    
    def __str__(self) -> str:
        return f'Comment by {self.name}'