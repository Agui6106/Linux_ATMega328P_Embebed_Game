import os
import shutil
import signal
import sys

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

app = FastAPI() 

@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
<!DOCTYPE html>
<html>
    <head>
        <title>Upload a file</title>
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
        <div class="nes-container is-rounded">
            <img src="./GameNestWeb.jpeg" alt="fondo" style="width: 100%;">
        </div>

        <section class="nes-container">
            <section class="message-list">
              <section class="message -left">
                <!-- Balloon -->
                <div class="nes-balloon from-left">
                    <p>Upload a file</p>
                </div>
                <i class="snes-logo"></i>
               </section>
            </section>
            <form action="/uploadfile/">
                <input type="file" class="is-primary" name="file">
                <input type="submit" class="is-primary" value="Submit">
            </form>
            
            <i class="nes-kirby"></i>
        </section>
    </body>
</html>
    """
    return content

@app.get('/hello') # Decorators: Es una función que crea otra funciones
def hello():
    return "Hello"

@app.get('/bye')
def bye():
    return "bye"

@app.get('led/:led/on')
def turn_led_on():
    pass

@app.post('/uploadfile/')
def upload_file(file:UploadFile = File(...)):
    try:
        # Context manager, archivos que necesitan cerrarse después de que se utilizan
        os.makedirs('./uploads', exist_ok = True)
        with open(f'./uploads/{file.filename}',"wb+") as f:
            shutil.copyfileobj(file.file, f)
        return "Nice:) Thanks"
    except:
        return "Upload file"

def signal_handler():
    print('Deteniendo el servidor...')
    sys.exit(0)

if __name__ == '__main__':
    import uvicorn
    signal.signal(signal.SIGTERM, signal_handler)
    uvicorn.run(app = app, host = "0.0.0.0", port = 8081)