import string
import time
import hashlib
import random
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect
from dangdang.models import *
from dangdang.book import ShopCar
from django.http import JsonResponse
from django.core.mail import send_mail

# Create your views here.


# --------------------------------------------------------------------------------------------
# ---------------------------用户模块---------------------------------------------------------
# --------------------------------------------------------------------------------------------


# 退出登陆逻辑
def out_login(request):
    # 删除session中的account，login_status
    del request.session["account"]
    del request.session["login_status"]
    # del request.session['addr']
    res = redirect('dang:show_index')
    # 删除浏览器中的cookie（账号，密码）
    res.set_cookie('account', "", max_age=0)
    res.set_cookie('password', "", max_age=0)
    return res


# 渲染注册页面
def register(request):
    return render(request, 'register.html')


# 判断注册的账号是否存在
def account_exist(request):
    # 获取用户的账号（手机号或邮箱号）
    account = request.POST.get('account')
    # 从库表中查询账号
    user = TUser.objects.filter(email=account)
    # 返回响应，1代表新账号，0代表账号已存在
    return HttpResponse(0 if user else 1)


# # 生成验证码图片
# def get_captcha(request):
#     # 实例化对象
#     image = ImageCaptcha(font_sizes=(42, 50, 56))
#     # 随机生成4个数字
#     code = random.sample(string.ascii_letters + string.digits, 4)
#     # 将code拼接成一个字符串
#     random_code = "".join(code)
#     # 将字符串存入session中
#     request.session["code"] = random_code
#     # 将字符串写到图片中
#     data = image.generate(random_code)
#     # 返回响应
#     return HttpResponse(data, 'image/png')


# 验证码
def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)  # RGB模式下的颜色信息


def get_captcha(request):
    img_obj = Image.new('RGB', (100, 50), get_random())  # 创建图片  长100 宽50
    img_draw = ImageDraw.Draw(img_obj)  # 生成画笔
    img_font = ImageFont.truetype(r'C:\Windows\Fonts\lucon.ttf', 40)  # 字体和文字大小
    # # 随机生成4个数字
    # code = random.sample(string.ascii_letters + string.digits, 4)
    # # 将code拼接成一个字符串
    # code = "".join(code)
    upper_str = chr(random.randint(65, 90))  # 利用ASCII码来生成大写小写的的文字
    lower_str = chr(random.randint(97, 122))  # 大写
    num_str = str(random.randint(0, 9))  # 数字
    code = ''
    for i in range(4):  # 每次随机拿出一个字母或者数字
        res = random.choice([upper_str, lower_str, num_str])
        img_draw.text((10 + i * 20, 10), res, get_random(), img_font)
        code += res
    io_obj = BytesIO()  # 生成二进制文件对象
    img_obj.save(io_obj, 'png')  # 将生成的验证码图片存入文件对象中
    request.session['code'] = code
    # print(code)
    return HttpResponse(io_obj.getvalue(), "image/png")


# 验证码判断
def judge_captcha(request):
    # 获取code中的验证码
    code_1 = request.session.get("code").lower()
    # 获取前端页面的验证码
    code_2 = request.GET.get("code").lower()
    # 判断验证码,1表示验证码输入正确，0表示验证码输入错误
    return HttpResponse(1 if code_1 == code_2 else 0)


# 注册逻辑
def register_ok(request):
    # 获取注册账号
    account = request.POST.get("txt_username")
    # 获取密码
    password = request.POST.get("txt_password")
    password = password if password else "0"
    password = add_password(password)
    print(password)
    if account and password:
        # 向数据库添加数据
        try:
            with transaction.atomic():
                # 向用户表张红添加用户信息,购物车
                TUser.objects.create(email=account, password=password)
                TShopCar.objects.create()
            # 获取数据库中对应的用户信息,及购物车
            user = TUser.objects.filter(email=account, password=password)[0]
            car = TShopCar.objects.filter(user_id=None)[0]
            # 将用户与购物车进行绑定
            user.tshopcar_set.add(car)
            # 获取session中的书籍
            books = request.session.get('books')
            if books:
                for book in books.books:
                    car_add_book(car, book.book.id, book.num)
                del request.session['books']
            # 用户状态保存到session中
            # 存储账号，及登录状态
            request.session["account"] = account
            request.session['login_status'] = 1

            # 获取session中的car
            addr = request.session.get('addr')
            print(addr)
            addr = addr if addr else "0"
            res = render(request, 'register ok.html', {'account': account, 'car': addr})
            return res
        except Exception as a:
            # print(a)
            return redirect('dang:register')
    else:
        return redirect('dang:register')


# # # 发送邮箱验证码
# def email_captcha(request):
#     email = request.POST.get('email')
#     info = random.sample(string.digits, 4)
#     info = "".join(info)
#     print(info)
#     send_mail('验证码', info, 'xhl_dian@sina.cn', [email])
#     res = HttpResponse(1)
#     res.set_cookie('info', info, max_age=60)
#     return res
#
#
# # 邮箱
# def email_logic(request):
#     info1 = request.COOKIES.get("info")
#     info2 = request.POST.get("info")
#     res = 1 if info1 == info2 else 0
#     return HttpResponse(res)


# 登录页面
def login(request):
    # 获取cookie：账号密码
    account = request.COOKIES.get("account")
    password = request.COOKIES.get("password")
    password = password if password else "0"
    print(request.COOKIES)
    # 查询账号
    user = TUser.objects.filter(email=account, password=password)
    print(user)
    if user:
        # password = add_password(password)
        # 存储账号，及登录状态
        request.session["account"] = account
        request.session['login_status'] = 1

        # 查询用户对应的购物车
        car = user[0].tshopcar_set.get(user_id=user[0].id)
        add_car(request, car)

        # 获取addr，addr表示从购物车跳转到登录
        addr = request.session.get("addr")
        if addr:
            # car存在跳转到购物车的地址页面
            return redirect('dang:indent')
        # addr不存在，跳转到首页（show_index）
        return redirect('dang:show_index')
    # 如果cookie中没有存取用户信息，则渲染登录页面
    return render(request, 'login.html')


# 登录逻辑
def login_logic(request):
    # 获取账号，密码，“记住我”
    account = request.POST.get("txtUsername")
    password = request.POST.get("txtPassword")
    password = add_password(password)
    remember = request.POST.get("auto_login")
    addr = request.session.get('addr')
    # 查询account对应得账号
    user = TUser.objects.filter(email=account)
    # 判断user是否存在，且账号的密码是否与用户输入的账号匹配
    if user and user[0].password == password:
        if addr:
            # del request.session['addr']
            res = redirect('dang:indent')
        else:
            res = redirect('dang:show_index')

        if remember:
            res.set_cookie('account', account, max_age=7 * 24 * 3600)
            res.set_cookie('password', password, max_age=7 * 24 * 3600)
        # 将登陆状态和用户名存入session
        request.session["login_status"] = 1
        request.session["account"] = account

        # 查询用户对应的购物车
        car = user[0].tshopcar_set.get(user_id=user[0].id)
        add_car(request, car)
        return res
    else:
        return redirect('dang:login')


# 获取session中书籍信息，登录后将其添加到购物车
def add_car(req, car: TShopCar):
    books = req.session.get("books")
    if books:
        for book in books.books:
            book_id = book.book.id
            num = book.num
            car_add_book(car, book_id, num)
        # 将session中存储的书籍信息删除
        del req.session["books"]


# 密码加密
def add_password(password: str) -> str:
    h = hashlib.sha256()
    h.update(password.encode())
    pwd = h.hexdigest()
    return pwd

# --------------------------------------------------------------------------------------------
# ---------------------------书籍展示模块---------------------------------------------------------
# --------------------------------------------------------------------------------------------


def check():
    # 获取一级分类信息
    one_category = TCategory.objects.filter(pid=None)
    # 获取二级分类信息
    two_category = TCategory.objects.filter(pid__isnull=False)
    return one_category, two_category


# 展示首页
def show_index(request):
    # 获取session中用户名
    account = request.session.get("account")
    one_category, two_category = check()
    # 按出版时间获取最新的8本书籍
    new_books = TBook.objects.all().order_by("-press_date")[:8]
    # 获取价格最高的12本书籍
    re_books = TBook.objects.all().order_by('-dd_price')[:12]
    # 获取最新价格最高的10本书籍
    new_re_books = TBook.objects.all().order_by('-press_date', '-dd_price')[:10]
    # 渲染前端页面（index.html）
    return render(request, 'index.html', {
        'account': account,
        'one_category': one_category,
        'two_category': two_category,
        'new_books': new_books,
        're_books': re_books,
        'new_re_books1': new_re_books[:5],
        'new_re_books2': new_re_books,
    })


# 展示书籍的分类展示
def show_book_list(request):
    # 获取session中用户名
    account = request.session.get("account")
    # url中的分类id
    category_id = request.GET.get('id')
    if category_id:
        try:
            TCategory.objects.get(id=category_id)
        except:
            category_id = 1
        # 将category_id存入session
        request.session['category_id'] = category_id
    else:
        category_id = request.session.get('category_id')
        category_id = category_id if category_id else 1
    # # 判断category_id是否存在，不存在时，默认为1
    category_id = category_id if category_id else 1

    # 创建一个空的QuerySet对象
    books_query = TBook.objects.filter(name="#####################")
    # 获取category_id对应的分类
    category = TCategory.objects.filter(id=category_id)
    # 判断category的分类级别,通过models对象的pid是否为空来判断
    if category[0].pid is None:
        # 条件成立，表示category为一级标题
        # 查询分类的pid为category_id
        two_category = TCategory.objects.filter(pid=category_id)
        # 遍历一级分类
        for i in two_category:
            # 查询二级分类下的书籍
            book = TBook.objects.filter(pid=i.id)
            # 将查询到的书籍添加到创建的books_query对象中
            books_query = books_query | book
    else:
        # 否则category为二级分类
        books_query = TBook.objects.filter(pid=category_id)

    # 创建分页器对象
    paginator = Paginator(books_query, per_page=4)
    # 获取页码
    num = request.GET.get('num')
    try:
        page = paginator.page(num)
    except:
        page = paginator.page(1)
    books = page.object_list
    one_category, two_category2 = check()
    # 渲染书籍分类页面
    return render(request, 'booklist.html', {'account': account,
                                             'one_category': one_category,
                                             'two_category': two_category2,
                                             'books': books,
                                             'page_num': paginator,
                                             'page': page})


# 书籍详情页
def book_detail(request):
    book_id = request.GET.get('book_id')
    try:
        book = TBook.objects.get(id=book_id)
    except:
        book = TBook.objects.get(id=1)
    two_category = book.pid
    one_category = TCategory.objects.get(id=two_category.pid)
    account = request.session.get('account')
    return render(request, 'Book details.html', {"book": book,
                                                 "one_category": one_category,
                                                 "two_category": two_category,
                                                 "account": account,
                                                 })


# --------------------------------------------------------------------------------------------
# ---------------------------购物车模块-------------------------------------------------------
# --------------------------------------------------------------------------------------------


# 购物车页面
def shop_car(request):
    # 获取session中在线的用户名
    account = request.session.get("account")
    # 获取session中的书籍信息
    books = request.session.get("books")
    all_books = []
    # 情况一：account存在，获取数据库购物车中的书籍信息
    if account:
        # 通过account获取用户的id，对应的购物车id
        user_id = TUser.objects.filter(email=account)[0]
        car = TShopCar.objects.filter(user_id=user_id)[0]
        # 获取购物车中用户正常存储的书籍信息
        all_books = query_book(car)

    # 情况二：用户没有登录，书籍信息存储在session中
    elif books:
        all_books = [[book.book, book.num] for book in books.books]
    return render(request, 'car.html', {"account": account, 'all_books': all_books})


# 购物车书籍详情查询
def query_book(car, shop_status=1):
    """
    :param car: 购物车
    :param shop_status: 商品状态（1：正常，0：恢复区）
    :return: list
    """
    all_books = []
    car_all = TShopCarAll.objects.filter(car_id=car.id, shop_status=shop_status)
    # print(car_all)
    # 通过购物车详情表查询书籍表
    for i in car_all:
        book = TBook.objects.filter(id=i.book_id)
        if book:
            all_books.append([book[0], i.num])
    return all_books


# 添加修改商品数量
def alter_book(request):
    # print(request.POST)
    # 获取商品id,数量
    book_id = request.POST.get("book_id")
    num = request.POST.get('num')
    num = int(num) if num else 1
    # 获取在线用户id
    account = request.session.get("account")
    users = TUser.objects.filter(email=account)
    # 判断是否存在在线用户
    if users:
        # 用户存在的情况
        user_id = users[0].id
        car = TShopCar.objects.filter(user_id=user_id)[0]
        # 调用函数，向购物车中添加书籍
        alter_add_book(book_id, car, num)
        computer_car_price(car)
        return HttpResponse(1)

    # 用户不存在的情况
    # 从session中获取书籍信息
    books = request.session.get('books')
    books = books if books else ShopCar()
    books.alter_book(int(book_id), num)

    # 将书籍信息存入session中
    request.session['books'] = books
    # 返回响应
    return HttpResponse(1)


# 删除书籍
def del_book(request):
    book_id = request.POST.get("book_id")
    books = request.session.get('books')
    account = request.session.get('account')
    user = TUser.objects.filter(email=account)
    if user:
        car = del_book_logic(user, book_id)
        computer_car_price(car)
        return HttpResponse(1)
    elif books:
        books.delete_book(int(book_id))
        request.session['books'] = books
        return HttpResponse(1)
    else:
        return HttpResponse(0)


# 删除书籍逻辑
def del_book_logic(user, book_id):
    # 获取用户对应的购物车
    car = user[0].tshopcar_set.filter(user_id=user[0].id)
    # 获取用户要删除的书籍，将书籍状态转为0
    car_one = car[0].tshopcarall_set.get(book_id=book_id, car_id=car[0].id)
    # 删除书籍
    # car_one.shop_car = 0
    car_one.delete()
    computer_car_price(car[0])
    return car[0]


# 计算购物率总价
def computer_car_price(car: TShopCar):
    """
    :param car:用户的购物车
    :return: float or none
    """
    # 获取用户购物车的书籍信息（数量，单价）
    books = car.tshopcarall_set.filter(car_id=car.id)
    try:
        if books:
            all_prices = 0
            make_prices = 0
            for book in books:
                # 获取书籍的详细信息（数量，当当价，市场价）
                num = book.num
                dd_price = book.book.dd_price
                mk_price = book.book.make_price
                all_prices += num * dd_price
                make_prices += num * mk_price
            car.all_price = all_prices
            car.make_prices = make_prices
        else:
            car.all_price = 0
            car.make_prices = 0
        car.save()
        return
    except:
        return


# 修改购物车中书籍逻辑
def alter_add_book(book_id, car, num=1) -> bool:
    # 判断购物车详情表中是否存在book_id
    book = TShopCarAll.objects.filter(book_id=book_id, car_id=car.id)[0]
    try:
        with transaction.atomic():
            book.num = num
            book.save()
        return True
    except Exception as a:
        print(a)
        return False


# 向购物车中添加书籍
def add_book(request):
    # print(request.POST)
    # 获取书籍id
    book_id = request.POST.get("book_id")
    try:
        TBook.objects.get(id=book_id)
    except:
        book_id = 1
    # 获取书籍数量，当num不存在时：num=1
    num = request.POST.get("num")
    num = int(num) if num else 1
    # 获取session 中account
    account = request.session.get("account")
    if account:
        # 情况一： 用户处于登录状态
        # 获取用户信息，及购物车信息
        user = TUser.objects.get(email=account)
        car = user.tshopcar_set.get(user_id=user.id)
        flag = car_add_book(car, book_id, num)
        return HttpResponse(1 if flag else 0)

    # 情况二： 用户没有登录状态
    # 获取session中的books
    books = request.session.get("books")
    books = books if books else ShopCar()
    books.add_book(int(book_id), int(num))
    request.session['books'] = books
    return HttpResponse(1)


# 向购购车中添加书籍
def car_add_book(car: TShopCar, book_id: int, num: int) -> bool:
    cars_all = car.tshopcarall_set.filter(book_id=book_id, car_id=car.id)
    try:
        with transaction.atomic():
            if cars_all:
                car_all = cars_all[0]
                if car_all.num + num > 20:
                    car_all.num = 20
                else:
                    car_all.num += num
                car_all.save()
            else:
                TShopCarAll.objects.create(num=num, book_id=book_id, car=car, shop_status=1)
            computer_car_price(car)
            return True
    except:
        return False

# --------------------------------------------------------------------------------------------
# ---------------------------地址模块---------------------------------------------------------
# --------------------------------------------------------------------------------------------


# 渲染地址页面
def indent(request):
    if request.session.get('addr'):
        del request.session['addr']
        # 获取session中account
        account = request.session.get('account')
        # 获取用户购物车中总价
        user = TUser.objects.get(email=account)
        car = user.tshopcar_set.get(user_id=user.id)

        # 在session中存入标记
        request.session['flag'] = 1
        # 获取用户历史订单地址
        address = user.taddress_set.filter(user_id=user.id)
        return render(request, 'indent.html', {"account": account, "all_price": car.all_price, 'address': address})
    return redirect('dang:show_index')


# 地址信息查询
def query_addr(request):
    addr_id = request.POST.get('addr_id')
    addr = TAddress.objects.filter(id=addr_id).values()
    return JsonResponse(addr[0])


# 跳转页面
def skip_page(request):
    # print(request.GET)
    car = request.GET.get("car")  # 获取路径中值
    request.session['addr'] = car  # 将car存入session中
    # print(car)
    account = request.session.get("account")
    if account:
        return redirect('dang:indent')
    return redirect('dang:login')


# 订单成功页面
def indent_logic(request):
    if not request.session.get('flag'):
        return redirect('dang:show_index')
    del request.session['flag']
    # 获取session中account
    account = request.session.get('account')
    # 获取用户购物车中总价
    user = TUser.objects.get(email=account)
    car = user.tshopcar_set.get(user_id=user.id)

    # 获取form表单中的数据
    name = request.POST.get('username')
    address = request.POST.get('addr')
    zip_code = request.POST.get('zipCode')
    phone = request.POST.get('phone')

    # 查询数据库是否存在此数据.如果存在，不添加地址
    try:
        with transaction.atomic():
            user.taddress_set.get_or_create(name=name, address=address, zip_code=zip_code, phone=phone)
    except Exception as a:
        print(a)
        pass

    # 获取用户订单中的书籍信息，并添加到订单表中
    addr = TAddress.objects.filter(name=name, address=address, zip_code=zip_code, phone=phone, user_id=user.id)
    order_id = random.sample(string.digits, 10)
    order_id = "".join(order_id)
    order_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    all_prices = car.all_price

    try:
        with transaction.atomic():
            TOrder.objects.create(order_id=order_id, order_time=order_time, all_price=all_prices, user=user, address=addr[0])
    except Exception as a:
        print(a)
        pass

    # 用户订单详情表中的
    order = TOrder.objects.get(order_id=order_id, order_time=order_time, all_price=all_prices,
                               user_id=user.id, address_id=addr[0].id)
    car_detail = car.tshopcarall_set.filter(car_id=car.id)
    try:
        with transaction.atomic():
            for i in car_detail:
                TOrderAll.objects.create(num=i.num, book_id=i.book_id, order=order)
    except Exception as a:
        print(a)
        pass

    # 将用户已购买的书籍从购物车中删除
    car_all = car.tshopcarall_set.filter(car_id=car.id)
    try:
        with transaction.atomic():
            car_all.delete()
    except:
        pass

    return render(request, 'indent ok.html', {'account': account, 'all_price': all_prices, 'order_id': order_id, 'name': addr[0].name})





