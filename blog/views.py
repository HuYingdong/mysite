from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .utils import paginate
from .models import Blog, BlogType
from django.conf import settings
from read_statistics.utils import read_statistics


def get_context(request, queryset, each_page_number):
    context = {}
    page_num = request.GET.get('page', 1)
    current_page_list, page_range = paginate(queryset, each_page_number, page_num)

    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context['page_range'] = page_range
    context['page_of_blogs'] = current_page_list
    context['blogs'] = current_page_list.object_list
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))  # 获取博客分类的对应博客数量
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    all_blog = Blog.objects.all()
    context = get_context(request, all_blog, settings.EACH_PAGE_NUMBER)
    return render(request, 'blog/blog_list.html', context)


def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    all_blog = Blog.objects.filter(blog_type=blog_type)
    context = get_context(request, all_blog, settings.EACH_PAGE_NUMBER)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)


def blog_with_date(request, year, month):
    all_blog = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_context(request, all_blog, settings.EACH_PAGE_NUMBER)
    context['blog_date'] = '{}年{}月'.format(year, month)
    return render(request, 'blog/blog_with_date.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics(request, blog)

    context = {'blog': blog,
               'previous_blog': Blog.objects.filter(created_time__gt=blog.created_time).last(),
               'next_blog': Blog.objects.filter(created_time__lt=blog.created_time).first(),
               }
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response
