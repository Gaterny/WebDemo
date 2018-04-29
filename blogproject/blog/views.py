import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from comments.forms import CommentForm
from .models import Post, Category
from django.views.generic import ListView
# Create your views here.

# def index(request):
# 	post_list = Post.objects.all().order_by('-created_time')  #-表示逆序,不加是正序
# 	return render(request, 'blog/index.html', context={
# 		'post_list': post_list
# 		})

class IndexView(ListView):
	'''ListView类视图'''
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)

	post.increase_views()
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
	return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
	post_list = Post.objects.filter(created_time_year=year, created_time_month=month).order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate).order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list':post_list})



#request实际上是HttpRequest的一个实例,request就是django为我们封装好的http请求
#在接收http请求之后,返回一个http响应给用户

#在模板的index.html,其中title和welcome的值会根据我们传递的变量来替换,最终模板中显示的是我们传递的值
#render的三个参数,一是传入的http请求,二是模板文件的位置,找到该文件读取模板中的内容
#之后render根据我们传入的context值将模板中的变量替换为我们传递的变量.