from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Trimly")


# Attach a file server to my app at /static, serve files from static
# folder, then call it static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return {"Status:" "This works! Hello World"}