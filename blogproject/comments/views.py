from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from .forms import CommentForm
from blog.models import Post
# redirect作用是重定向，可以接收一个url作为参数，也可以接收一个模型的实例作为参数
# 如果接收模型实例，该实例必须返回url，根据返回的url值进行重定向

def post_comment(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)
 
	if request.method == 'POST':           #只要当用户请求为POST时才处理表单
		form = CommentForm(request.POST)

		if form.is_valid():   #is_valid方法自动检查表单的数据是否符合请求
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect(post)     #重定向到post的详情页
		else:
			comment_list = post.comment_set.all()   #获取文章下的全部评论
			context = {'post': post,
			'form': form,
			'comment_list': comment_list}
			return render(request, 'blog.detail.html', context=context)

	return redirect(post)