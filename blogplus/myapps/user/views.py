import json
import uuid

import os

from django.contrib.auth.hashers import check_password, SHA1PasswordHasher
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from XartPro import settings
from user.forms import UserForm
from user.models import UserProfile

from helper.valid_field import valid_required

def regist(request):
    if request.method == 'POST':
        # print('client-ip>', requst.META.get('REMOTE_ADDR'))
        form = UserForm(request.POST)

        # 验证form表单中必填项是否满足条件
        if form.is_valid():
            user = form.save()  # 验证成功
            # 将用户信息(id, nickname, photo)保存到session中
            request.session['login_user'] = json.dumps({'id': user.id,
                                                        'nickname': user.nickname,
                                                        'photo': user.photo})
            return redirect('/')
        else:
            errors = json.loads(form.errors.as_json())

    return render(request, 'user/regist.html', locals())


@csrf_exempt
def upload(request):
    '''
    ｜ 注册用户提交之前，多次点击图片，
    ｜ 造成注册一位用户会产生多个异步上传的图片，如何解决？
    ajax上传图片接口
    :param request:  HttpRequest/WSGIRequest 请求对象
    :return:  JsonResponse对象，数据格式{'code':200,'path':'user/xx.jpg','msg':''}
    '''
    if request.method == 'POST':
        # 获取上传的文件对象
        photo: InMemoryUploadedFile = request.FILES.get('photo')

        # 生成新的文件名
        fileName = str(uuid.uuid4()).replace('-', '')+os.path.splitext(photo.name)[-1]
        filePath = os.path.join(settings.MEDIA_ROOT, 'user/'+fileName)
        with open(filePath, 'wb') as f:
            for chunk in photo.chunks():
                f.write(chunk)
        return JsonResponse({'code': 200,
                             'path': 'user/'+fileName})

    return JsonResponse({'code': 101,
                         'msg': '图片上传仅支持POST请求'})


def logout(request):
    # 删除session的login_user
    del request.session['login_user']
    return redirect('/')


def login(request):
    if request.method == 'POST':
        # 先以用户名查询用户，再验证口令(check_password)
        errors = {}
        username = request.POST.get('username')
        password = request.POST.get('password')

        valid_required('name', '账号', username, errors)
        valid_required('pwd', '口令', password, errors)

        # 判断验证是否存在错误
        if not errors:
            user_qs = UserProfile.objects.filter(username=username)
            if not user_qs.exists():
                errors['name'] = '%s 用户不存在' % username
            else:
                user = user_qs.first()  # 从查询结果中获取第一条数据
                if not check_password(password, user.password):
                    errors['pwd'] = '口令验证失败'
                else:
                    # 登录成功
                    request.session['login_user'] = json.dumps({
                        'id': user.id,
                        'nickname': user.nickname,
                        'photo': user.photo
                    })
                    return redirect('/')


    return render(request,
                  'user/login.html',
                  locals())