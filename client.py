import socket
import pickle
import random
from models import Soup, MainCourse, Dessert


HOST = 'localhost'
PORT = 5000

CLASS_MAP = {
    "Soup": Soup,
    "MainCourse": MainCourse,
    "Dessert": Dessert
}


def run_client(client_id: int) -> None:
    print(f"\n[Client {client_id}] Starting...")
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f"[Client {client_id}] Connected to restaurant server")
        
        client_socket.send(pickle.dumps(client_id))
        
        response = pickle.loads(client_socket.recv(1024))
        print(f"[Client {client_id}] Server response: {response}")
        
        if response == "REFUSED":
            print(f"[Client {client_id}] Connection refused - restaurant full, terminating")
            client_socket.close()
            return
        
        print("\n=== RESTAURANT MENU ===")
        print("1. Soup")
        print("2. MainCourse")
        print("3. Dessert")
        print("4. Drink")
        print("=======================")
        
        choice = input("Choose option (1-4): ").strip()
        
        menu_options = {
            "1": "Soup",
            "2": "MainCourse",
            "3": "Dessert",
            "4": "Drink"
        }
        
        requested_class = menu_options.get(choice)
        if requested_class is None:
            print(f"[Client {client_id}] Invalid choice, disconnecting")
            client_socket.send(pickle.dumps("DISCONNECT"))
            client_socket.close()
            return
        
        print(f"[Client {client_id}] Ordering {requested_class}...")
        client_socket.send(pickle.dumps(requested_class))

        data = client_socket.recv(4096)
        objects = pickle.loads(data)
        
        print(f"[Client {client_id}] Received {len(objects)} items:")
        
        expected_class = CLASS_MAP.get(requested_class)
        
        for obj in objects:
            try:
                if expected_class is None:
                    raise TypeError(f"Unknown class '{requested_class}', received {type(obj).__name__}")
                elif isinstance(obj, expected_class):
                    print(f"[Client {client_id}]   {requested_class}: {obj}")
                else:
                    raise TypeError(f"Expected {requested_class}, got {type(obj).__name__}")
                    
            except TypeError as e:
                print(f"[Client {client_id}]   CASTING ERROR: {e}")
        
        print(f"\n[Client {client_id}] Disconnecting...")
        client_socket.send(pickle.dumps("DISCONNECT"))
        client_socket.close()
        print(f"[Client {client_id}] Finished")
        
    except ConnectionRefusedError:
        print(f"[Client {client_id}] Cannot connect to server")
    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")


if __name__ == "__main__":
    client_id = random.randint(100, 999)
    run_client(client_id)
