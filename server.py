from fastapi import FastAPI
import gradio as gr
import uvicorn

# import threading
# import os
# from http.server import SimpleHTTPRequestHandler
# from socketserver import TCPServer
# import subprocess

# def start_http_server():
#     static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './code/'))
#     if not os.path.exists(static_dir):
#         raise FileNotFoundError(f"Static directory not found: {static_dir}")
#     os.chdir(static_dir)
#     handler = SimpleHTTPRequestHandler
#     with TCPServer(("127.0.0.1", 8000), handler) as httpd:
#         print("Serving files at http://127.0.0.1:8000")
#         httpd.serve_forever()

# def start_gradio_app():
#     app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './app.py'))
#     if not os.path.exists(app_path):
#         raise FileNotFoundError(f"Gradio app file not found: {app_path}")
#     subprocess.run(["python", app_path])

# if __name__ == "__main__":
#     http_server_thread = threading.Thread(target=start_http_server)
#     http_server_thread.daemon = True
#     http_server_thread.start()
#     start_gradio_app()
#     os.system('cls' if os.name == 'nt' else 'clear')
#     print("Serving files at http://127.0.0.1:8000")

from app import demo


app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}


app = gr.mount_gradio_app(app, demo, path="/gradio")
