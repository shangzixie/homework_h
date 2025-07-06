# homework

## quiz.py

codes please jump to the [quiz.py](quiz.py)

```python
def reverse_list(l: list):
    """
    Reverse a list without using any built-in functions.
    The function should return a reversed list.
    Input l is a list that may contain any type of data.
    """
    if len(l) == 0:
        return []
    left = 0
    right = len(l) - 1
    while left < right:
        l[left], l[right] = l[right], l[left]
        left += 1
        right -= 1
    return l
 
def solve_sudoku(matrix):
    """
    Write a program to solve a 9x9 Sudoku board.
    The board must be completed so that every row, column, and 3x3 section
    contains all digits from 1 to 9.
    Input: a 9x9 matrix representing the board.
    """
    def dfs(matrix, x, y):
        nextY = 0 if y == 8 else y + 1
        nextX = x + 1 if nextY == 0 else x
        
        if x == 9 and y == 0:
            return True
        
        if matrix[x][y] != 0:
            return dfs(matrix, nextX, nextY)
        else:
            for i in range(1, 10):
                matrix[x][y] = i
                if not check(matrix, x, y, i):
                    continue
                if dfs(matrix, nextX, nextY):
                    return True
            matrix[x][y] = 0
            return False
    
    def check(matrix, curX, curY, curNum):
        for j in range(9):
            if j == curY:
                continue
            if matrix[curX][j] == curNum:
                return False
        
        for i in range(9):
            if i == curX:
                continue
            if matrix[i][curY] == curNum:
                return False
        
        box_start_row = curX // 3 * 3
        box_start_col = curY // 3 * 3
        for i in range(3):
            for j in range(3):
                row = box_start_row + i
                col = box_start_col + j
                if row != curX and col != curY and matrix[row][col] == curNum:
                    return False
        
        return True

    dfs(matrix, 0, 0)
    return matrix
```


## review.py

```python
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
```


## the webapp

see the [readme.md](webapp/README.md) for more details


```python
# webapp/main.py
import io
import threading
from datetime import datetime
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lock = threading.Lock()
history = []

@app.get("/")
async def home():
    return {"message": "Image Compression Service"}

@app.post("/compress")
async def compress_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith('image/'):
        return {"error": "Please upload an image file"}
    
    try:
        with lock:
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            # support to save an image with transparency (RGBA mode) as JPEG format
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            elif image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            
            original_size = len(image_data)
            
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=70)
            output.seek(0)
            
            compressed_size = len(output.getvalue())
            
            history.append({
                "filename": file.filename,
                "original_size": original_size,
                "compressed_size": compressed_size,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            # handle filename with chinese characters
            safe_filename = file.filename.encode('ascii', 'ignore').decode('ascii') if file.filename else 'image'
            if not safe_filename:
                safe_filename = 'image'
            
            return Response(
                content=output.getvalue(),
                media_type="image/jpeg",
                headers={"Content-Disposition": f"attachment; filename=compressed_{safe_filename}.jpg"}
            )
            
    except Exception as e:
        return {"error": f"Failed to compress image: {str(e)}"}

@app.get("/history")
async def get_history():
    with lock:
        return {
            "total_processed": len(history),
            "history": history
        }
```