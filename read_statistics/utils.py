import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum, ReadDetail


def read_statistics(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        #  总阅读数 +1
        read_num_obj, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        read_num_obj.read_num += 1
        read_num_obj.save()
        # 当天阅读数 +1
        date = timezone.now().date()
        read_detail_obj, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        read_detail_obj.read_num += 1
        read_detail_obj.save()
    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_deatils = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_deatils.aggregate(read_num_sum=Sum('read_num'))

        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_hot_data(content_type, date='today'):
    today = timezone.now().date()
    if date == 'yesterday':
        yesterday = today - datetime.timedelta(days=1)
        read_details = ReadDetail.objects.filter(
            content_type=content_type, date=yesterday).order_by('-read_num')
    else:
        read_details = ReadDetail.objects.filter(
            content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]
