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
