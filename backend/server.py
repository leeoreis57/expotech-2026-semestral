import sys
import uuid
import json
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse

import state
from utils.mysql import MySqlDatabase

app = FastAPI()

db = MySqlDatabase()

qr_sessions = {}


@app.get("/join/{session_id}")
async def handle_join(session_id: str):
    if session_id not in qr_sessions:
        session = str(uuid.uuid4())
        qr_sessions[session] = None
        return RedirectResponse(url=f"/join/{session}")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "views", "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    qr_sessions[session_id] = websocket

    await websocket.send_json({"action": "connection:opened", "sessionId": session_id})

    try:
        while True:
            message = await websocket.receive_text()
            msg = json.loads(message)
            action = msg.get("action")

            if action == "user:login":
                payload = msg.get("payload", {})
                result = db.query(
                    "SELECT id_usuario, tipo_usuario, senha_usuario FROM tbl_usuarios WHERE username_usuario = %s",
                    (payload.get("username"),)
                )
                senha_plain = payload.get("password", "")
                senha_bd = result[0][2] if result else ""
                senha_ok = False
                if result:
                    if senha_bd.startswith("$2b$") or senha_bd.startswith("$2a$"):
                        senha_ok = bcrypt.checkpw(senha_plain.encode("utf-8"), senha_bd.encode("utf-8"))
                    else:
                        senha_ok = senha_plain == senha_bd
                        if senha_ok:
                            hashed = bcrypt.hashpw(senha_plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                            db.execute("UPDATE tbl_usuarios SET senha_usuario = %s WHERE id_usuario = %s", (hashed, result[0][0]))
                if senha_ok:
                    await websocket.send_json({"action": "user:login", "response": "OK"})
                    state.user_data["role"] = result[0][1]
                    state.user_data["user_id"] = result[0][0]
                    state.login_event.set()
                else:
                    await websocket.send_json({"action": "user:login", "response": "CREDENTIALS_INVALID"})

            elif action == "user:register":
                payload = msg.get("payload", {})
                required_fields = ["nome", "telefone", "username", "password"]

                if not all(payload.get(f) for f in required_fields):
                    await websocket.send_json({"action": "user:register", "response": "MISSING_FIELDS"})
                    continue

                try:
                    hashed = bcrypt.hashpw(payload["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                    db.execute(
                        "INSERT INTO tbl_usuarios (nome_usuario, cpf_usuario, telefone_usuario, username_usuario, senha_usuario, tipo_usuario) VALUES (%s, %s, %s, %s, %s, 'leitor')",
                        (payload["nome"], payload.get("cpf", ""), payload["telefone"], payload["username"], hashed)
                    )
                    user_result = db.query(
                        "SELECT id_usuario FROM tbl_usuarios WHERE username_usuario = %s",
                        (payload["username"],)
                    )
                    state.registered_user["id"] = user_result[0][0] if user_result else None
                    state.registered_user["username"] = payload["username"]
                    state.registered_user["nome"] = payload["nome"]
                    state.register_event.set()
                    await websocket.send_json({"action": "user:register", "response": "OK"})
                except Exception as e:
                    if "Duplicate entry" in str(e) and "username" in str(e):
                        await websocket.send_json({"action": "user:register", "response": "USERNAME_TAKEN"})
                    else:
                        await websocket.send_json({"action": "user:register", "response": "ERROR", "detail": str(e)})

            elif action == "user:delete":
                if state.user_data.get("role") != "admin":
                    await websocket.send_json({"action": "user:delete", "response": "UNAUTHORIZED"})
                    continue
                payload = msg.get("payload", {})
                user_id = payload.get("userId")
                try:
                    emprestimo_ativo = db.query(
                        "SELECT id_emprestimo FROM tbl_emprestimos WHERE id_leitor = %s AND data_devolucao IS NULL",
                        (user_id,)
                    )
                    if emprestimo_ativo:
                        await websocket.send_json({"action": "user:delete", "response": "HAS_ACTIVE_LOAN"})
                        continue
                    db.execute("DELETE FROM tbl_favoritos WHERE id_usuario = %s", (user_id,))
                    db.execute("DELETE FROM tbl_emprestimos WHERE id_leitor = %s", (user_id,))
                    db.execute("DELETE FROM tbl_usuarios WHERE id_usuario = %s", (user_id,))
                    await websocket.send_json({"action": "user:delete", "response": "OK"})
                except Exception as e:
                    await websocket.send_json({"action": "user:delete", "response": "ERROR"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"[WS] Erro: {e}")
    finally:
        qr_sessions.pop(session_id, None)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.server:app", host="0.0.0.0", port=80, reload=True)
