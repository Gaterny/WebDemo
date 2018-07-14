利用httpserver模块重写listen()方法,app.listen()只能在单进程模式中使用

```
import tornado.web
import tornado.ioloop
import tornado.httpserver # 新引入httpserver模块

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Tornado!")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    # ------------------------------
    # 我们修改这个部分
    # app.listen(8000)
    http_server = tornado.httpserver.HTTPServer(app) 
    http_server.listen(8000)
    # ------------------------------
    tornado.ioloop.IOLoop.current().start()

```
httpserver模块是Tornado的HTTP服务器实现
我们创建了一个HTTP服务器实例http_server，因为服务器要服务于我们刚刚建立的web应用，将接收到的客户端请求通过web应用中的路由映射表引导到对应的handler中，所以在构建http_server对象的时候需要传出web应用对象app。http_server.listen(8000)将服务器绑定到8000端口。

启动多进程
```
import tornado.web
import tornado.ioloop
import tornado.httpserver 

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Itcast!")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app) 
    # -----------修改----------------
    http_server.bind(8000)    #将服务器绑定到指定端口
    http_server.start(0)
    # ------------------------------
    tornado.ioloop.IOLoop.current().start()
```
http_server.start(num_processes=1)方法指定开启几个进程，参数num_processes默认值为1，即默认仅开启一个进程；如果num_processes为None或者<=0，则自动根据机器硬件的cpu核芯数创建同等数目的子进程；如果num_processes>0，则创建num_processes个子进程。

tornado给我们提供了一次开启多个进程的方法，但是由于：

每个子进程都会从父进程中复制一份IOLoop实例，如过在创建子进程前我们的代码动了IOLoop实例，那么会影响到每一个子进程，势必会干扰到子进程IOLoop的工作；
所有进程是由一个命令一次开启的，也就无法做到在不停服务的情况下更新代码；
所有进程共享同一个端口，想要分别单独监控每一个进程就很困难。
不建议使用这种多进程的方式，而是手动开启多个进程，并且绑定不同的端口。

tornado.options模块：全局参数定义、存储、转换。

tornado.options.define()
用来定义options选项变量的方法，定义的变量可以在全局的tornado.options.options中获取使用，传入参数：

name 选项变量名，须保证全局唯一性，否则会报“Option 'xxx' already defined in ...”的错误；
default　选项变量的默认值，如不传默认为None；
type 选项变量的类型，从命令行或配置文件导入参数的时候tornado会根据这个类型转换输入的值，转换不成功时会报错，可以是str、float、int、datetime、timedelta中的某个，若未设置则根据default的值自动推断，若default也未设置，那么不再进行转换。可以通过利用设置type类型字段来过滤不正确的输入。
multiple 选项变量的值是否可以为多个，布尔类型，默认值为False，如果multiple为True，那么设置选项变量时值与值之间用英文逗号分隔，而选项变量则是一个list列表（若默认值和输入均未设置，则为空列表[]）。
help 选项变量的帮助提示信息，在命令行启动tornado时，通过加入命令行参数 --help　可以查看所有选项变量的信息（注意，代码中需要加入tornado.options.parse_command_line()）。

tornado.options.options
全局的options对象，所有定义的选项变量都会作为该对象的属性。

tornado.options.parse_command_line()
转换命令行参数，并将转换后的值对应的设置到全局options对象相关属性上。追加命令行参数的方式是--myoption=myvalue

新建opt.py，我们用代码来看一下如何使用：
```
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options # 新导入的options模块

tornado.options.define("port", default=8000, type=int, help="run server on the given port.") # 定义服务器监听端口选项
tornado.options.define("Tornado", default=[], type=str, multiple=True, help="Tornado subjects.") # 无意义，演示多值情况

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Itcast!")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    print (tornado.options.options.Tornado) # 输出多值选项
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
    
    #$ python opt.py --port=9000 --Tornado=python,c++,java,php,ios
```
tornado.options.parse_config_file(path)
从配置文件导入option，配置文件中的选项格式如下：
在当前文件夹下新建config文件，并配置config
```
port = 8000
Tornado = ["python", "is", "nice"]
```
修改opt.py文件
```
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options # 新导入的options模块

tornado.options.define("port", default=8000, type=int, help="run server on the given port.") # 定义服务器监听端口选项
tornado.options.define("Tornado", default=[], type=str, multiple=True, help="Tornado subjects.") # 无意义，演示多值情况

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Tornado!")

if __name__ == "__main__":
    tornado.options.parse_config_file("./config") # 仅仅修改了此处
    print tornado.options.options.Tornado # 输出多值选项
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
#python opt.py
```

说明
1. 日志
当我们在代码中调用parse_command_line()或者parse_config_file()的方法时，tornado会默认为我们配置标准logging模块，即默认开启了日志功能，并向标准输出（屏幕）打印日志信息。
如果想关闭tornado默认的日志功能，可以在命令行中添加--logging=none 或者在代码中执行如下操作:
```
from tornado.options import options, parse_command_line
options.logging = None
parse_command_line()
```
2. 配置文件
我们看到在使用prase_config_file()的时候，配置文件的书写格式仍需要按照python的语法要求，其优势是可以直接将配置文件的参数转换设置到全局对象tornado.options.options中；然而，其不方便的地方在于需要在代码中调用tornado.options.define()来定义选项，而且不支持字典类型，故而在实际应用中大都不使用这种方法。

在使用配置文件的时候，通常会新建一个python文件（如config.py），然后在里面直接定义python类型的变量（可以是字典类型）；在需要配置文件参数的地方，将config.py作为模块导入，并使用其中的变量参数。

如config.py文件：
```
# Redis配置
redis_options = {
    'redis_host':'127.0.0.1',
    'redis_port':6379,
    'redis_pass':'',
}

# Tornado app配置
settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    'cookie_secret':'0Q1AKOKTQHqaa+N80XhYW7KCGskOUE2snCW06UIxXgI=',
    'xsrf_cookies':False,
    'login_url':'/login',
    'debug':True,
}

# 日志
log_path = os.path.join(os.path.dirname(__file__), 'logs/log')
```
需要使用时直接导入config模块即可：
```
import tornado.web
import config

if __name__ = "__main__":
    app = tornado.web.Application([], **config.settings)
...
```
