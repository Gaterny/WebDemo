import tornado.httpserver   
import tornado.ioloop   
import tornado.options   
import tornado.web  

from tornado.options import define, options   
define("port", default=8000, help="run on the given port", type=int)  #设置端口,默认是8000,帮助文档,以及参数接收的类型int

class IndexHandler(tornado.web.RequestHandler):   
    def get(self):   #对Http的get请求做出响应
        greeting = self.get_argument('greeting', 'Hello')   #没有指定greeting的值,将会使用get_argument的第二个参数作为默认值
        self.write(greeting + ', This is Tornado!')   #以一个字符串作为函数的参数,将其写入到HTTp响应中

    def post(self):
    	pass

if __name__ == "__main__":
    tornado.options.parse_command_line()   #解析命令
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])   #Application类实例, handlers处理地址映射
    http_server = tornado.httpserver.HTTPServer(app)   
    http_server.listen(options.port)    #监听指定的端口  
    tornado.ioloop.IOLoop.instance().start()  #由IOloop启动消息循环

# #导入了一些Tornado模块
# tornado.httpserver — 一个无阻塞HTTP服务器的实现
# tornado.ioloop — 核心的I/O循环
# tornado.options — 解析终端参数
# tornado.web — 包含web框架的大部分主要功能，包含RequestHandler和Application两个重要的类
# handlers定义根路径的路由和处理函数之间的映射
