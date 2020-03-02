# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(blank=True, null=True, max_length=8)
    phone = models.CharField(max_length=11, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_address'


class TBook(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)
    pic = models.CharField(max_length=100, blank=True, null=True)
    press = models.CharField(max_length=20, blank=True, null=True)
    press_date = models.DateField(blank=True, null=True)
    press_count = models.CharField(max_length=20, blank=True, null=True)
    print_date = models.DateField(blank=True, null=True)
    print_count = models.CharField(max_length=20, blank=True, null=True)
    isbn = models.IntegerField(db_column='ISBN', blank=True, null=True)  # Field name made lowercase.
    types = models.CharField(max_length=20, blank=True, null=True)
    make_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    dd_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    word_num = models.IntegerField(blank=True, null=True)
    page_num = models.SmallIntegerField(blank=True, null=True)
    book_size = models.SmallIntegerField(blank=True, null=True)
    paper = models.CharField(max_length=10, blank=True, null=True)
    pack = models.CharField(max_length=10, blank=True, null=True)
    editor_rec = models.TextField(blank=True, null=True)
    content_validity = models.TextField(blank=True, null=True)
    author_validity = models.TextField(blank=True, null=True)
    list = models.TextField(blank=True, null=True)
    media_reviews = models.TextField(blank=True, null=True)
    illustrate = models.TextField(db_column='Illustrate', blank=True, null=True)  # Field name made lowercase.
    pid = models.ForeignKey('TCategory', models.DO_NOTHING, db_column='pid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_book'


class TCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_category'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    order_id = models.CharField(max_length=30, blank=True, null=True)
    order_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    all_price = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_order'


class TOrderAll(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    order = models.ForeignKey(TOrder, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_order_all'


class TShopCar(models.Model):
    id = models.IntegerField(primary_key=True)
    all_price = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    make_prices = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_shop_car'


class TShopCarAll(models.Model):
    id = models.IntegerField(primary_key=True)
    shop_status = models.IntegerField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    car = models.ForeignKey(TShopCar, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_shop_car_all'


class TUser(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=30, blank=True, null=False, unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=1000, blank=True, null=False)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_user'























