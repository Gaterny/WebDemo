from django.db import models

# Create your models here.
class Comment(models.Model):
	"""docstring for Comment"""
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=255)
	url = models.URLField(blank=True)   #允许为空
	text = models.TextField()
	created_time = models.DateTimeField(auto_now_add=True) #自动记录评论时间为当前时间
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
	def __str__(self):
		return self.text[:20]
		