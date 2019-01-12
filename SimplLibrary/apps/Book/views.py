from django.shortcuts import render,redirect
from django.views import View
from .models import Book
from .froms import BookFrom
# Create your views here.


class IndexView(View):
    """首页"""
    def get(self,request):
        all_book = Book.objects.all()
        return render(request, 'index.html',{
            'all_book': all_book,
        })


class AddBookView(View):
    """添加图书"""
    def get(self,request):
        previous_html = request.GET.get('from', '')
        return render(request, 'add_book.html',{
            'previous_html': previous_html,#上一个页面url
        })

    def post(self, request):
        book_from = BookFrom(request.POST)#表单
        if book_from.is_valid():
            add_book = book_from.save(commit=True)
            return redirect('index')
        else:
            return render(request, 'add_book.html', {
                'book_from': book_from
            })


class DeleteBookView(View):
    """删除图书"""
    def get(self,request):
        book_id = int(request.GET.get('book_id', 0))
        Book.objects.filter(id=book_id).delete() #筛选用户点击的图书，进行删除。注：不能使用Book.objects.get方法

        return redirect('index')


class ModificationBookView(View):
    """修改图书"""
    def get(self,request):
        book_id = int(request.GET.get('book_id', 0)) #传递给modification_book的form表单
        book_detail = Book.objects.filter(id=book_id)[0]

        return render(request, 'modification_book.html',{
            'book_detail': book_detail,#传递给modification_book的form表单
        })

    def post(self,request):
        #获取到用户要修改的图书的信息
        id = int(request.POST.get('id', 0))#获取到用户点击进来的id

        #获取用户输入（修改）
        book = Book.objects.get(id=id)#获取到刚刚的图书对象
        name = request.POST.get('name', '')
        price = int(request.POST.get('price', 0))
        author = request.POST.get('author', '')
        publish = request.POST.get('publish', '')

        #进行修改
        book.name = name
        book.price = price
        book.author = author
        book.publish = publish
        book.save()

        return redirect('index')
