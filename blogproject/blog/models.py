from django.db import models
from django.contrib.auth.models import User   #django内置的专门用来处理网站用户的注册、登录等流程，User是和其他类一样，只不过是Django写好的用户模型
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.

#分类功能,实际是创建category数据库表,name是列名
class Category(models.Model):
	"""docstring for Category"""
	name = models.CharField(max_length=100)  #存储较短的字符使用CharField
	def __str__(self):
		return self.name

#标签
class Tag(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

#文章
class Post(models.Model):
	title = models.CharField(max_length=100)  #文章标题

	body = models.TextField()  #文章正文,使用TextField

	#创建和最后修改时间
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()

	#摘要,指定blank之后,参数可以为空
	excerpt = models.CharField(max_length=250, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE) #一对多的关联关系
	tags = models.ManyToManyField(Tag, blank=True) #多对多的关系,文章可以没有标签

	author = models.ForeignKey(User, on_delete=models.CASCADE)  #一对多的关系,一篇文章只有一个作者,一个作者可以有很多文章.
	views = models.PositiveIntegerField(default=0)

	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		if not self.excerpt:
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
			])
			# 先将 Markdown 文本渲染成 HTML 文本
			# strip_tags 去掉 HTML 文本的全部 HTML 标签
			# 从文本摘取前 54 个字符赋给 excerpt
			self.excerpt = strip_tags(md.convert(self.body))[:50]

		# 调用父类的 save 方法将数据保存到数据库中
		super(Post, self).save(*args, **kwargs)


	class Meta:
		ordering = ['-created_time', 'title']
