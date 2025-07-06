import threading

# -------- 1 --------
def add_to_list(value, my_list):
    """
    问题：我不知道这段代码要求是每次返回同一个list还是不同的list，如果是不同的list，需要在函数内校验
    """
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list

# -------- 2 --------
def format_greeting(name, age):
    """
    问题：返回中缺少f
    """
    return f"你好，我叫{name}，今年{age}岁。"

# -------- 3 --------
class Counter:
    """
    问题：
    count = 0，是类变量，所有实例共享
    需要前面加self.count变为实例变量
    """
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count

# -------- 4 --------
class SafeCounter:
    """
    问题：
        初始代码没有加锁，不是线程安全的
    """
    def __init__(self):
        self.count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.count += 1

def worker(counter):
    for _ in range(1000):
        counter.increment()


counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# -------- 5 --------
def count_occurrences(lst):
    """
    问题：
        counts[item] =+ 1 应该是counts[item] += 1
    """
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1 
        else:
            counts[item] = 1
    return counts
