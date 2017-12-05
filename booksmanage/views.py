from django.shortcuts import render,HttpResponse,redirect

from . import models
# Book,Publisher,Author,Category
import json,time
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
from django.db.models import F,Q
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.forms import ModelForm
from django.forms import Field

class AddBookForm(ModelForm):
    class Meta:
        model = models.Book
        fields=['title','price','pub_date','publish','catego','auth']


# Create your views here.
def authentication(func):
    def wrapper(request,*args,**kwargs):
        next_path=request.path
        # print('next>>>>>>>>>',next_path)
        if request.user.is_authenticated():

            backresponse = func(request, *args, **kwargs)
            return backresponse
        else:
            return redirect('/login/?next=%s' %next_path)
    return wrapper

@authentication
def index(request):

    book_all=models.Book.objects.all().order_by()
    books=Paginator(book_all,5,orphans=1)
    try:
        page=request.GET.get('page',1)
        book_list=books.page(int(page))
    except EmptyPage:
        book_list = books.page(books.num_pages)
    except PageNotAnInteger:
        book_list = books.page(1)
    dic={"book_all":book_all,"books":books,"page":page,"book_list":book_list}
    return render(request,'booksmanage/InfoManageSystem.html',dic)

@authentication
def addbook(request):
    '''添加书籍'''
    book_list = models.Book.objects.all()
    category_list=models.Category.objects.all()
    author_list = models.Author.objects.all()
    publisher_list = models.Publisher.objects.all()
    if request.method=='POST':
        addform = AddBookForm(data=request.POST)
        print(request.POST)
        if addform.is_valid():
            addform.save()
            return HttpResponse('ok')
        else:
            return render(request, 'booksmanage/addbook.html',
                          {'addform': addform})
        # title=request.POST.get('title')
        # price=request.POST.get('price')
        # auth=request.POST.getlist('author')
        # catego=request.POST.getlist('category')
        # publish=request.POST.get('publisher')
        # pub_date=request.POST.get('pub_date')
        # print(request.POST)
        # b=models.Book(title=title,price=price,publish_id=publish,pub_date=pub_date)
        # b.save()
        # for i in auth:
        #     auth_obj=models.Author.objects.get(id=int(i))
        #     b.auth.add(auth_obj)
        # for i in catego:
        #     catego_obj=models.Category.objects.get(id=int(i))
        #     b.catego.add(catego_obj)
        # return HttpResponse(json.dumps("添加成功"))
        # return redirect('/index')
    elif request.method=='GET':
        addform = AddBookForm()
        return render(request, 'booksmanage/addbook.html',
                      {'addform':addform})

@authentication
def editrecords(request):
    '''编辑书籍'''
    # edit_book = Book.objects.get(id=int(id))
    if request.method=='GET':
        id=request.GET.get('id')
        edit_book = models.Book.objects.get(id=int(id))
        dic = {'author': {"edit_author":[],"unedit_author":[]},
               'publisher': {"edit_pub":"","unedit_pub":[]},
               'category':{"edit_cate":[],"unedit_cate":[]}
               }
        edit_pub=models.Publisher.objects.filter(book__id=edit_book.id).first()
        dic['publisher']['edit_pub']=(edit_pub.id,edit_pub.name)
        unedit_pub=models.Publisher.objects.exclude(book__id=edit_book.id)
        for i in unedit_pub:
            dic['publisher']['unedit_pub'].append((i.id,i.name))
        edit_author=models.Author.objects.filter(book__id=edit_book.id)
        for i in edit_author:
            dic['author']['edit_author'].append((i.id, i.name))
        unedit_author=models.Author.objects.exclude(book__id=edit_book.id)
        for i in unedit_author:
            dic['author']['unedit_author'].append((i.id, i.name))
        edit_cate = models.Category.objects.filter(book__id=edit_book.id)
        for i in edit_cate:
            dic['category']['edit_cate'].append((i.id, i.name))
        unedit_cate = models.Category.objects.exclude(book__id=edit_book.id)
        for i in unedit_cate:
            dic['category']['unedit_cate'].append((i.id, i.name))
        return HttpResponse(json.dumps(dic))
    elif request.method=='POST':
        print(request.POST)
        id=request.POST.get('id')
        title = request.POST.get('title')
        price = request.POST.get('price')
        auth = request.POST.getlist('author')
        catego = request.POST.getlist('category')
        publish_id = request.POST.get('publisher')
        pub_date = request.POST.get('pub_date')
        updatebook_set=models.Book.objects.filter(id=int(id))
        updatebook_set.update(title=title,price=price,publish_id=publish_id,pub_date=pub_date)
        update_book=updatebook_set.first()
        update_book.auth.clear()
        update_book.catego.clear()
        for i in auth:
            auth_obj=models.Author.objects.get(id=int(i))
            update_book.auth.add(auth_obj)
        for i in catego:
            catego_obj=models.Category.objects.get(id=int(i))
            update_book.catego.add(catego_obj)
        return  HttpResponse(json.dumps('编辑成功'))
    else:
        return HttpResponse(json.dumps('error'))

@authentication
def editauthor(request):
    if request.method=='POST':
        name=request.POST.get('name')
        id=request.POST.get('id')
        models.Author.objects.filter(id=id).update(name=name)
        return HttpResponse(json.dumps('编辑成功'))

@authentication
def editpublisher(request):
    if request.method=='POST':
        name=request.POST.get('name')
        city=request.POST.get('city')
        id=request.POST.get('id')
        models.Publisher.objects.filter(id=id).update(name=name,city=city)
        return HttpResponse(json.dumps('编辑成功'))

@authentication
def delrecords(request):
    id=request.POST.get('id')
    book_obj=models.Book.objects.get(id=int(id))
    book_obj.auth.clear()
    book_obj.catego.clear()
    book_obj.delete()
    return HttpResponse('ok')

@authentication
def addpublisher(request):
    if request.method=='POST':
        name = request.POST.get('name')
        city = request.POST.get('city')
        if name:
            models.Publisher.objects.create(name=name,city=city)
            return HttpResponse(json.dumps('成功添加出版社%s' %name))

@authentication
def addauthor(request):
    if request.method=='POST':
        name=request.POST.get('name')
        print("NAME>>>>>>>>>>>>>>>>>>>>>",name)
        if name:
            models.Author.objects.create(name=name)
        return HttpResponse(json.dumps('成功添加作者%s' %name))

def logininterface(request):
    nextpath=request.GET.get('next')
    backhttp = render(request, 'booksmanage/logininterface.html')
    if nextpath:
        backhttp=render(request,'booksmanage/logininterface.html',{'nextpath':nextpath})
    if request.method=='POST':
        user=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=user,password=password)  #验证输入的密码和用户和数据库中的是否匹配
        print(user)
        if user:
            auth.login(request,user)     #设置cookie和session
            print(nextpath)
            if nextpath:
                backhttp = redirect(nextpath)
            else:
                backhttp = redirect('/index/')
        else:
            # 密码或者用户输入错误
            message='密码或者用户名输入错误'
            backhttp=render(request,'booksmanage/logininterface.html',{'nextpath':nextpath,'message':message})
    return backhttp

def register(request):
    ret=render(request,'booksmanage/signup.html')
    if request.method=='POST':
        message=''
        username=request.POST.get('username')
        password=request.POST.get('password')
        if  username and  password:

            if User.objects.filter(username=username).exists():
                print("---------------------------")
                print("用户已存在")
                message='用户已存在'
                ret = render(request, 'booksmanage/signup.html',{'message':message})
            else:
                print(">>>>>>>>>>创建用户成功<<<<<<<<<<")
                user = User.objects.create_user(username = username, password = password)
                user.save()
                ret=redirect('/login/')

    return ret
@authentication
def changepassword(request):
    user=request.user
    state=''
    if request.method=='POST':
        raw_password=request.POST.get('raw-password',None)
        new_password=request.POST.get('new-password',None)
        rep_password=request.POST.get('re-password',None)
        if user.check_password(raw_password):
            if not new_password:
                state='密码为空'
            elif new_password != rep_password:
                state="密码不一致"
            else:
                user.set_password(new_password)
                user.save()
                state='修改成功'
                # return  redirect('/login/')
        else:
            state='原始密码输入错误'
    dic={'state':state}
    return  render(request,'booksmanage/changepassword.html',dic)

def logout_view(request):
    logout(request)
    return redirect('/login/')

@authentication
def searchbook(request):
    booktitle=request.GET.get('mysearch')
    book_obj=Book.objects.filter(title__contains=booktitle).order_by('id')
    books=Paginator(book_obj,per_page=5,orphans=1)
    try:
        page=request.GET.get('page',1)
        book_list=books.page(page)
    except InvalidPage:
        book_list = books.page(1)
    dic={'book_list':book_list,'page':page,'books':books}
    return render(request,'booksmanage/InfoManageSystem.html',dic)

    return redirect('/')
@authentication
def publisherindex(request):
    publisherall=models.Publisher.objects.all().order_by('id')
    P_pubisher=Paginator(publisherall,per_page=5,orphans=1)
    page=request.GET.get('page')
    try:
        publisher_page = P_pubisher.page(page)
    except InvalidPage:
        publisher_page = P_pubisher.page(1)
    dic={'publisher_page':publisher_page,'page':page,'P_pubisher':P_pubisher}
    return render(request,'booksmanage/publisherinterface.html',dic)
@authentication
def authorindex(request):
    authorall=models.Author.objects.all().order_by('id')
    P_author=Paginator(authorall,per_page=5,orphans=1)
    page=request.GET.get('page')
    try:
        author_page = P_author.page(page)
    except InvalidPage:
        author_page = P_author.page(1)
    dic={'author_page':author_page,'page':page,'P_author':P_author}
    return render(request,'booksmanage/authorinterface.html',dic)
@authentication
def delpublisher(request):
    if request.method=='POST':

        id=request.POST.get('id')
        print("PUBLISHER id",id)
        publish_obj=models.Publisher.objects.get(id=id)
        publish_obj.delete()
    return HttpResponse(json.dumps('删除成功'))
@authentication
def delauthor(request):
    if request.method=='POST':

        id=request.POST.get('id')
        print("author id",id)
        publish_obj=models.Author.objects.get(id=id)
        publish_obj.delete()
    return HttpResponse(json.dumps('删除成功'))


