import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dd.settings")
django.setup()

from dangdang.models import TBook


# 创建购物车类
class ShopCar(object):
    # 初始化类属性
    def __init__(self):
        self.books = []
        self.all_price = 0
        self.save_money = 0

    def __str__(self) -> list:
        return str(self.books)

    # 类方法（增加，删除，修改）
    # 添加书籍
    def add_book(self, book_id, num=1) -> None:
        if num > 20:
            num = 20
        for i in self.books:
            if i.book.id == book_id:
                if i.num + num > 20:
                    i.num = 20
                    return

        self.books.append(Book(book_id, num))

    # 删除书籍
    def delete_book(self, book_id) -> None:
        for i in self.books:
            if i.book.id == book_id:
                self.books.remove(i)
                return

    # 修改书籍数量
    def alter_book(self, book_id, num) -> None:
        print(num, type(num))
        for i in self.books:
            print(i, 1111)
            if i.book.id == book_id:
                print(i, 222222222)
                i.num = num
                print(i.num)
                return

    def computer(self) -> None:
        self.all_price, self.save_money = 0, 0
        for i in self.books:
            self.all_price += i.small_computer
            self.save_money += i.small_save_money


# 创建书籍类
class Book(object):
    # 初始化类属性
    def __init__(self, book_id, num=1):
        self.book = TBook.objects.filter(id=book_id)[0]
        self.book_name = self.book.name
        self.num = num
        self.small_computer = float(self.book.dd_price) * self.num
        self.small_save_money = float(self.book.make_price - self.book.dd_price) * self.num

    def __str__(self) -> str:
        return str(self.book_name)


# # 测试
# if __name__ == '__main__':
#     # book = Book(book_id=12)
#     # print(book.book)
#     car = ShopCar()
#     car.add_book(1, 2)
#     # car.add_book(1, 2)
#     print(car.books[0].book)
#     # print(type(car.books[0].book))
#     # print(car.books[0].book.pid)
#     print(Book(1).book)

