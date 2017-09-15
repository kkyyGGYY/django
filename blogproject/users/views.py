from django.shortcuts import render, redirect
from .forms import RegisterForm
# Create your views here.


# 带表单的视图函数
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})