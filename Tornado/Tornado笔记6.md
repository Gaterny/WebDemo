1.同步：
```
def req_a():
    """模拟请求a"""
    print ('开始处理请求req_a')
    print ('完成处理请求req_a')

def req_b():
    """模拟请求b"""
    print ('开始处理请求req_b')
    print ('完成处理请求req_b')

def main():
    """模拟tornado框架，处理两个请求"""
    req_a()
    req_b()

if __name__ == "__main__":
    main()
```
执行结果：
开始处理请求req_a
完成处理请求req_a
开始处理请求req_b
完成处理请求req_b

同步是按部就班的依次执行，始终按照同一个步调执行，上一个步骤未执行完不会执行下一步。

在处理请求req_a时需要执行一个耗时的工作（如IO）：
```
def long_io():
    """模拟耗时IO操作"""
    print ("开始执行IO操作")
    time.sleep(5)
    print ("完成IO操作")
    return "io result"
def req_a():
    """模拟请求a"""
    print ('开始处理请求req_a')
    print ('完成处理请求req_a')

def req_b():
    """模拟请求b"""
    print ('开始处理请求req_b')
    ret = long_io()
    print ('完成处理请求req_b')

def main():
    """模拟tornado框架，处理两个请求"""
    req_a()
    req_b()

if __name__ == "__main__":
    main()
```
执行结果：
开始处理请求req_a
开始执行IO操作
完成IO操作
完成处理请求req_a
开始处理请求req_b
完成处理请求req_b

耗时的操作会将代码执行阻塞住，即req_a未处理完req_b是无法执行的。想要解决这个问题，就需要用到异步处理

2. 异步
对于耗时的过程，我们将其交给别人（如其另外一个线程）去执行，而我们继续往下处理，当别人执行完耗时操作后再将结果反馈给我们，这就是我们所说的异步。

Tornado利用epoll来实现异步，即将异步过程交给epoll执行并进行监视回调
epoll主要是用来解决网络IO的并发问题，所以Tornado的异步编程也主要体现在网络IO的异步上，即异步Web请求。
