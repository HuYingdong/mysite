# python manage.py shell

from blog.models import Blog, BlogType
from django.contrib.auth.models import User

Blog.objects.all()

Blog.objects.all().count()

blog_type1 = BlogType.objects.all()[0]

user1 = User.objects.all()[0]
for i in range(1, 31):
    blog = Blog(title='title_%s' % i, content='xxxxxxxxxxxxxxxxxxx%s' % i,
                blog_type=blog_type1, author=user1)
    blog.save()


Blog.objects.all().count()

# 分页器
from django.core.paginator import Paginator

paginator = Paginator(Blog.objects.all(), 10)
page1 = paginator.page(1)
