# -*- encoding: utf-8 -*-
# @File    : custom_tag.py
# @Time    : 2020/6/25 1:56
# @Author  : 一叶星羽
# @Email   : h0670131005@gmail.com
# @Software: PyCharm

import re
from random import randint
from django import template
from django.template.defaultfilters import stringfilter
from PerBlogNote import settings

register = template.Library()


@register.simple_tag()
def random_num():
    return randint(1, 10)


@register.filter(is_safe=True)
@stringfilter
def custom_markdown(content):
    code_list = re.findall(r'<pre><code class="lang-(.*)">', content, re.M)
    for code in code_list:
        content = re.sub(r'<pre><code class="(.*)">',
                         '<pre class="language-{code}"><code class="language-{code}">'.format(code=code.lower()), content,
                         1)
    return content


@register.simple_tag(name='settings_value')
def settings_value(name):
    return getattr(settings, name, "站点名称")