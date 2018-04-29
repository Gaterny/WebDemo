from . import views
from django.urls import path

app_name = 'blog'
urlpatterns = [
	path('post/<int:pk>/', views.detail, name='detail'),
	path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
	path('category/<int:pk>/', views.category, name='category'),
	path('', views.IndexView.as_view(), name='index'),
]
#path的参数中,一为路由地址,二为处理函数,三为处理函数名
#需要将类视图通过as_view方法转换成函数视图