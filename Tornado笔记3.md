
Application settings:
参数debug：
debug，设置tornado是否工作在调试模式，默认为False即工作在生产模式。当设置debug=True 后，tornado会工作在调试/开发模式，在此种模式下，tornado为方便我们开发而提供了几种特性：

自动重启，tornado应用会监控我们的源代码文件，当有改动保存后便会重启程序，这可以减少我们手动重启程序的次数。需要注意的是，一旦我们保存的更改有错误，自动重启会导致程序报错而退出，从而需要我们保存修正错误后手动启动程序。这一特性也可单独通过autoreload=True设置；
取消缓存编译的模板，可以单独通过compiled_template_cache=False来设置；
取消缓存静态文件hash值，可以单独通过static_hash_cache=False来设置；
提供追踪信息，当RequestHandler或者其子类抛出一个异常而未被捕获后，会生成一个包含追踪信息的页面，可以单独通过serve_traceback=True来设置。
```
import tornado.web
app = tornado.web.Application([], debug=True)
```
在构建路由映射列表时，可以传入多个信息：
```
[
    (r"/", Indexhandler),
    (r"/cpp", TornadoHandler, {"subject":"c++"}),
    url(r"/python", TornadoHandler, {"subject":"python"}, name="python_url")
]

```
路由中的字典，会传入到对应的RequestHandler的initialize()方法中
```
import tornado.web
class TornadoHandler(tornado.web.RequestHandler):
    def initialize(self, subject):
        self.subject = subject
        
    def get(self):
        self.write(self.subject)
```
对于路由中的name字段，注意此时不能再使用元组，而应使用tornado.web.url来构建。name是给该路由起一个名字，可以通过调用RequestHandler.reverse_url(name)来获取该名子对应的url。

```
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import url, RequestHandler

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    def get(self):
        python_url = self.reverse_url("python_url")
        self.write('<a href="%s">Tornado</a>' %
                   python_url)

class TornadoHandler(RequestHandler):
    def initialize(self, subject):
        self.subject = subject

    def get(self):
        self.write(self.subject)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/", Indexhandler),
            (r"/cpp", TornadoHandler, {"subject":"c++"}),
            url(r"/python", TornadoHandler, {"subject":"python"}, name="python_url")
        ],
        debug = True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
```
