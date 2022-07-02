import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render


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
    if request.method == "POST":
        pass
    return render(request, 'b-base/login.html')
