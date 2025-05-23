from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uuid
import json
import os
from utils.banco import MySqlDatabase

app = FastAPI()

db = MySqlDatabase()

# Sessões na memória
qr_sessions = {}
terminal_session = {}

@app.get("/join/{session_id}")
async def handle_join(session_id: str):
    file_path = os.path.join("views", "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    qr_sessions[session_id] = websocket
    print(f"[WS] Sessão iniciada: {session_id}")

    await websocket.send_json({ "action": "connection:opened", "sessionId": session_id })

    try:
        while True:
            message = await websocket.receive_text()
            msgParsed = json.loads(message)
            action = msgParsed.get("action")

            if action == "terminal:start":
                terminal_id = msgParsed.get("terminalId")
                terminal_session[terminal_id] = websocket
                await websocket.send_json({ "action": "terminal:session", "response": "OK" })

            elif action == "user:login":
                payload = msgParsed.get("payload", {})
                sql = """
                    SELECT id_usuario, tipo_usuario, username_usuario, senha_usuario FROM tbl_usuarios
                    WHERE username_usuario = %s AND senha_usuario = %s;
                """
                result = db.query(sql, (payload.get("username"), payload.get("password")))
                if len(result) == 1:
                    await websocket.send_json({ "action": "user:login", "response": "OK" })
                    print(result[0])
                    ws = terminal_session.get("default")
                    if ws:
                        await ws.send_json({
                            "action": "user:logged",
                            "payload": {
                                "username": payload.get("username"),
                                "role": result[0][1],
                                "userId": result[0][0]
                            }
                        })
                else:
                    await websocket.send_json({ "action": "user:login", "response": "CREDENTIALS_INVALID" })

    except WebSocketDisconnect:
        print(f"[WS] Sessão desconectada: {session_id}")
    except Exception as e:
        print(f"[WS] Erro: {e}")
    finally:
        qr_sessions.pop(session_id, None)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
