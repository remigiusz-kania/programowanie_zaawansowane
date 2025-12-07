import socket
import pickle
import threading
import time
import random
from typing import Dict, Any, List
from models import Soup, MainCourse, Dessert


HOST = 'localhost'
PORT = 5000
MAX_CLIENTS = 3

clients_lock = threading.Lock()
current_clients = 0

objects_map: Dict[str, Any] = {}


def initialize_objects() -> None:
    soups = [
        Soup("Tomato Soup", 65),
        Soup("Chicken Broth", 70),
        Soup("Mushroom Cream", 60),
        Soup("Borscht", 68)
    ]
    for i, soup in enumerate(soups, 1):
        objects_map[f"Soup_{i}"] = soup
    
    main_courses = [
        MainCourse("Grilled Salmon", 45.00),
        MainCourse("Beef Steak", 55.00),
        MainCourse("Chicken Parmesan", 38.00),
        MainCourse("Vegetable Risotto", 32.00)
    ]
    for i, main_course in enumerate(main_courses, 1):
        objects_map[f"MainCourse_{i}"] = main_course
    
    desserts = [
        Dessert("Chocolate Cake", 450),
        Dessert("Tiramisu", 380),
        Dessert("Ice Cream", 220),
        Dessert("Cheesecake", 410)
    ]
    for i, dessert in enumerate(desserts, 1):
        objects_map[f"Dessert_{i}"] = dessert
    
    print("Restaurant menu initialized:")
    for key, value in objects_map.items():
        print(f"  {key}: {value}")


def get_objects_by_class(class_name: str) -> List[Any]:
    result = []
    for key, value in objects_map.items():
        if key.startswith(class_name + "_"):
            result.append(value)
    return result


def handle_client(client_socket: socket.socket, address: tuple) -> None:
    global current_clients
    client_id = None
    
    try:
        data = client_socket.recv(1024)
        client_id = pickle.loads(data)
        print(f"Client ID {client_id} attempting to connect from {address}")

        with clients_lock:
            if current_clients >= MAX_CLIENTS:
                print(f"REFUSED client ID {client_id} - max clients reached ({MAX_CLIENTS})")
                client_socket.send(pickle.dumps("REFUSED"))
                return
            else:
                current_clients += 1
                print(f"ACCEPTED client ID {client_id} - current clients: {current_clients}/{MAX_CLIENTS}")
                client_socket.send(pickle.dumps("OK"))
        
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                request = pickle.loads(data)
                
                if request == "DISCONNECT":
                    print(f"Client ID {client_id} disconnecting")
                    break
                
                class_name = request
                print(f"Client ID {client_id} requested objects of class: {class_name}")
                
                delay = random.uniform(0.5, 2.0)
                print(f"Processing request for client ID {client_id} (delay: {delay:.2f}s)")
                time.sleep(delay)
                
                objects = get_objects_by_class(class_name)
                
                if objects:
                    print(f"Sending {len(objects)} {class_name} objects to client ID {client_id}:")
                    for obj in objects:
                        print(f"  - {obj}")
                    client_socket.send(pickle.dumps(objects))
                else:
                    print(f"Class {class_name} not found, sending fallback Soup to client ID {client_id}")
                    fallback = Soup("Zalewajka", 20)
                    client_socket.send(pickle.dumps([fallback]))
                    
            except Exception as e:
                print(f"Error handling request from client ID {client_id}: {e}")
                break
                
    except Exception as e:
        print(f"Error with client connection: {e}")
    finally:
        with clients_lock:
            if client_id is not None:
                current_clients -= 1
                print(f"Client ID {client_id} disconnected - current clients: {current_clients}/{MAX_CLIENTS}")
        client_socket.close()


def start_server() -> None:
    initialize_objects()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    
    print(f"\nServer started on {HOST}:{PORT}")
    print(f"Maximum clients: {MAX_CLIENTS}")
    print("Waiting for connections...\n")
    
    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
