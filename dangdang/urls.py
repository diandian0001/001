from django.urls import path
from dangdang import views


app_name = 'dang'

urlpatterns = [
    path('show_index/', views.show_index, name='show_index'),
    path('show_book_list/', views.show_book_list, name='show_book_list'),
    path('book_detail/', views.book_detail, name='book_detail'),
    path('shop_car/', views.shop_car, name='shop_car'),
    path('register/', views.register, name='register'),
    path('account_exist/', views.account_exist, name='account_exist'),
    path('get_captcha/', views.get_captcha, name='get_captcha'),
    path('judge_captcha/', views.judge_captcha, name='judge_captcha'),
    path('register_ok/', views.register_ok, name='register_ok'),
    path('login/', views.login, name='login'),
    path('login_logic/', views.login_logic, name='login_logic'),
    path('out_login/', views.out_login, name='out_login'),
    path('alter_book/', views.alter_book, name='alter_book'),
    path('add_book/', views.add_book, name='add_book'),
    path('del_book/', views.del_book, name='del_book'),
    path('indent/', views.indent, name='indent'),
    path('indent_logic/', views.indent_logic, name='indent_logic'),
    path('skip_page/', views.skip_page, name='skip_page'),
    path('query_addr/', views.query_addr, name='query_addr'),
    # path('email_captcha/', views.email_captcha, name='email_captcha'),
    # path('email_logic/', views.email_logic, name='email_logic'),
]

