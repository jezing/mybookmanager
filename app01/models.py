from django.db import models
import random


# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.pk}.{self.name}"


class BOOK(models.Model):
    name = models.CharField(max_length=32)
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE)
    """
    on_delete 选项django2.0后必须要填
    models.CASCADE：级联删除
    models.PROTECT: 保护，当外键仍然在被引用时，不予许删除外键所在表的键
    models.SET（value）：删除后设置成某个value值
    models.SETDEFAULE：删除后设置成默认值。后面还需要加个default=value
    models.SET_NULL：删除后设置为Null
    """

    price = models.DecimalField(max_digits=5, decimal_places=2,
                                default=float(random.randint(10, 50)) - 0.11 * random.randint(0, 10))  # 999.99
    sale = models.IntegerField(default=random.randint(0, 50))  # 销量
    stock = models.IntegerField(default=random.randint(50, 100))  # 库存

    def __str__(self):
        return f"{self.publisher}.{self.name}"


class Author(models.Model):
    name = models.CharField(max_length=32)
    books = models.ManyToManyField("BOOK")  # 不在Author表中新增字段的话，会创建第三张表

    def __str__(self):
        return f"{self.name}"
