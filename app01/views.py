from django.shortcuts import render, redirect, HttpResponse, reverse
from app01 import models
from django.views import View
from django.utils.decorators import method_decorator
import time
from functools import wraps
import json
from django.http.response import JsonResponse
from functools import wraps


# 确认是否已经登录的装饰器
def login_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        print(request.COOKIES)
        is_login = request.COOKIES.get("is_login")
        if is_login != "1":
            # 没有登录跳转到相对应的界面
            return redirect("/login/?url={}".format(request.path_info))
        ret = func(request, *args, **kwargs)
        return ret

    return inner


# 测试json
def get_json(request):
    data = {"k2": "v2"}
    # return HttpResponse(json.dumps({"k1": "v1"}))  # Content-Type: text/html; charset=utf-8
    return JsonResponse(data)  # Content-Type: application/json


# 运行时间计算器
def timer(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        start = time.time()
        ret = func(request, *args, **kwargs)
        print(f"run time :{time.time() - start}")
        return ret

    return inner


# Create your views here.

class Login(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")

        if user == "root" and pwd == "admin":
            url = request.GET.get("url")
            ret = redirect(reverse(url) if url else reverse("publisher"))
            ret.set_cookie("is_login", "1")
            return ret
        else:
            error = "*plz check your name and password"
            return render(request, "login.html", locals())


# 展示出版社
# @timer
def publisher_list(request):
    # 从数据库获取出版社名称
    # 通过order_by进行字段排序，id为升序，-id为降序
    all_pub = models.Publisher.objects.all().order_by("id")
    # for i in all_pub:
    #     print(i)
    #     print(i.id, i.name)
    # 然后用一个页面返回
    return render(request, "publisher_list.html", {"all_pub": all_pub})


# CBV重构 publisher_list，进行替换
@method_decorator(login_required, name="dispatch")
class PublisherList(View):

    def get(self, request):
        all_pub = models.Publisher.objects.all().order_by("id")
        return render(request, "publisher_list.html", {"all_pub": all_pub})

    def post(self, request):
        print("error")
        return "<h1>error</h1>"


# 新增出版社
def publisher_add(request):
    if request.method == "POST":
        pub_name = request.POST.get("pub_name")
        if not pub_name:
            return render(request, "publisher_add.html", {"error": "出版社名称不能为空"})
        # print(pub_name)
        if models.Publisher.objects.filter(name=pub_name):
            # 数据库有重复出版社
            return render(request, "publisher_add.html", {"error": "出版社名字已存在"})

        ret = models.Publisher.objects.create(name=pub_name)
        print(ret, type(ret))
        return redirect(reverse("publisher"))
    # get请求回一个页面。其中包括一个form表单进行提交
    # POST请求
    # 获取用户输入数据然后将数据提交到数据库中
    # 返回一个重定向到展示界面

    return render(request, "publisher_add.html")


# CBV重构 publisher_add，进行替换
# @method_decorator(timer, name="get")
# @method_decorator(timer, name="post")
@method_decorator(login_required, name="dispatch")
class PublisherAdd(View):

    # @method_decorator(timer)
    # def dispatch(self, request, *args, **kwargs):
    #     # 之前的操作
    #     ret = super().dispatch(request, *args, **kwargs)
    #     # 之后的操作
    #     return ret

    # @method_decorator(timer)
    def get(self, request):
        print("get request")
        return render(request, "publisher_add.html")

    def post(self, request):
        print("post request")
        pub_name = request.POST.get("pub_name")
        if not pub_name:
            return render(request, "publisher_add.html", {"error": "出版社名称不能为空"})
        if models.Publisher.objects.filter(name=pub_name):
            # 数据库有重复出版社
            return render(request, "publisher_add.html", {"error": "出版社名字已存在"})

        models.Publisher.objects.create(name=pub_name)
        return redirect(reverse("publisher"))


# 删除出版社
def publisher_del(request):
    # 获取相对应要删除数据的id
    pk = request.GET.get("pk")
    print(pk)
    # 根据id删除数据库中的记录
    # models.Publisher.objects.get(pk=pk).delete()# 查询到一个对象符合并进行删除
    models.Publisher.objects.filter(pk=pk).delete()  # 查询到一个对象列表符合并进行删除列表中的所有对象
    # 返回重定向到list页面
    return redirect(reverse("publisher"))


# CBV重构 publisher_del，进行替换
@method_decorator(login_required, name="dispatch")
class PublisherDel(View):

    def get(self, request, pk):
        # pk = request.GET.get("pk")
        # print(pk)
        models.Publisher.objects.filter(pk=pk).delete()
        return redirect(reverse("publisher"))


# 修改出版社
def publisher_edit(request):
    # GET请求，返回一个页面包含form表单，input有原始数据
    pk = request.GET.get("pk")
    pub_obj = models.Publisher.objects.get(pk=pk)
    if request.method == "GET":
        return render(request, "publisher_edit.html", {"pub_obj": pub_obj})
    else:
        # 获取用户提交的出版社名称
        edited_pub = request.POST.get("edited_pub")
        if not edited_pub:
            return render(request, "publisher_edit.html", {"error": "出版社名称不能为空"})
        pub_obj.name = edited_pub  # 只在内存中修改了name的属性
        # 需要在数据库中也进行操作
        pub_obj.save()
        return redirect(reverse("publisher"))
    # POST请求，修改对应的数据，返回重定向到list页面


# CBV重构 publisher_edit，进行替换
@method_decorator(login_required, name="dispatch")
class PublisherEdit(View):

    def get(self, request, pk):
        # pk = request.GET.get("pk")
        pub_obj = models.Publisher.objects.get(pk=pk)
        return render(request, "publisher_edit.html", {"pub_obj": pub_obj})

    def post(self, request, pk):
        # pk = request.GET.get("pk")
        pub_obj = models.Publisher.objects.get(pk=pk)
        edited_pub = request.POST.get("edited_pub")
        if not edited_pub:
            return render(request, "publisher_edit.html", {"error": "出版社名称不能为空"})
        pub_obj.name = edited_pub
        pub_obj.save()
        return redirect(reverse("publisher"))


# 图书列表
def book_list(request):
    all_books = models.BOOK.objects.all().order_by("id")
    # for i in all_books:
    #     print(i)
    #     print(i.id, i.name, i.publisher_id, i.publisher)
    # i.publisher拿到的是关联的publish对象，publisher_id 是键值
    # 然后用一个页面返回
    return render(request, "book_list.html", {"all_books": all_books})


# CBV重构 book_list，进行替换
@method_decorator(login_required, name="dispatch")
class BookList(View):

    def get(self, request):
        all_books = models.BOOK.objects.all().order_by("id")
        return render(request, "book_list.html", {"all_books": all_books})


# 增加书籍
def book_add(request):
    error = ""
    if request.method == "POST":
        book_name = request.POST.get("book_name")
        pub_id = request.POST.get("pub_id")
        print(pub_id, type(pub_id))
        if not book_name:
            error = "书籍名称不能为空"
        elif models.BOOK.objects.filter(name=book_name, publisher=pub_id):
            error = "书籍已存在"
        else:
            models.BOOK.objects.create(name=book_name, publisher_id=pub_id)
            return redirect(reverse("book"))

    all_pubs = models.Publisher.objects.all()
    return render(request, "book_add.html", {"all_pubs": all_pubs, "error": error})


# CBV重构 book_add，进行替换
@method_decorator(login_required, name="dispatch")
class BookAdd(View):

    def get(self, request):
        error = ""
        all_pubs = models.Publisher.objects.all()
        return render(request, "book_add.html", {"all_pubs": all_pubs, "error": error})

    def post(self, request):
        error = ""
        book_name = request.POST.get("book_name")
        pub_id = request.POST.get("pub_id")
        if not book_name:
            error = "书籍名称不能为空"
        elif models.BOOK.objects.filter(name=book_name, publisher=pub_id):
            error = "书籍已存在"
        else:
            models.BOOK.objects.create(name=book_name, publisher_id=pub_id)
            return redirect(reverse("book"))
        all_pubs = models.Publisher.objects.all()
        return render(request, "book_add.html", {"all_pubs": all_pubs, "error": error})


# 删除书籍
def book_del(request):
    # 获取相对应要删除数据的id
    pk = request.GET.get("pk")
    print(pk)
    # 根据id删除数据库中的记录
    # models.BOOK.objects.get(pk=pk).delete()# 查询到一个对象符合并进行删除
    models.BOOK.objects.filter(pk=pk).delete()  # 查询到一个对象列表符合并进行删除列表中的所有对象
    # 返回重定向到list页面
    return redirect(reverse("book"))


# CBV重构 book_del，进行替换
@method_decorator(login_required, name="dispatch")
class BookDel(View):

    def get(self, request):
        pk = request.GET.get("pk")
        print(pk)
        models.BOOK.objects.filter(pk=pk).delete()
        return redirect(reverse("book"))

    def post(self, request):
        return redirect(reverse("book"))


# 编辑书籍
def book_edit(request):
    book_id = request.GET.get("pk")
    book_obj = models.BOOK.objects.get(pk=book_id)
    if request.method == "GET":
        all_pubs = models.Publisher.objects.all()
        return render(request, "book_edit.html", {"book_obj": book_obj, "all_pubs": all_pubs})
    else:
        # 获取用户提交的出版社名称
        edited_book = request.POST.get("edited_book")
        edited_id = request.POST.get("pub_id")
        if not edited_book:
            return render(request, "book_edit.html", {"error": "书籍名称不能为空"})
        # 方法一
        # book_obj.name = edited_book  # 只在内存中修改了name的属性
        # book_obj.publisher_id = edited_id
        # # 需要在数据库中也进行操作
        # book_obj.save()
        # 方法二
        models.BOOK.objects.filter(pk=book_id).update(name=edited_book, publisher_id=edited_id)

        return redirect(reverse("book"))


# CBV重构 book_edit，进行替换
@method_decorator(login_required, name="dispatch")
class BookEdit(View):

    def get(self, request, book_id):
        # book_id = request.GET.get("pk")
        book_obj = models.BOOK.objects.get(pk=book_id)
        all_pubs = models.Publisher.objects.all()
        return render(request, "book_edit.html", {"book_obj": book_obj, "all_pubs": all_pubs})

    def post(self, request, book_id):
        # book_id = request.GET.get("pk")
        edited_book = request.POST.get("edited_book")
        edited_id = request.POST.get("pub_id")
        if not edited_book:
            return render(request, "book_edit.html", {"error": "书籍名称不能为空"})
        models.BOOK.objects.filter(pk=book_id).update(name=edited_book, publisher_id=edited_id)
        return redirect(reverse("book"))


# 展示作者信息
def author_list(request):
    # 查询所有作者
    all_authors = models.Author.objects.all()
    # for author in all_authors:
    #     print(author)
    #     print(author.id)
    #     print(author.name)
    #     print(author.books, type(author.books)) 关系管理对象
    # 多对多关系，其中一个作者可能有多个作者，或者一个书有多个作者
    """
        Author object (1)
        1
        鲁迅
        app01.BOOK.None <class 'django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager'>
        <QuerySet [<BOOK: BOOK object (9)>, <BOOK: BOOK object (11)>, <BOOK: BOOK object (13)>]>
        ----------
        Author object (2)
        2
        巴金
        app01.BOOK.None <class 'django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager'>
        <QuerySet [<BOOK: BOOK object (10)>, <BOOK: BOOK object (11)>, <BOOK: BOOK object (12)>]>
        ----------
        Author object (3)
        3
        雨果
        app01.BOOK.None <class 'django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager'>
        <QuerySet [<BOOK: BOOK object (8)>, <BOOK: BOOK object (12)>, <BOOK: BOOK object (13)>]>
        ----------
    """
    # print(author.books.all())  # 所关联的所有对象
    # print("-" * 10)
    # 返回一个界面显示作者
    return render(request, "author_list.html", {"all_authors": all_authors})


# CBV重构 author_list，进行替换
@method_decorator(login_required, name="dispatch")
class AuthorList(View):

    def get(self, request):
        all_authors = models.Author.objects.all()
        return render(request, "author_list.html", {"all_authors": all_authors})


# 添加作者
def author_add(request):
    # post
    if request.method == "POST":
        author_name = request.POST.get("author_name")
        selected_books_id = request.POST.getlist("selected_books_id")
        # print(request.POST)
        # print(author_name)
        # print(selected_books_id, type(selected_books_id))
        # 获取提交数据
        author_obj = models.Author.objects.create(name=author_name)
        author_obj.books.set(selected_books_id)  # 设置多对多关系
        # 提交数据库
        # 返回重定向，展示作者界面
        return redirect(reverse("author"))
    # 返回一个界面，包含form表单让用户输入作者姓名以及选择代表作
    # 查询所有的书籍
    all_books = models.BOOK.objects.all()
    return render(request, "author_add.html", {"all_books": all_books})


# CBV重构 author_add，进行替换
@method_decorator(login_required, name="dispatch")
class AuthorAdd(View):

    def get(self, request):
        all_books = models.BOOK.objects.all()
        return render(request, "author_add.html", {"all_books": all_books})

    def post(self, request):
        author_name = request.POST.get("author_name")
        selected_books_id = request.POST.getlist("selected_books_id")
        author_obj = models.Author.objects.create(name=author_name)
        author_obj.books.set(selected_books_id)  # 设置多对多关系

        return redirect(reverse("author"))


# 删除作者
def author_del(request):
    # 获取返回的对象ID
    author_pk = request.GET.get("id")
    # 根据ID进行删除
    models.Author.objects.filter(pk=author_pk).delete()
    # 会删除作者以及对应的作者所关联的代表作关系删除，并不会删除书籍。
    return redirect(reverse("author"))
    # 返回重定向展示作者页面


# CBV重构 author_del，进行替换
@method_decorator(login_required, name="dispatch")
class AuthorDel(View):

    def get(self, request):
        author_pk = request.GET.get("id")
        models.Author.objects.filter(pk=author_pk).delete()
        return redirect(reverse("author"))

    def post(self, request):
        return redirect(reverse("author"))


# 修改作者信息
def author_edit(request):
    pk = request.GET.get("id")
    author_obj = models.Author.objects.get(pk=pk)
    # post
    if request.method == "POST":
        author_name = request.POST.get("author_name")
        books = request.POST.getlist("selected_books_id")
        author_obj.name = author_name
        author_obj.save()
        author_obj.books.set(books)
        return redirect(reverse("author"))
    # get

    all_books = models.BOOK.objects.all()
    # 获取要编辑的对象的ID，根据ID获取对象的相关信息，如姓名，代表作
    # 返回包含姓名，代表作的页面
    return render(request, "author_edit.html", {"author_obj": author_obj, "all_books": all_books})


# CBV重构 author_edit，进行替换
@method_decorator(login_required, name="dispatch")
class AuthorEdit(View):

    def get(self, request, author_id):
        # pk = request.GET.get("id")
        author_obj = models.Author.objects.get(pk=author_id)
        all_books = models.BOOK.objects.all()
        return render(request, "author_edit.html", {"author_obj": author_obj, "all_books": all_books})

    def post(self, request, author_id):
        # pk = request.GET.get("id")
        author_obj = models.Author.objects.get(pk=author_id)
        author_name = request.POST.get("author_name")
        books = request.POST.getlist("selected_books_id")
        author_obj.name = author_name
        author_obj.save()
        author_obj.books.set(books)
        return redirect(reverse("author"))


# 使用delete将所有的删除操作统一
def delete(request, name, pk):
    print(name, pk)
    # 获取删除的对象，进行删除
    # dic = {"publisher": models.Publisher,
    #        "book": models.BOOK,
    #        "author": models.Author,
    #        }

    if name == "book":
        cls = getattr(models, name.upper())
    else:
        cls = getattr(models, name.lower().capitalize())

    # print(cls)
    cls.objects.filter(pk=pk).delete()
    # 返回重定向
    return redirect(reverse(name))
    # return HttpResponse("ok")


@method_decorator(login_required, name="dispatch")
class Delete(View):
    def get(self, request, name, pk):
        # print(name, pk)
        # 获取删除的对象，进行删除
        # dic = {"publisher": models.Publisher,
        #        "book": models.BOOK,
        #        "author": models.Author,
        #        }

        if name == "book":
            cls = getattr(models, name.upper())
        else:
            cls = getattr(models, name.lower().capitalize())
        if not cls:
            return HttpResponse("检测表名是否存在")

        # print(cls)
        ret = cls.objects.filter(pk=pk)
        if ret:
            ret.delete()
        else:
            return HttpResponse("删除数据不存在")
        # 返回重定向
        return redirect(name)  # 可以直接使用name或者使用reverse（name）
        # return HttpResponse("ok")

    def post(self, request, name):
        return redirect(reverse("publisher"))


def templates_test(request):
    num = 1
    string = "templates_test"
    name_list = ["one", "two", "three"]
    name_set = {"one", "two", "three"}
    dic = {"key1": "value1", "key2": "value2", "key3": "value3"}
    name_tup = ("one", "two", "three")

    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def talk(self):
            return "{}你耗子尾汁".format(self.name)

        def __str__(self):
            return "<Person object {}:{}>".format(self.name, self.age)

    person = Person("lyi", 88)

    return render(request, "templates_test.html", {
        "num": num,
        "string": string,
        "name_list": name_list,
        "name_set": name_set,
        "dic": dic,
        "name_tup": name_tup,
        "Person": person,
        "empty": ""

    })
