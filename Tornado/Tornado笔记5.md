模板的使用：

1.静态文件：通过向web.Application类的构造函数传递一个名为static_path的参数来告诉Tornado从文件系统的一个特定位置提供静态文件，如：
```
app = tornado.web.Application(
    [(r'/', IndexHandler)],
    static_path = os.path.join(os.path.dirname(__file__), "statics"),
    )
```
在这里，我们设置了一个当前应用目录下名为statics的子目录作为static_path的参数。现在应用将以读取statics目录下的filename.ext来响应诸如/static/filename.ext的请求，并在响应的主体中返回。

对于静态文件目录的命名，为了便于部署，建议使用static
对于我们提供的静态文件资源，可以通过http://127.0.0.1/static/html/index.html来访问。而且在index.html中引用的静态资源文件，我们给定的路径也符合/static/...的格式，故页面可以正常浏览。
```<link href="/static/plugins/bootstrap/css/bootstrap.min.css" rel="stylesheet">```

StaticFileHandler
我们再看刚刚访问页面时使用的路径http://127.0.0.1/static/html/index.html，这中url显然对用户是不友好的，访问很不方便。我们可以通过tornado.web.StaticFileHandler来自由映射静态文件与其访问路径url。

tornado.web.StaticFileHandler是tornado预置的用来提供静态资源文件的handler。
```
import os

current_path = os.path.dirname(__file__)
app = tornado.web.Application(
    [
        (r'^/()$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html"), "default_filename":"index.html"}),
        (r'^/view/(.*)$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html")}),
    ],
    static_path=os.path.join(current_path, "statics"),
)
```
path 用来指明提供静态文件的根路径，并在此目录中寻找在路由中用正则表达式提取的文件名。
default_filename 用来指定访问路由中未指明文件名时，默认提供的文件。
对于静态文件statics/html/index.html，现在可以通过三种方式进行访问：

http://127.0.0.1/static/html/index.html
http://127.0.0.1/
http://127.0.0.1/view/index.html

2.使用模板：
1. 路径与渲染
使用模板，需要仿照静态文件路径设置一样，向web.Application类的构造函数传递一个名为template_path的参数来告诉Tornado从文件系统的一个特定位置提供模板文件，如：
```
app = tornado.web.Application(
    [(r'/', IndexHandler)],
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
)
```
我们设置了一个当前应用目录下名为templates的子目录作为template_path的参数。在handler中使用的模板将在此目录中寻找。
将静态文件目录statics/html中的index.html复制一份到templates目录中，此时文件目录结构为：
```
.
├── statics
│   ├── css
│   │   ├── index.css
│   │   ├── main.css
│   │   └── reset.css
│   ├── html
│   │   └── index.html
│   ├── images
│   │   ├── home01.jpg
│   │   ├── home02.jpg
│   │   ├── home03.jpg
│   │   └── landlord01.jpg
│   ├── js
│   │   ├── index.js
│   │   └── jquery.min.js
│   └── plugins
│       ├── bootstrap
│       │   └─...
│       └── font-awesome
│           └─...
├── templates
│   └── index.html
└── test.py
```
在handler中使用render()方法来渲染模板并返回给客户端
```
class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html") # 渲染主页模板，并返回给客户端。



current_path = os.path.dirname(__file__)
app = tornado.web.Application(
    [
        (r'^/$', IndexHandler),
        (r'^/view/(.*)$', StaticFileHandler, {"path":os.path.join(current_path, "statics/html")}),
    ],
    static_path=os.path.join(current_path, "statics"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
)
```
与django类似，tornado中也使用{{}}作为变量或者表达式的占位符，使用render渲染后占位符会被替换成相应的结果值
例如，在index.html中添加一条房源信息记录：
```
<li class="house-item">
    <a href=""><img src="/static/images/home01.jpg"></a>
    <div class="house-desc">
        <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
        <div class="house-price">￥<span>398</span>/晚</div>
        <div class="house-intro">
            <span class="house-title">宽窄巷子+160平大空间+文化保护区双地铁</span>
            <em>整套出租 - 5分/6点评 - 北京市丰台区六里桥地铁</em>
        </div>
    </div>
</li>

改为模板：
<li class="house-item">
    <a href=""><img src="/static/images/home01.jpg"></a>
    <div class="house-desc">
        <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
        <div class="house-price">￥<span>{{price}}</span>/晚</div>
        <div class="house-intro">
            <span class="house-title">{{title}}</span>
            <em>整套出租 - {{score}}分/{{comments}}点评 - {{position}}</em>
        </div>
    </div>
</li>
```
渲染方式：
```
class IndexHandler(RequestHandler):
    def get(self):
        house_info = {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        }
        self.render("index.html", **house_info)
```
{{}}中的变量会被替换成house_info的值，当然，{{}}中还可以包含表达式

与django类似，可以在Tornado模板中使用Python条件和循环语句。控制语句以{\%和\%}包围，并以类似下面的形式被使用：
```
{% if ... %} ... {% elif ... %} ... {% else ... %} ... {% end %}
{% for ... in ... %} ... {% end %}
{% while ... %} ... {% end %}
```

尝试修改index.html
```
<ul class="house-list">
    {% if len(houses) > 0 %}
        {% for house in houses %}
        <li class="house-item">
            <a href=""><img src="/static/images/home01.jpg"></a>
            <div class="house-desc">
                <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
                <div class="house-price">￥<span>{{house["price"]}}</span>/晚</div>
                <div class="house-intro">
                    <span class="house-title">{{house["title"]}}</span>
                    <em>整套出租 - {{house["score"]}}分/{{house["comments"]}}点评 - {{house["position"]}}</em>
                </div>
            </div>
        </li>
        {% end %}
    {% else %}
        对不起，暂时没有房源。
    {% end %}
</ul>
```
渲染语句如下：
```
class IndexHandler(RequestHandler):
    def get(self):
        houses = [
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        },
        {
            "price": 398,
            "title": "宽窄巷子+160平大空间+文化保护区双地铁",
            "score": 5,
            "comments": 6,
            "position": "北京市丰台区六里桥地铁"
        }]
        self.render("index.html", houses=houses)
```

static_url()
Tornado模板模块提供了一个叫作static_url的函数来生成静态文件目录下文件的URL。如下面的示例代码：
```<link rel="stylesheet" href="{{ static_url("style.css") }}">```

这个对static_url的调用生成了URL的值，并渲染输出类似下面的代码：
```<link rel="stylesheet" href="/static/style.css?v=ab12">```
优点：

static_url函数创建了一个基于文件内容的hash值，并将其添加到URL末尾（查询字符串的参数v）。这个hash值确保浏览器总是加载一个文件的最新版而不是之前的缓存版本。无论是在你应用的开发阶段，还是在部署到生产环境使用时，都非常有用，因为你的用户不必再为了看到你的静态内容而清除浏览器缓存了。
另一个好处是你可以改变你应用URL的结构，而不需要改变模板中的代码。例如，可以通过设置static_url_prefix来更改Tornado的默认静态路径前缀/static。如果使用static_url而不是硬编码的话，代码不需要改变。

转义
我们新建一个表单页面new.html:
```
<!DOCTYPE html>
<html>
    <head>
        <title>新建房源</title>
    </head>
    <body>
        <form method="post">
            <textarea name="text"></textarea>
            <input type="submit" value="提交">
        </form>
        {{text}}
    </body>
</html>
```
表单是post请求，对应的handler为：
```
class NewHandler(RequestHandler):

    def get(self):
        self.render("new.html", text="")

    def post(self):
        text = self.get_argument("text", "") 
        print text
        self.render("new.html", text=text)
```
tornado中默认开启了模板自动转义功能，防止网站受到恶意攻击。
我们可以通过raw语句来输出不被转义的原始格式，如：

```{% raw text %}```
注意：在Firefox浏览器中会直接弹出alert窗口，而在Chrome浏览器中，需要set_header("X-XSS-Protection", 0)

若要关闭自动转义，一种方法是在Application构造函数中传递autoescape=None，另一种方法是在每页模板中修改自动转义行为，添加如下语句：

```{% autoescape None %}```

escape()

关闭自动转义后，可以使用escape()函数来对特定变量进行转义，如：

```{{ escape(text) }}```

我们可以使用块来复用模板，块语法如下：
```
{% block block_name %} {% end %}
```
对模板index.html进行抽象，抽离出父母版base.html:
```
<!DOCTYPE html>
<html>
<head> 
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    {% block page_title %}{% end %}
    <link href="{{static_url('plugins/bootstrap/css/bootstrap.min.css')}}" rel="stylesheet">
    <link href="{{static_url('plugins/font-awesome/css/font-awesome.min.css')}}" rel="stylesheet">
    <link href="{{static_url('css/reset.css')}}" rel="stylesheet">
    <link href="{{static_url('css/main.css')}}" rel="stylesheet">
    {% block css_files %}{% end %}
</head>
<body>
    <div class="container">
        <div class="top-bar">
            {% block header %}{% end %}
        </div>
        {% block body %}{% end %}
        <div class="footer">
            {% block footer %}{% end %}
        </div>
    </div>

    <script src="{{static_url('js/jquery.min.js')}}"></script>
    <script src="{{static_url('plugins/bootstrap/js/bootstrap.min.js')}}"></script>
    {% block js_files %}{% end %}
</body>
</html>
```
在子模板index.html中使用extends来使用base.html
```
{% extends "base.html" %}

{% block page_title %}
    <title>爱家-房源</title>
{% end %}

{% block css_files %}
    <link href="{{static_url('css/index.css')}}" rel="stylesheet">
{% end %} 

{% block js_files %}
    <script src="{{static_url('js/index.js')}}"></script>
{% end %}

{% block header %}
    <div class="nav-bar">
        <h3 class="page-title">房 源</h3>
    </div>
{% end %}

{% block body %}
    <ul class="house-list">
    {% if len(houses) > 0 %}
        {% for house in houses %}
        <li class="house-item">
            <a href=""><img src="/static/images/home01.jpg"></a>
            <div class="house-desc">
                <div class="landlord-pic"><img src="/static/images/landlord01.jpg"></div>
                <div class="house-price">￥<span>{{house["price"]}}</span>/晚</div>
                <div class="house-intro">
                    <span class="house-title">{{title_join(house["titles"])}}</span>
                    <em>整套出租 - {{house["score"]}}分/{{house["comments"]}}点评 - {{house["position"]}}</em>
                </div>
            </div>
        </li>
        {% end %}
    {% else %}
        对不起，暂时没有房源。
    {% end %}
    </ul>
{% end %}

{% block footer %}
    <p><span><i class="fa fa-copyright"></i></span>爱家租房&nbsp;&nbsp;享受家的温馨</p>
{% end %}

```
