import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.contrib import auth
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, reverse


from utils.response import Response
from utils.consts import *

# 随机生成验证码背景色
def get_random_background():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# 验证码视图
def get_code_image(request):
    img_obj = Image.new(mode='RGB', size=(166, 36), color=get_random_background())  # 产生一个图片对象
    img_draw = ImageDraw.Draw(img_obj)  # 产生一个画笔对象
    img_font = ImageFont.truetype('static/font/111.ttf', 32)  # 字体样式  字体大小

    code = ''
    # 随机生成6个验证码（数字、大写字母、小写字母）
    for i in range(4):
        upper_num = chr(random.randint(65, 90))
        lower_num = chr(random.randint(97, 122))
        num = str(random.randint(0, 9))
        tem_code = random.choice([upper_num, lower_num, num])
        # 将选中的随机验证码写入图片
        img_draw.text((i * 37 + 20, 5), tem_code, get_random_background(), img_font)
        # 拼接随机验证码
        code += tem_code
    print("验证码：", code)

    # 将随机验证码保存在redis中
    cache.set(settings.CODE_KEY, code, settings.CODE_EXPIRED)

    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


def login(request):
    """
    登录视图
    :param request:
    :return:
    """
    response = Response()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        # 为空校验
        if not all([username, password, code]):
            response.set_code_and_message(PARAMS_ERR_MSG)
            return JsonResponse(response.data)
        # 验证码校验
        cache_code = cache.get(settings.CODE_KEY) if cache.get(settings.CODE_KEY) else ""
        if code.upper() != cache_code.upper():
            response.set_code_and_message(CODE_ERR_MSG)
            return JsonResponse(response.data)
        # 密码校验
        user = auth.authenticate(request, username=username, password=password)
        if user:  # 登录成功
            auth.login(request, user)
            response.set_code_and_message(SUCCESS_MSG)
            response.data['url'] = reverse('backend:index')
            return JsonResponse(response.data)
        else:
            response.set_code_and_message(LOGIN_ERR_MSG)
            return JsonResponse(response.data)

    return render(request, 'b-base/login.html')
