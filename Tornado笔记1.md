Django为代表的python web应用部署时采用wsgi协议与服务器对接（被服务器托管），而这类服务器通常都是基于多线程的，也就是说每一个网络请求服务器都会有一个对应的线程来用web应用（如Django）进行处理。

Tornado旨在解决C10K问题：处理大于或等于一万的并发

Tornado是一个是一个轻量级的Web框架，类似于另一个Python web框架Web.py，其拥有异步非阻塞IO的处理方式。
作为Web服务器，Tornado有较为出色的抗负载能力，官方用nginx反向代理的方式部署Tornado和其它Python web应用框架进行对比，结果最大浏览量超过第二名近40%。
Tornado框架和服务器一起组成一个WSGI的全栈替代品。单独在WSGI容器中使用tornado网络框架或者tornaod http服务器，有一定的局限性，为了最大化的利用tornado的性能，推荐同时使用tornaod的网络框架和HTTP服务器

```
# hello.py
import tornado.web
import tornado.ioloop

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Tornado!")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
# 打开网址，输入127.0.0.1：8000即可看到response

```
RequestHandler:封装了对应一个请求的所有信息和方法，write(响应信息)就是写响应信息的一个方法；对应每一种http请求方式（get、post等），把对应的处理逻辑写进同名的成员方法中（如对应get请求方式，就将对应的处理逻辑写在get()方法中），当没有对应请求方式的成员方法时，会返回“405: Method Not Allowed”错误。

Application:Tornado Web框架的核心应用类，是与服务器对接的接口，里面保存了路由信息表，其初始化接收的第一个参数就是一个路由信息映射元组的列表；其listen(端口)方法用来创建一个http服务器实例，并绑定到给定端口（注意：此时服务器并未开启监听）。

tornado.ioloop:tornado的核心io循环模块，封装了Linux的epoll和BSD的kqueue，tornado高性能的基石。 
IOloop.current():返回当前线程的IOloop实例
IOloop.start():启动IOloop实例的IO循环，同时服务器监听被打开



