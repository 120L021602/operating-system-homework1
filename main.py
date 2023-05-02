# 这是一个包含三个线程的应用，实现了全局数据共享、线程间通信、线程同步的功能。
# 该应用模拟了一个生产者-消费者模型，其中生产者线程随机生成数字并将其存储在全局队列中，
# 消费者线程从队列中读取数字并进行加和运算，统计出所有数字的和。
# 生产者线程和消费者线程使用了线程同步技术，确保了对全局队列的同步访问。
# 同时，通过信号量semaphore，消费者线程在等待队列中有数字时可以被唤醒，从而实现了线程间通信。

import threading
import queue
import random

# 全局共享数据：存储随机生成的数字（队列）
numbers = queue.Queue()

# 线程同步工具
mutex = threading.Lock()
semaphore = threading.Semaphore(0)


# 生产者线程
class ProducerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global numbers
        while True:
            # 随机生成数字并存储到队列中
            number = random.randint(1, 10)
            mutex.acquire()
            # 同步访问全局队列
            numbers.put(number)
            print("Producer: produced %s" % number)
            mutex.release()
            semaphore.release()
            # 通知消费者线程可以读取数字了


# 消费者线程
class ConsumerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global numbers
        total = 0
        while True:
            semaphore.acquire()
            # 等待生产者线程生成数字
            mutex.acquire()
            # 同步访问全局队列
            if numbers.empty():
                mutex.release()
                break
            number = numbers.get()
            total += number
            # 统计所有数字的和
            print("Consumer: consumed %s" % number)
            mutex.release()
            print("Consumer: total is %s" % total)


# 主线程
if __name__ == "__main__":
    producer_thread = ProducerThread()
    consumer_thread_1 = ConsumerThread()
    consumer_thread_2 = ConsumerThread()
    consumer_thread_3 = ConsumerThread()
    producer_thread.start()
    consumer_thread_1.start()
    consumer_thread_2.start()
    consumer_thread_3.start()
    producer_thread.join()
    consumer_thread_1.join()
    consumer_thread_2.join()
    consumer_thread_3.join()
    print("End of main thread.")

