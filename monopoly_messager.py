'''
MESSAGES NEEDED:
Dice roll
Buy
Auction
Auction Bids
Withdraw from Auction
Card that's drawn
'''

import asyncio
import websockets
import random
import monopoly


async def main():

    async with websockets.connect("ws://132.36.167.100:8080") as websocket:

        try:
            user_name = input("ENTER NAME: ")
            if (len(user_name) == 0):
                user_name = "Player" + str(random.randint(0,99))
            await websocket.send("NEW USER " + user_name)

            player_list = []

            monopoly_game = None

            while True:
                server_message = await websocket.recv()
                print(server_message)

                if "NEW PLAYER" in server_message:
                    player_name = server_message[server_message.find(":")+1:server_message.find(",")]
                    player_piece = server_message[server_message.find(",")+1:]
                    player = monopoly.player(player_name,player_piece,balance=1500)
                    player_list.append(player)

                if "BEGIN GAME" in server_message:
                    monopoly_game = monopoly.main(player_list, websocket)

                if "rolls" in server_message:
                    start_index = server_message.find(":"+2)
                    roll_value = server_message[start_index:]
                    monopoly_game.sidebar.player.move(roll_value, 0)

                if server_message == "It is " + user_name + "'s turn.":
                    monopoly_game.sidebar.critical = False
                    monopoly_game.sidebar.render_buttons()
                elif "turn" in server_message:
                    monopoly_game.sidebar.critical = True
                    monopoly_game.sidebar.render_buttons()

                    
            
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed by server")

asyncio.run(main())