from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend.processor import process_dxf
import os, shutil

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, use your domain here
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process/")
async def upload_and_process(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    input_path = os.path.join(temp_dir, file.filename)
    output_path = os.path.join(temp_dir, f"processed_{file.filename}")

    # Save uploaded file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call your DXF processing logic
    process_dxf(input_path, output_path)

    return FileResponse(output_path, media_type="application/dxf", filename=f"processed_{file.filename}")
