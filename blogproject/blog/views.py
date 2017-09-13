from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Post, Category
import markdown
import pygments

from comments.forms import CommentForm


def index(request):
    post_list = Post.objects.all()

    return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'  # 这个name不能瞎取,必须和模板中的变量一样


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    # 相当于对 post.body 多了一个中间步骤,先将 Markdown 格式的文本渲染成 HTML 文本再传递给模板
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list,
    }
    return render(request, 'blog/detail.html',context=context)


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


class ArchivesViews(IndexView):  # 继承IndexView
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'

    def get_queryset(self):
        return super().get_queryset().filter(
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
        )


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # 下面中的category 是post.category
        return super().get_queryset().filter(category=cate)
