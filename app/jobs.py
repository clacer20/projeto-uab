import threading
import time
import sys

def background_process_post(post_id, titulo):
    """
    Simula um processamento em segundo plano (ex: indexação, notificação, log).
    """
    def task():
        print(f"DEBUG: Iniciando processamento do post {post_id}: {titulo}", file=sys.stderr)
        # Simula uma tarefa demorada
        time.sleep(2)
        print(f"DEBUG: Finalizado processamento do post {post_id}", file=sys.stderr)
    
    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()
