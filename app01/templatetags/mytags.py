from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def add_arg(value, arg):  # 参数最多两个，一个是变量，一个是过滤器需要使用的参数
    # template中的引用方式为{{xx|add_arg:xxx}}
    return "{}_{}".format(value, arg)


@register.simple_tag
def pagination(num):
    # template中的引用为{%%}
    li_list = ['<li><a href="#">{}</a></li>'.format(i) for i in range(1, num + 1)]
    print(li_list)
    return mark_safe('''
    <nav aria-label="Page navigation">
  <ul class="pagination">
    <li>
      <a href="#" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
    {}
    <li>
      <a href="#" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  </ul>
</nav>
'''.format("".join(li_list)))


@register.inclusion_tag("page.html")
def pages(num):
    return {"num": range(1, num + 1)}
