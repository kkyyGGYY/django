from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from .models import Post, Category, Tag
import markdown
import pygments
from comments.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import PostForm
# def index(request):
#     post_list = Post.objects.all()
#
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'  # 这个post_list不能瞎取,必须和模板中的变量一样
    paginate_by = 2

    def paginator_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        # 首页
        first = False

        # 省略号
        left_has_more = False

        # 当前页左边的几个页码
        left = []

        # 当前页的页码
        page_number = page.number

        # 当前页右边的几个页码
        right = []

        # 省略号
        right_has_more = False

        # 最后一页
        last = False

        # 总页数
        total_pages = paginator.num_pages

        # 获取整个分页页码
        page_range = paginator.page_range

        #如果当前是第一页
        if page_number == 1:
            right = page_range[page_number:page_number+2]
            if right[-1] < total_pages-1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:  # 如果当前是最后一页

            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number-3) if (page_number-3) > 0 else 0:page_number-1]
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number-3) if (page_number-3) > 0 else 0:page_number-1]
            right = page_range[page_number:page_number + 2]
            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left':left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.paginator_data(paginator, page, is_paginated)

        context.update(pagination_data)
        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context



# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.increase_views()
#     # 相当于对 post.body 多了一个中间步骤,先将 Markdown 格式的文本渲染成 HTML 文本再传递给模板
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {
#         'post': post,
#         'form': form,
#         'comment_list': comment_list,
#     }
#     return render(request, 'blog/detail.html',context=context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args,**kwargs):  # 每次请求就会直接调用get方法,所以点击量的写在get方法中比较合适
        # 复写基类的方法,一定要使用super来调用
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()  # objects 实际上是Post的对象
        print('-------------end-------------')
        return response  # 复写基类的方法,该返回的必须要返回


    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        # 下面的self.get_object
        # 因此self.get_object()必须返回post
        comment_list = self.object.comment_set.all()
        context.update({  # context实际上已有post,所以这里使用更新update
            'form': form,
            'comment_list': comment_list,
        })
        return context

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
#     context_object_name = 'post'
#
#     def get(self, request, *args, **kwargs):
#         response = super().get(request, *args, **kwargs)
#         self.object.increase_views()  # self.object实际上是Post的对象
#         return response
#
#     def get_object(self, queryset=None):
#         post = super().get_object(queryset)
#         post.body = markdown.markdown(post.body, extensions=[
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',
#             'markdown.extensions.toc',
#         ])
#         return post
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)  # 把post加到context
#         form = CommentForm()
#         # 下面的self.object是由self.get_object()得到的
#         # 因此self.get_object()必须返回post
#         comment_list = self.object.comment_set.all()
#         context.update({  # context已有post了，所以这里使用更新update
#             'form': form,
#             'comment_list': comment_list,
#         })
#         return context


# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month)
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class ArchivesViews(IndexView):  # 继承IndexView
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'

    def get_queryset(self):
        return super().get_queryset().filter(
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
        )


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # 下面中的category 是post.category
        return super().get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)


class AuthView(IndexView):
    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(author=user)


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q :
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', context={'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
    return render(request, 'blog/index.html', context={'post_list': post_list})

def pushhtml(request):
    return render(request, 'blog/push.html')


# def post_comment(request, post_pk):
#     # 获得要评论的文章
#     post = get_object_or_404(Post, pk=post_pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)  # 实例化表单对象
#         if form.is_valid():
#             comment = form.save(commit=False)  # 由表单对象得到模型对象
#             comment.post = post
#             comment.save()
#             # 可以直接重定向到Post模型对象当中,因为我们指定了get_absolute_url
#             return redirect(post)
#         else:
#             # 获取文章已有的评论
#             # 看不到的属性comment_set
#             comment_list = post.comment_set.all()
#             conetext = {
#                 'post': post,
#                 'form': form,
#                 'comment_list': comment_list,
#             }
#             return render(request, 'blog/detail.html', conetext=conetext)
#     return redirect(post)

from datetime import datetime


def push(request):

    if request.method == 'POST':

        post1 = request.POST
        author_id = post1.get('user')
        print('====================',author_id,'=====================')
        created_time = datetime.now()
        modified_time = datetime.now()

        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = author_id
            # post.author = author
            post.created_time = created_time
            post.modified_time = modified_time
            form.save_m2m()
            post.save()
            return redirect('/')

    else:
        form = PostForm()
    return render(request, 'blog/push.html', context={'form': form})

