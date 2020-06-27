"""PerBlogNote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings

from apps.blog.views import Index, Friends, Detail, Archive, CategoryList, \
    CategoryView, TagList, TagView, About

urlpatterns = [
    path('admin/', admin.site.urls),

    # 首页
    path('', Index.as_view(), name='index'),

    # 友情链接
    path('friends/', Friends.as_view(), name='friends'),

    # 后台 markdown 编辑器配置
    path('mdeditor/', include('mdeditor.urls')),

    # 文章详情
    re_path(r'article/av(?P<pk>\d+)', Detail.as_view(), name='detail'),

    # 文章归档
    path('article/', Archive.as_view(), name='archive'),

    # 分类统计
    path(r'category/', CategoryList.as_view(), name='category'),

    # 文章分类
    re_path(r'category/cg(?P<pk>\d+)', CategoryView.as_view(), name='article_category'),

    # 标签统计
    path(r'tag/', TagList.as_view(), name='tag'),

    # 文章标签
    re_path(r'tag/tg(?P<pk>\d+)', TagView.as_view(), name='article_tag'),

    # 关于本站
    path('about/', About.as_view(), name='about'),

    # 静态文件
    re_path(r'^medias/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name="media"),
    # re_path(r'^static/(?P<path>.*)',serve, {'document_root': settings.STATIC_ROOT}, name='static')
]

# 设置后台名称
admin.site.site_header = '沐叶博客后台'
admin.site.site_title = '沐叶博客后台'


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns = urlpatterns + \
                  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
