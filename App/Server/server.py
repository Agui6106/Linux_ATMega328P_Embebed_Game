
import os
import shutil
import signal
import sys

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

app = FastAPI() 

@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
<!DOCTYPE html>
<html>
    <head>
        <title>Upload and Download Files</title>
        <!-- minify -->
        <link href="https://unpkg.com/nes.css@2.3.0/css/nes.min.css" rel="stylesheet" />
        <!-- latest -->
        <link href="https://unpkg.com/nes.css@latest/css/nes.min.css" rel="stylesheet" />
        <!-- core style only -->
        <link href="https://unpkg.com/nes.css/css/nes-core.min.css" rel="stylesheet" />

        <link href="https://fonts.googleapis.com/css?family=Press+Start+2P" rel="stylesheet">
        <link href="https://unpkg.com/nes.css/css/nes.css" rel="stylesheet" />
    </style>
    </head>
    <body>
        <style>
            body {
                background-color: #4A71BC;
            }
        </style>
        <div class="nes-container with-title is-centered" style="color: white">
            <h4>GameNest.Inc team</h4>
            <h2>Welcome to GAMENEST Uploader Scores</h2>
        </div>

        <!-- Subir archivos -->
        <section class="nes-container">
            <section class="message-list">
              <section class="message -left">
                <!-- Balloon -->
                <div class="nes-balloon from-left">
                    <p>Upload a file</p>
                </div>
                <i class="nes-icon trophy is-medium"></i>
               </section>
            </section>
            <form action="/uploadfile/" method="post" enctype="multipart/form-data">
                <input type="file" class="is-primary" name="file">
                <input type="submit" class="is-primary" value="Submit">
            </form>
            
            <i class="nes-kirby"></i>
        </section>

        <!-- Descargar archivos -->
        <section class="nes-container">
            <section class="message-list">
              <section class="message -left">
                <!-- Balloon -->
                <div class="nes-balloon from-left">
                    <p>Download a file</p>
                </div>
                <i class="nes-icon coin is-medium"></i>
               </section>
            </section>
            <form id="downloadForm" action="/downloadfile/" method="get">
                <div class="nes-field">
                    <label for="filename">File Name</label>
                    <input type="text" id="filename" class="nes-input" name="filename" required>
                </div>
                <input type="submit" class="is-primary" value="Download">
            </form>

            <i class="nes-charmander"></i>
        </section>

        <script>
            document.getElementById('downloadForm').onsubmit = function(event) {
                event.preventDefault();
                var filename = document.getElementById('filename').value;
                window.location.href = '/downloadfile/' + filename;
            };
        </script>
        
        <section class="nes-container">
            <span class="nes-text is-success"> Crafted by: Agui, Pau, Isra</span>
        </section>
        
    </body>
</html>

    """
    return content

# - For everyone around the world who loves what they do - #
@app.get('/about_us')
def about_us():
    return "With love and passion: GameNest Systems Inc. Team - Santiaga de Queretaro. Mexico 2024"

# - Subir archvios al servidor - #
@app.post('/uploadfile/')
def upload_file(file:UploadFile = File(...)):
    try:
        # Context manager, archivos que necesitan cerrarse después de que se utilizan
        os.makedirs('./uploads', exist_ok = True)
        with open(f'./uploads/{file.filename}',"wb+") as f:
            shutil.copyfileobj(file.file, f)
        return "Upload complete. Thanks for using GameNest :]"
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Upload file error: {e}"})

# - Descargar archivos del servidor - #
@app.get('/downloadfile/{filename}')
def download_file(filename: str):
    file_path = f'./uploads/{filename}'
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    else:
        return JSONResponse(status_code=404, content={"message": "File not found"})

def signal_handler():
    print('Deteniendo el servidor...')
    sys.exit(0)

if __name__ == '__main__':
    import uvicorn
    signal.signal(signal.SIGTERM, signal_handler)
    uvicorn.run(app = app, host = "192.168.137.29", port = 8081)
