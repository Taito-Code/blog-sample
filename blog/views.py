from django.views.generic import TemplateView
from .models import Article, Ine, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.http.response import JsonResponse
import json 
import urllib.request
from .forms import ArticleForm

#index表示
class index(TemplateView):
    template_name = "blog/index.html" 

#新規作成
def new(request):
    template_name = "blog/new.html"
    if request.method == "POST":
        form = ArticleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(article_all)

    else:
        form = ArticleForm
    return render(request, template_name, {'form': form })

#記事一覧
def article_all(request):
    template_name = "blog/article_all.html"
    context = {"articles":Article.objects.all()}
    return render(request, template_name, context)

#記事を閲覧
def view_article(request, pk):
    template_name = "blog/view_article.html"
    try:
        article = Article.objects.get(pk=pk)
        post = get_object_or_404(Article, pk=pk)
        ine = Ine.objects.filter(parent=post).count()

    except Article.DoesNotExist:
        raise Http404
    
    if request.method == "POST":
        # データベースに投稿されたコメントを保存
        Comment.objects.create(text=request.POST["text"], article=article) 
    context = {"article":article, "ine":ine}
    return render(request, template_name, context)

#編集ページ
def edit(request,pk):
    template_name = "blog/edit.html"
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        raise Http404
    if request.method == "POST":
        article.title = request.POST["title"]
        article.text = request.POST["text"]
        article.save()
        return redirect(view_article, pk)
    context = {"article": article}
    return render(request, template_name, context)

#記事削除
def delete(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        raise Http404
    article.delete()
    return redirect(article_all)

#いいね関数
def add_ine(request, pk):
    
    post = get_object_or_404(Article, pk=pk) #Articleの受け取り
    ip_address = get_client_ip(request) #IPアドレスをget_client_ip()で取得
    ips = [ine.ip_address for ine in Ine.objects.filter(parent=post).all()]

    #IPアドレスが未登録の場合はDBに登録
    if ip_address in ips:
        msg = '登録済みです'
    else:
        ine = Ine.objects.create(ip_address=ip_address, parent=post)
        ine.save()
        msg = '登録しました'

    #Json形式にして格納
    d = {
        'count': Ine.objects.filter(parent=post).count(),
        'msg': msg,
    }
    return JsonResponse(d)

#IPアドレスを取得
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
