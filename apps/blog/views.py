import random
import datetime
import mistune
from operator import itemgetter
from django.shortcuts import render
from django.views.generic.base import View
from django.conf import settings
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Links, Article, Category, Tag


def global_setting(request):
    """
    将settings里面的变量 注册为全局变量
    """
    active_categories = Category.objects.filter(active=True).order_by('index')
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESCRIPTION,
        'SITE_KEY': settings.SECRET_KEY,
        'SITE_MAIL': settings.SITE_MAIL,
        'SITE_ICP': settings.SITE_ICP,
        'SITE_ICP_URL': settings.SITE_ICP_URL,
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_TYPE_CHINESE': settings.SITE_TYPE_CHINESE,
        'SITE_TYPE_ENGLISH': settings.SITE_TYPE_ENGLISH,
        'active_categories': active_categories
    }


class Index(View):
    """
    首页展示
    """
    def get(self, request):
        all_articles = Article.objects.all().order_by('-add_time')
        top_articles = Article.objects.filter(is_recommend=1)
        # 首页分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 9, request=request)
        articles = p.page(page)

        result = {
            'all_articles': articles,
            'top_articles': top_articles,
        }
        result.update(global_setting(result))

        return render(request, 'index.html', result)


class Friends(View):
    """
    友链链接展示
    """
    def get(self, request):
        links = Links.objects.all()
        card_num = random.randint(1, 10)

        result = {
            'links': links,
            'card_num': card_num,
        }
        result.update(global_setting(result))
        return render(request, 'friends.html', result)


class Detail(View):
    """
    文章详情页
    """
    def get(self, request, pk):
        article = Article.objects.get(id=int(pk))
        article.viewed()
        mk = mistune.Markdown()
        output = mk(article.content)

        result = {
            'article': article,
            'detail_html': output,
        }
        result.update(global_setting(result))

        return render(request, 'detail.html', result)


class Archive(View):
    """
    文章归档
    """
    def get(self, request):
        all_articles = Article.objects.all().order_by('-add_time')
        all_date = all_articles.values('add_time')
        latest_date = all_date[0]['add_time']
        all_date_list = []
        for i in all_date:
            all_date_list.append(i['add_time'].strftime("%Y-%m-%d"))

        # 遍历1年的日期
        end = datetime.date(latest_date.year, latest_date.month, latest_date.day)
        begin = datetime.date(latest_date.year-1, latest_date.month, latest_date.day)
        d = begin
        date_list = []
        temp_list = []

        delta = datetime.timedelta(days=1)
        while d <= end:
            day = d.strftime("%Y-%m-%d")
            if day in all_date_list:
                temp_list.append(day)
                temp_list.append(all_date_list.count(day))
            else:
                temp_list.append(day)
                temp_list.append(0)
            d += delta
            date_list.append(temp_list)
            temp_list = []

        # 文章归档分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 10, request=request)
        articles = p.page(page)

        result = {
            'all_articles': articles,
            'date_list': date_list,
            'end': str(end),
            'begin': str(begin),
        }
        result.update(global_setting(result))

        return render(request, 'archive.html', result)


class CategoryList(View):
    def get(self, request):
        categories = Category.objects.all()

        result = {
            'categories': categories,
        }
        result.update(global_setting(result))

        return render(request, 'category.html', result)


class CategoryView(View):
    def get(self, request, pk):
        active_categories = Category.objects.all().order_by("index")
        categories = Category.objects.all()
        articles = Category.objects.get(id=int(pk)).article_set.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(articles, 9, request=request)
        articles = p.page(page)

        result = {
            'categories': categories,
            'pk': int(pk),
            'articles': articles
        }
        result.update(global_setting(result))

        return render(request, 'article_category.html', result)


class TagList(View):
    def get(self, request):
        tags = Tag.objects.all()

        result = {
            'tags': tags,
        }
        result.update(global_setting(result))
        return render(request, 'tag.html', result)


class TagView(View):
    def get(self, request, pk):
        tags = Tag.objects.all()
        articles = Tag.objects.get(id=int(pk)).article_set.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(articles, 9, request=request)
        articles = p.page(page)

        result = {
            'tags': tags,
            'pk': int(pk),
            'articles': articles,
        }
        result.update(global_setting(result))
        return render(request, 'article_tag.html', result)


class About(View):
    def get(self, request):
        articles = Article.objects.all().order_by('-add_time')
        categories = Category.objects.all()
        tags = Tag.objects.all()

        all_date = articles.values('add_time')

        latest_date = all_date[0]['add_time']
        end_year = latest_date.strftime("%Y")
        end_month = latest_date.strftime("%m")
        date_list = []
        for i in range(int(end_month), 13):
            date = str(int(end_year)-1)+'-'+str(i)
            date_list.append(date)

        for j in range(1, int(end_month)+1):
            date = end_year + '-' + str(j)
            date_list.append(date)

        value_list = []
        all_date_list = []
        for i in all_date:
            all_date_list.append(i['add_time'].strftime("%Y-%m"))

        for i in date_list:
            value_list.append(all_date_list.count(i))

        temp_list = []  # 临时集合
        tags_list = []  # 存放每个标签对应的文章数
        tags = Tag.objects.all()
        for tag in tags:
            temp_list.append(tag.name)
            temp_list.append(len(tag.article_set.all()))
            tags_list.append(temp_list)
            temp_list = []

        tags_list.sort(key=lambda x: x[1], reverse=True)  # 根据文章数排序

        top10_tags = []
        top10_tags_values = []
        for i in tags_list[:10]:
            top10_tags.append(i[0])
            top10_tags_values.append(i[1])

        result = {
            'articles': articles,
            'categories': categories,
            'tags': tags,
            'date_list': date_list,
            'value_list': value_list,
            'top10_tags': top10_tags,
            'top10_tags_values': top10_tags_values
        }
        result.update(global_setting(result))

        return render(request, 'about.html', result)