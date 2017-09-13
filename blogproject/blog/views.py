from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from .models import Post, Category
import markdown
import pygments

from comments.forms import CommentForm


# def index(request):
#     post_list = Post.objects.all()
#
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'  # 这个name不能瞎取,必须和模板中的变量一样


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

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
#     context_object_name = 'post'
#
#     def get(self, request, *args,**kwargs):  # 每次请求就会直接调用get方法,所以点击量的写在get方法中比较合适
#         # 复写基类的方法,一定要使用super来调用
#         response = super().get(request, *args,**kwargs)
#         self.object.increase_views()  # objects 实际上是Post的对象
#         return response  # 复写基类的方法,该返回的必须要返回
#
#     def get_object(self, queryset=None):
#         post = super().get_object(queryset)
#         post.body = markdown.markdown(post.body, extensions=[
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',
#             'markdown.extensions.toc'
#         ])
#         return post
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         form = CommentForm()
#         # 下面的self.get_object
#         # 因此self.get_object()必须返回post
#         comment_list = self.object.comment_set.all()
#         context.update({  # context实际上已有post,所以这里使用更新update
#             'form': form,
#             'comment_list': comment_list,
#         })
#         return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()  # self.object实际上是Post的对象
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 把post加到context
        form = CommentForm()
        # 下面的self.object是由self.get_object()得到的
        # 因此self.get_object()必须返回post
        comment_list = self.object.comment_set.all()
        context.update({  # context已有post了，所以这里使用更新update
            'form': form,
            'comment_list': comment_list,
        })
        return context


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
