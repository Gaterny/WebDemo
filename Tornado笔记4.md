tornado.web.RequestHandler模块学习

利用http协议向服务器传递参数有几种途径：

查询字符串（query string)，形如key1=value1&key2=value2；
请求体（body）中发送的数据，比如表单数据、json、xml；
提取uri的特定部分，如/blogs/2016/09/0001，可以在服务器端的路由中用正则表达式截取；
在http报文的头（header）中增加自定义字段，如X-XSRFToken=xxxx。

1.获取查询字符串参数
get_query_argument(name, default=_ARG_DEFAULT, strip=True)

从请求的查询字符串中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。
default为设值未传name参数时返回的默认值，如若default也未设置，则会抛出tornado.web.MissingArgumentError异常。
strip表示是否过滤掉左右两边的空白字符，默认为过滤。

get_query_arguments(name, strip=True)
从请求的查询字符串中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表[]。

2. 获取请求体参数
get_body_argument(name, default=_ARG_DEFAULT, strip=True)
从请求体中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。
default与strip同前，不再赘述。

get_body_arguments(name, strip=True)
从请求体中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表[]。

说明：
对于请求体中的数据要求为字符串，且格式为表单编码格式（与url中的请求字符串格式相同），即key1=value1&key2=value2，HTTP报文头Header中的"Content-Type"为application/x-www-form-urlencoded 或 multipart/form-data。对于请求体数据为json或xml的，无法通过这两个方法获取。

3. 前两类方法的整合
get_argument(name, default=_ARG_DEFAULT, strip=True)
从请求体和查询字符串中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。

default与strip同前，不再赘述。

get_arguments(name, strip=True)
从请求体和查询字符串中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表[]。

来看以下代码：
```
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    def post(self):
        query_arg = self.get_query_argument("a")
        query_args = self.get_query_arguments("a")
        body_arg = self.get_body_argument("a")
        body_args = self.get_body_arguments("a", strip=False)
        arg = self.get_argument("a")
        args = self.get_arguments("a")

        default_arg = self.get_argument("b", "itcast")
        default_args = self.get_arguments("b")

        try:
            missing_arg = self.get_argument("c")
        except MissingArgumentError as e:
            missing_arg = "We catched the MissingArgumentError!"
            print e
        missing_args = self.get_arguments("c")

        rep = "query_arg:%s<br/>" % query_arg
        rep += "query_args:%s<br/>" % query_args 
        rep += "body_arg:%s<br/>"  % body_arg
        rep += "body_args:%s<br/>" % body_args
        rep += "arg:%s<br/>"  % arg
        rep += "args:%s<br/>" % args 
        rep += "default_arg:%s<br/>" % default_arg 
        rep += "default_args:%s<br/>" % default_args 
        rep += "missing_arg:%s<br/>" % missing_arg
        rep += "missing_args:%s<br/>" % missing_args

        self.write(rep)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    ```
