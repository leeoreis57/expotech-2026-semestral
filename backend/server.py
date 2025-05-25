from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
import uuid
import json
import os

from utils.mysql import MySqlDatabase

app = FastAPI()

db = MySqlDatabase()

# Sessões na memória
qr_sessions = {}
terminal_session = {}

@app.get("/join/{session_id}")
async def handle_join(session_id: str):
    if session_id not in qr_sessions:
        session = str(uuid.uuid4())
        qr_sessions[session] = None
        return RedirectResponse(url=f"/join/{session}")

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
                print(result)
                if result:
                    await websocket.send_json({ "action": "user:login", "response": "OK" })
                    print(result)
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
            elif action == "user:register": 
                payload = msgParsed.get("payload", {})

                # Campos obrigatórios
                required_fields = ["nome", "cpf", "telefone", "username", "password"]

                print(payload)
                # Verifica se todos os campos foram enviados
                if all(field in payload for field in required_fields):
                    try:
                        sql = """
                            INSERT INTO tbl_usuarios (nome_usuario, cpf_usuario, telefone_usuario, username_usuario, senha_usuario, tipo_usuario)
                            VALUES (%s, %s, %s, %s, %s, %s);
                        """
                        db.execute(sql, (
                            payload["nome"],
                            payload["cpf"],
                            payload["telefone"],
                            payload["username"],
                            payload["password"],
                            "leitor"
                        ))
                        db.connection.commit()

                        await websocket.send_json({
                            "action": "user:register",
                            "response": "OK"
                        })

                    except Exception as e:
                        # Verifica se o erro é de usuário já existente
                        if "Duplicate entry" in str(e) and "username" in str(e):
                            await websocket.send_json({
                                "action": "user:register",
                                "response": "USERNAME_TAKEN"
                            })
                        else:
                            await websocket.send_json({
                                "action": "user:register",
                                "response": "ERROR",
                                "detail": str(e)
                            })
                else:
                    await websocket.send_json({
                        "action": "user:register",
                        "response": "MISSING_FIELDS"
                    })

    except WebSocketDisconnect:
        print(f"[WS] Sessão desconectada: {session_id}")
    except Exception as e:
        print(f"[WS] Erro: {e}")
    finally:
        qr_sessions.pop(session_id, None)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=3000, reload=True)
