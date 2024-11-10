from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi import Request
from fastapi.staticfiles import StaticFiles
import chatbot

app = FastAPI()

# Configura la carpeta de plantillas
templates = Jinja2Templates(directory="templates")

# Ruta para servir la página principal (front.html)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("front.html", {"request": request})

# Ruta para obtener respuesta del chatbot
class Message(BaseModel):
    message: str

# Servir archivos estáticos desde la carpeta "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/get_response")
def get_response(message: Message):
    user_message = message.message
    bot_response = chatbot.respuesta(user_message)
    return {"response": bot_response}

