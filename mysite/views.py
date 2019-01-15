import datetime
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from blog.models import Blog
from read_statistics.utils import get_seven_days_read_data, get_hot_data


def get_hot_blogs(day_num):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=day_num)
    blogs = Blog.objects.filter(read_detail__date__range=[date, today]).values(
        'id', 'title').annotate(read_num_sum=Sum('read_detail__read_num')).order_by(
        '-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    seven_days_hot_data = cache.get('seven_days_hot_data')
    if seven_days_hot_data is None:
        seven_days_hot_data = get_hot_blogs(7)
        cache.set('seven_days_hot_data', seven_days_hot_data, 3600)

    context = dict()
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_hot_data(blog_content_type, 'yesterday')
    context['seven_days_hot_data'] = seven_days_hot_data
    return render(request, 'home.html', context)
