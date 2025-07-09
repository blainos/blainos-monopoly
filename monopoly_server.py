import asyncio
import websockets

users = []
sockets = []
pieces = [
    "car",
    "hat",
    "iron",
    "shoe"
]
num_users = 2

async def send_all(message: str):
    for socket in sockets:
        await socket.send(message)

async def handle_connection(websocket):
    sockets.append(websocket)
    global curr_user
    try:
        # Add users to start game
        while len(users) < num_users:
            message = await websocket.recv()

            if "NEW USER" in message:
                users.append(message[9:])

        i = 0
        for user in users:
            await send_all("NEW PLAYER:" + user + "," + pieces[i])
            i += 1

        await send_all("BEGIN GAME")

        # Main game loop
        while True:
            
            message = await websocket.recv()

            await send_all(message)

            if "KILL" in message:
                break

            

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")

    except websockets.ConnectionClosedOK:
        print("The client has disconnected")

    except Exception as e:
        print(f"An Error Occured: {e}")

async def main():
    async with websockets.serve(handle_connection, "132.36.167.100", 8080, ping_interval=60, ping_timeout=60):  
        print("Server started on port 8080")
        print("\n")
        await asyncio.Future()
    
asyncio.run(main())