import asyncio
import uuid
import qrcode
import io
from aiohttp import web
import websockets
import threading
import os
import json 

from utils.mysql import MySqlDatabase

# Sessões armazenadas na memória
qr_sessions = {}        
terminal_session = {}
authenticated_sessions = set() 
db = MySqlDatabase()

# Gerar QR com link
def generate_qr(session_id):
    url = f"https://ebd0-2804-41a0-3f06-5b00-9816-be8e-2f3d-36d4.ngrok-free.app/join/{session_id}"

    img = qrcode.make(url)
    buf = io.BytesIO()

    img.save(buf)
    buf.seek(0)
    return buf

# Rotas do Servidor
async def handle_main(request):
    session_id = str(uuid.uuid4())
    request.app['websockets'][session_id] = None

    img_data = generate_qr(session_id)
    return web.Response(body=img_data.read(), content_type='image/png')

async def handle_join(request):
    file_path = os.path.join("views", "index.html")

    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()

    return web.Response(text=content, content_type='text/html')

# WebSocket 
async def websocket_handler(websocket):
    session_id = str(uuid.uuid4())
    qr_sessions[session_id] = websocket
    print(f"[WS] Sessão iniciada: {session_id}")

    await websocket.send(json.dumps({ "action": "connection:opened", "sessionId": session_id }))

    try:
        async for message in websocket:
            msgParsed = json.loads(message)
            action = msgParsed["action"]
            
            if action == "terminal:start": 
                terminal_id = msgParsed['terminalId']
                terminal_session[terminal_id] = websocket

                await websocket.send(json.dumps({ 'action': 'terminal:session', 'response': 'OK' }))
            if action == "user:login":
                payload = msgParsed["payload"]
                sql = """
                    SELECT id_usuario, tipo_usuario, username_usuario, senha_usuario FROM tbl_usuarios
                    WHERE username_usuario = %s AND senha_usuario = %s;
                """

                result = db.query(sql, (payload["username"], payload["password"]))
                if len(result) == 1:
                    await websocket.send(json.dumps({ "action": "user:login", "response": "OK" }));
                    
                    print(result[0])
                    ws = terminal_session.get('default')
                    if ws:
                        await ws.send(json.dumps({ 'action': 'user:logged', 'payload': { 'username': payload['username'], 'role': result[0][1], 'userId': result[0][0] } }))
                else: 
                    await websocket.send(json.dumps({ "action": "user:login", "response": "CREDENTIALS_INVALID" }));
    except Exception as error:
        print(error)
        print(f"[WS] Sessão desconectada: {session_id}")
    finally:
        qr_sessions.pop(session_id, None)

# Thread para rodar servidor WebSocket
def start_websocket_server():
    async def handler(ws, path):
        await websocket_handler(ws)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    ws_server = websockets.serve(handler, "localhost", 6789)
    loop.run_until_complete(ws_server)

    print("[WS] Servidor WebSocket rodando na porta 6789")
    loop.run_forever()

# Thread para rodar servidor HTTP
def start_http_server():
    app = web.Application()
    app['websockets'] = {}

    app.router.add_get('/', handle_main)
    app.router.add_get('/join/{session_id}', handle_join)

    web.run_app(app, port=80)

# Iniciar os dois servidores
if __name__ == '__main__':
    threading.Thread(target=start_websocket_server, daemon=True).start()
    start_http_server()
