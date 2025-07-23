from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve the frontend folder
app.mount("/", StaticFiles(directory="phonebook-frontend", html=True), name="frontend")
