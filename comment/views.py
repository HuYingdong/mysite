from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from comment.forms import CommentForm
from .models import Comment


def update_comment(request):
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)

    if comment_form.is_valid():
        comment = Comment(user=comment_form.cleaned_data['user'],
                          text=comment_form.cleaned_data['text'],
                          content_object=comment_form.cleaned_data['content_object'])

        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 发送邮件通知
        comment.send_mail()

        # 返回数据
        data = {
            'pk': comment.pk,
            'status': 'SUCESS',
            'username': comment.user.get_nickname_or_username(),
            'comment_time': comment.comment_time.timestamp(),
            'text': comment.text,
            'content_type': ContentType.objects.get_for_model(comment).model,
            'reply_to': comment.reply_to.get_nickname_or_username() if parent is not None else '',
            'root_pk': comment.root.pk if comment.root is not None else '',
        }
    else:
        data = {'status': 'ERROR',
                'message': list(comment_form.errors.values())[0][0]
                }
    return JsonResponse(data)
