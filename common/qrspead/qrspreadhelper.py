from PIL import Image, ImageDraw, ImageFont

import qrcode
import io
import os

import config


def get_spread_img(name, qrcontent, head):
    '''
    :param name: 名字
    :param qrcontent: 二维码内容
    :param head: 头像
    :return: img
    '''
    root_path = os.path.dirname(os.path.abspath(__file__))
    # 名字
    # name = '谁xxx'
    # 背景图
    if config.COMPANY == 'guoxue':
        backgroud = os.path.join(root_path, 'bg.png')
    elif config.COMPANY == 'kexuejiyi':
        backgroud = os.path.join(root_path, 'kexuejiyi-bg.png')
    # 头像，没有请给个默认值
    if config.COMPANY == 'guoxue':
        if not head:
            head = os.path.join(root_path, 'default-head.png')
    elif config.COMPANY == 'kexuejiyi':
        if not head:
            head = os.path.join(root_path, 'kexuejiyi-default-head.png')
    # 二维码内容
    # content = 'hello, qrcode'
    # 字体
    font_uri = os.path.join(root_path, 'winYH.ttf')

    # 生成二维码
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=0,
    )
    qr.add_data(qrcontent)
    qr.make(fit=True)
    img = qr.make_image()
    imgio = io.BytesIO()
    img.save(imgio, 'PNG')

    qr_img = Image.open(imgio)
    qr_img = qr_img.resize((300, 300), Image.ANTIALIAS)

    # 头像切圆
    im = Image.open(backgroud)

    box = (272, 235, 272 + 206, 441)
    region = im.crop(box)

    ima = Image.open(head).convert("RGBA")
    ima = ima.resize((206, 206), Image.ANTIALIAS)
    pima = ima.load()

    pimb = region.load()

    size = ima.size
    r2 = min(size[0], size[1])
    r = float(r2 / 2)  # 圆心横坐标

    # 切圆
    for i in range(r2):
        for j in range(r2):
            lx = abs(i - r)  # 到圆心距离的横坐标
            ly = abs(j - r)  # 到圆心距离的纵坐标
            l = pow(lx, 2) + pow(ly, 2)
            if l <= pow(r, 2):
                pimb[i, j] = pima[i, j]

    # 图片合成
    # im.paste(qr_img, (225, 580, 525, 880))
    im.paste(region, box)
    drawObj = ImageDraw.Draw(im)

    #  计算汉字和ascii的长度
    # print(sum(1 if ord(name[i]) < 128 else 2 for i in range(len(name))))
    # 添加文字
    if config.COMPANY == 'guoxue':
        Font3 = ImageFont.truetype(font_uri, 24)
        drawObj.text([375 - (12 * (5 + sum(1 if ord(name[i]) < 128 else 2 for i in range(len(name))))) / 2, 450],
                     '我是 ' + name,
                     fill=(255, 153, 19), font=Font3)
        drawObj.text([375 - (24 * 6) / 2, 490], '我为孩子改变', fill=(255, 153, 19), font=Font3)
        im.paste(qr_img, (225, 540, 525, 840))
    elif config.COMPANY == 'kexuejiyi':
        Font3 = ImageFont.truetype(font_uri, 28)
        drawObj.text([375 - (12 * (5 + sum(1 if ord(name[i]) < 128 else 2 for i in range(len(name))))) / 2, 460],
                     '我是 ' + name,
                     fill=(0, 117, 244), font=Font3)
        im.paste(qr_img, (225, 580, 525, 880))

    return im
    # 输出图片  调试输出图片
    # im.save(os.path.join(root_path, 'result.png'))

    # 实际使用输入Bytes缓存
    # resultIO = io.BytesIO()
    # im.save(resultIO,'PNG')
