import threading

login_event = threading.Event()
user_data = {"role": None, "user_id": None}

register_event = threading.Event()
registered_user = {"id": None, "username": None, "nome": None}
