from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import SnsModel

# Create your views here.

def signupfunc(request):
    # 全ユーザのリストを取得
    user_list = User.objects.all()
    print(user_list)
    # 特定のユーザの情報を取得
    user_specified = User.objects.get(username='hogehoge')
    print(user_specified)
    print(user_specified.email)
    if request.method == 'POST':
        # POST['username']はsignup.htmlの<input>タグのnameに対応
        username = request.POST['username']
        password = request.POST['password']
        # try/except文で例外処理
        try:
            # username(key値)がusername(POSTで受け取った値)と一致しているものを抽出
            User.objects.get(username=username)
            # errorというcontextをhtmlに渡す
            return render(request, 'signup.html', {'error':'このユーザは登録されています'})
        except:
            # try文がエラーとなったとき実行される(登録済ユーザ名でない場合実行される)
            # djangoのメソッドを使ってユーザを登録
            User.objects.create_user(username, '', password)
            # print(request.POST)
            return render(request, 'signup.html', {'some': 100})
    # class based viewでのtemplate_nameに対応
    return render(request, 'signup.html', {'some': 100})

def loginfunc(request):
    if request.method == 'POST':
        # POST['username']はsignup.htmlの<input>タグのnameに対応
        username = request.POST['username']
        password = request.POST['password']    
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html', {'some': 100})

def logoutfunc(request):
    logout(request)
    return redirect('login')

# ログインしていればlistfuncを実行|ログインしてなければloginにリダイレクト
@login_required
def listfunc(request):
    object_list = SnsModel.objects.all()
    return render(request, 'list.html', {'object_list':object_list})

def detailfunc(request, pk):
    object = SnsModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
    object = SnsModel.objects.get(pk=pk)
    object.good += 1
    object.save()
    return redirect('list')

def readfunc(request, pk):
    object = SnsModel.objects.get(pk=pk)
    current_user = request.user.get_username()
    if current_user in object.read_user:
        return redirect('list')
    else:
        object.read += 1
        object.read_user = object.read_user + ' ' + current_user
        object.save()
        return redirect('list')

class CreatePost(CreateView):
    template_name = 'create.html'
    model = SnsModel
    fields = ('title', 'content', 'author', 'images')
    success_url = reverse_lazy('list')
