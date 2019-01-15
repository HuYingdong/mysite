def paginate(queryset, each_page_number, page):
    from django.core.paginator import Paginator
    paginator = Paginator(queryset, each_page_number)
    current_page_list = paginator.get_page(page)
    current_page_num = current_page_list.number  # 获取当前页码
    total_num_pages = paginator.num_pages  # 总页数
    page_range = list(range(max(current_page_num - 2, 1), min(current_page_num + 2, total_num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if total_num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != total_num_pages:
        page_range.append(total_num_pages)
    return current_page_list, page_range



