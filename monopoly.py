import json
import random
import tkinter as tk
from PIL import Image, ImageTk
import time
import emoji

class InsufficientFunds(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class tile:
    def __init__(self, type: str, name: str):
        self.type = type
        self.name = name
        self.space = None

    def __str__(self):
        return f"{self.name}"
    
    def link_space(self, space):
        self.space = space

class property(tile):

    def __init__(self, type: str, name: str):
        super().__init__(type, name)
        self.owner = None
        self.mortgaged = False

    def owned(self):
        if self.owner == None:
            return False
        else:
            return True
    
    def update_owner(self, player):
        self.owner = player

    def print_detail(self):
        print(self.name + "\n\t" + "Owner: " + self.owner + "\n\t" + "Mort: " + str(self.mortgaged) + "\n\t")
    
    def get_detail(self):
        pass


class color(property):

    def __init__(self, type: str, color: str, name: str, price: int, upgrade: int, rents: dict):
        super().__init__(type, name)
        self.color = color
        self.price = price
        self.upgrade = upgrade
        self.rents = rents
        self.mortgage_price = self.price // 2
        self.num_houses = 0
        self.monopoly_flag = False

    def add_house(self):
        self.num_houses += 1

    def get_rent(self, dice_roll=0, multiplier=1):
        if self.mortgaged:
            return 0
        if self.monopoly_flag and self.num_houses == 0:
            return self.rents[0] * 2
        else:
            return self.rents[self.num_houses]
        
    def print_detail(self):
        print(self.name + 
              "\n\t Color: " + self.color + 
              "\n\t Price: $" + str(self.price) + 
              "\n\t Owner: " + str(self.owner) + 
              "\n\t  Mort: " + str(self.mortgaged) + 
              "\n\t\t          RENT: \t$" + str(self.rents[0]) + 
              "\n\t\t  with 1 house: \t$" + str(self.rents[1]) + 
              "\n\t\t with 2 houses: \t$" + str(self.rents[2]) + 
              "\n\t\t with 3 houses: \t$" + str(self.rents[3]) + 
              "\n\t\t with 4 houses: \t$" + str(self.rents[4]) + 
              "\n\t\t    with hotel: \t$" + str(self.rents[5]) + 
              "\n\t\tMortgage Value: $" + str(self.mortgage_price) + 
              "\n\t\tHouses cost $" + str(self.upgrade) + " each")
        
    def get_detail(self) -> str:
        detail = ("RENT: $" + str(self.rents[0]) + 
              "\nwith color set: \t$" + str(self.rents[0]*2) +
              "\nwith 1 house: \t$" + str(self.rents[1]) + 
              "\nwith 2 houses: \t$" + str(self.rents[2]) + 
              "\nwith 3 houses: \t$" + str(self.rents[3]) + 
              "\nwith 4 houses: \t$" + str(self.rents[4]) + 
              "\nwith hotel: \t$" + str(self.rents[5]) + 
              "\nMortgage Value: $" + str(self.mortgage_price) + 
              "\nHouses cost $" + str(self.upgrade) + " each" +
              "\nHotels, $" + str(self.upgrade) + " plus 4 houses")
        return detail


class railroad(property):

    def __init__(self, type: str, name: str, price: int, rents: dict):
        super().__init__(type, name)
        self.price = price
        self.rents = rents
        self.mortgage_price = self.price // 2
        self.num_rr = 0

    def get_rent(self, dice_roll=0, multiplier=1): # such a dumb fix
        if self.mortgaged:
            return 0
        else:
            return self.rents[self.num_rr] * multiplier
        
    def print_detail(self):
        print(self.name + 
              "\n\t Price: $" + str(self.price) + 
              "\n\t Owner: " + str(self.owner) + 
              "\n\t  Mort: " + str(self.mortgaged) + 
              "\n\t\t           RENT:\t $" + str(self.rents[0]) + 
              "\n\t\tif 2 RR's owned:\t $" + str(self.rents[1]) + 
              "\n\t\tif 3 RR's owned:\t $" + str(self.rents[2]) + 
              "\n\t\tif 4 RR's owned:\t $" + str(self.rents[3]) + 
              "\n\t\t Mortgage Value: $" + str(self.mortgage_price))
        
    def get_detail(self):
        detail = ("RENT: \t\t $" + str(self.rents[0]) + 
              "\nif 2 RR's owned:\t $" + str(self.rents[1]) + 
              "\nif 3 RR's owned:\t $" + str(self.rents[2]) + 
              "\nif 4 RR's owned:\t $" + str(self.rents[3]) + 
              "\n\nMortgage Value:\t$" + str(self.mortgage_price))
        return detail


class utility(property):

    def __init__(self, type: str, name: str, price: int, mults: dict):
        super().__init__(type, name)
        self.price = price
        self.mults =  mults
        self.mortgage_price = self.price // 2
        self.num_u = 0

    def get_rent(self, dice_roll=0, multiplier=1):
        if self.mortgaged:
            return 0
        else:
            if self.num_u == 2:
                multiplier = 1
            return self.mults[self.num_u * multiplier] * dice_roll
        
    def print_detail(self):
        print(self.name + 
              "\n\t Price: $" + str(self.price) + 
              "\n\t Owner: " + str(self.owner) + 
              "\n\t  Mort: " + str(self.mortgaged) + 
              "\n\t\tRENT:" + 
              "\n\t\t  1 utility owned = " + str(self.mults[0]) + "x dice roll" + 
              "\n\t\t2 utilities owned = " + str(self.mults[1]) + "x dice roll" + 
              "\n\t\t Mortgage Value: $" + str(self.mortgage_price))
        
    def get_detail(self):
        detail = ("   If one \"Utility\" is owned," + 
              "\nrent is " + str(self.mults[0]) + " times amount" + 
              "\nshown on dice." + 
              "\n   If both \"Utilities\" are owned," +
              "\nrent is " + str(self.mults[1]) + " times amount" + 
              "\nshown on dice.\n"
              "\nMortgage Value: $" + str(self.mortgage_price))
        return detail

class tax(tile):
    def __init__(self, type: str, name: str, amount: int):
        super().__init__(type, name)
        self.amount = amount

class draw(tile):
    def __init__(self, type: str, name: str):
        super().__init__(type, name)

class go(tile):
    def __init__(self, type: str, name: str, pay: int):
        super().__init__(type, name)
        self.pay = pay

class jail(tile):
    def __init__(self, type: str, name: str, fine: int):
        super().__init__(type, name)
        self.fine = fine

class free(tile):
    def __init__(self, type: str, name: str, house_rule=False):
        super().__init__(type, name)
        self.house_rule = house_rule
        self.payout = 0

class gotojail(tile):
    def __init__(self, type: str, name: str):
        super().__init__(type, name)

class player:

    def __init__(self, name: str, piece: str, balance: int):
        self.name = name
        self.piece = piece
        self.temp_balance = balance
        self.gui = None
        self.position = 0
        self.property_list = []
        self.corner = 0
        self.jail_sentence = 0
        self.free_cards = 0

    def set_space_list(self, space_list: list):
        self.space_list = space_list
        self.balance = tk.IntVar(self.space_list[0].master, self.temp_balance)

        unit = self.space_list[1].width + self.space_list[1].height
        size_tuple = (unit//5,unit//5)
        import_img = Image.open(self.piece + ".png")
        resize_img = import_img.resize(size_tuple)
        self.piece_img = ImageTk.PhotoImage(image=resize_img)

    def __str__(self):
        return f"{self.name}"
    
    def pay(self, amount: int):
        '''Decreases player's balance by amount given'''
        if amount > self.balance.get():
            raise InsufficientFunds()
        self.balance.set(self.balance.get() - amount)
        print("\033[38;2;205;49;49m" + self.name + " -$" + str(amount) + "\033[0m")

    def collect(self, amount: int):
        '''Increases player's balance by amount given'''
        self.balance.set(self.balance.get() + amount)
        print("\033[38;2;35;209;139m" + self.name + " +$" + str(amount) + "\033[0m")

    def add_property(self, property: property, buy=True, amount=0):
        print(self.name + " now owns " + property.name)
        self.property_list.append(property)
        if buy:
            self.pay(property.price)
        else:
            if amount > 0:
                self.pay(amount)
        property.owner = self

        # This is lowkey inefficient
        num_rr = -1
        num_u = -1

        color_counts = {
            "brown": 0,
            "teal": 0,
            "magenta": 0,
            "orange": 0,
            "red": 0,
            "yellow": 0,
            "green": 0,
            "navy": 0
        }

        for prop in self.property_list:
            if prop.type == "RAILROAD":
                num_rr += 1
            if prop.type == "UTILITY":
                num_u += 1
            if prop.type == "COLOR":
                color_counts[prop.color] += 1
        
        for prop in self.property_list:
            if prop.type == "RAILROAD":
                prop.num_rr = num_rr
            if prop.type == "UTILITY":
                prop.num_u = num_u
            if prop.type == "COLOR":
                if (prop.color == "brown" or prop.color == "navy") and color_counts[prop.color] == 2:
                    prop.monopoly_flag = True
                elif color_counts[prop.color] == 3:
                    prop.monopoly_flag = True

        # self.space_list[self.position].event_generate("<<Tap>>")
        # self.space_list[self.position].event_generate("<<Land>>")

    def remove_property(self, property_string: str):
        prop_to_remove = None
        for p in self.property_list:
            if p.name == property_string:
                prop_to_remove = p
        if prop_to_remove is not None:
            self.property_list.remove(prop_to_remove)

        # This is lowkey inefficient also DUPLICATE CODE WEE WOO WEE WOO
        num_rr = -1
        num_u = -1

        color_counts = {
            "brown": 0,
            "teal": 0,
            "magenta": 0,
            "orange": 0,
            "red": 0,
            "yellow": 0,
            "green": 0,
            "navy": 0
        }

        for prop in self.property_list:
            if prop.type == "RAILROAD":
                num_rr += 1
            if prop.type == "UTILITY":
                num_u += 1
            if prop.type == "COLOR":
                color_counts[prop.color] += 1
        
        for prop in self.property_list:
            if prop.type == "RAILROAD":
                prop.num_rr = num_rr
            if prop.type == "UTILITY":
                prop.num_u = num_u
            if prop.type == "COLOR":
                if (prop.color == "brown" or prop.color == "navy") and color_counts[prop.color] == 2:
                    prop.monopoly_flag = True
                elif color_counts[prop.color] == 3:
                    prop.monopoly_flag = True

        return prop_to_remove


    def house_check(self, property: property, mode: str):
        if property.type == "COLOR": # might be redundant
            if mode == "buy" and self.balance.get() < property.upgrade:
                return False
        
        color_set = []
        for prop in self.property_list:
            if prop.type == "COLOR":
                if prop.color == property.color:
                    color_set.append(prop)
        
        for prop in color_set:
            if mode == "buy" and property.num_houses > prop.num_houses:
                return False
            if mode == "sell" and property.num_houses < prop.num_houses:
                return False
            
        return True

    def get_piece(self):
        return self.piece_img
    
    def move(self, d1: int, d2: int):

        number = d1+d2

        if self.jail_sentence > 0 and d1 != d2:
            self.jail_sentence -= 1
            if self.jail_sentence == 0:
                self.pay(self.space_list[self.position].property.fine)
                self.space_list[self.position].remove_piece(self)
                self.space_list[self.position].put_piece(self)
            return
        elif self.jail_sentence > 0 and d1 == d2:
            self.jail_sentence = 0

        window = self.space_list[self.position].master
        buttons = []
        for w in window.grid_slaves():
            if (int(w.grid_info()["row"]) == 9 and (int(w.grid_info()["column"]) == 11 or int(w.grid_info()["column"]) == 12 or int(w.grid_info()["column"]) == 13)):
                w.configure(state='disabled')
                buttons.append(w)

        destination = (self.position + number)
        for i in range(self.position,destination):
            pos = i % 40
            next = (pos+1)%40
            #self.space_list[pos].master.after(1000)
            self.space_list[pos].remove_piece(self)
            self.space_list[next].event_generate("<<Tap>>")
            self.space_list[next].put_piece(self)

            # event_poser = event_fake(self.space_list[next])
            # display_title_deed(event_poser)
            # self.space_list[next].event_generate("<<Tap>>")
            
            # test = tk.Canvas()
            # test.event_generate()
        self.position = destination % 40
        for b in buttons:
            b.configure(state='normal')
        self.space_list[self.position].event_generate("<<Land>>")

    def teleport(self, destination: int):
        self.space_list[self.position].remove_piece(self)
        self.space_list[destination].event_generate("<<Tap>>")
        self.space_list[destination].put_piece(self)
        self.position = destination
        self.space_list[self.position].event_generate("<<Land>>")

    def section(self, pos, next):
        time.sleep(0.1)
        self.space_list[pos].remove_piece(self)
        self.space_list[next].put_piece(self)

    def link_gui(self, player_gui):
        self.gui = player_gui




class spaceGUI(tk.Canvas):

    def __init__(self, tile_text: str, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.tile_text = tile_text
        self.tile_name = tile_text.replace("-\n", "")
        self.tile_name = self.tile_name.replace("\n", " ")
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.position = None

        self.property = None
        self.pieces = []
        self.pieces_pos = [False, False, False, False]


    def link_property(self, tile_list: list, index: int):
        #print(str(tile_list))
        tile_list[index].link_space(self)
        self.property = tile_list[index]
        self.position = index

    def put_piece(self, player: player):
        piece_img = player.get_piece()
        unit_width = (self.width) // 4
        unit_height = (self.height) // 4
        player.corner = self.pieces_pos.index(False)
        match player.corner:
            case 0:
                x1 = self.width - unit_width
                y1 = unit_height
                if self.property.type == "JAIL":
                    if player.jail_sentence > 0:
                        x1 = x1 # do nothing
                        y1 = y1 # do nothing 
                    else:
                        x1 = x1 + (unit_width//2)
                        y1 = self.height - (unit_height//2)
            case 1:
                x1 = unit_width
                y1 = unit_height
                if self.property.type == "JAIL":
                    if player.jail_sentence > 0:
                        x1 = unit_width * 2
                        y1 = y1 # do nothing 
                    else:
                        #x1 = x1 - (unit_width//2)
                        y1 = self.height - (unit_height//2)
            case 2:
                x1 = unit_width
                y1 = self.height - unit_height
                if self.property.type == "JAIL":
                    if player.jail_sentence > 0:
                        x1 = x1 * 2
                        y1 = self.height - (unit_height*2)
                    else:
                        x1 = unit_width//2
                        y1 = y1 - (unit_height//2)
            case 3:
                x1 = self.width - unit_width
                y1 = self.height - unit_height
                if self.property.type == "JAIL":
                    if player.jail_sentence > 0:
                        x1 = x1
                        y1 = self.height - (unit_height*2)
                    else:
                        x1 = unit_width//2
                        y1 = unit_height//2

        piece_tag = self.create_image(x1, y1, image=piece_img, tags=player.piece)
        self.pieces.append(player.piece)
        #print(self.tile_name + ": " + player.piece)
        self.pieces_pos[player.corner] = True
        self.update()
        time.sleep(0.2)

    def remove_piece(self, player:player):
        self.delete(player.piece)
        self.pieces.remove(player.piece)
        self.pieces_pos[player.corner] = False

    def mortgage(self):
        self.create_line(0,0,self.width,self.height,fill="red",width=2, tags="mortgage")

    def unmortgage(self):
        self.delete("mortgage")


class colorGUI(spaceGUI):
    def __init__(self, set_color: str, board_side: str, tile_text: str, master=None, **kwargs):
        super().__init__(tile_text, master, bd=0, highlightthickness=0, **kwargs)
        self.set_color = set_color
        self.board_side = board_side
        self.strip_height = (self.height + self.width) // 10
        self.font_size = (self.height + self.width) // 15
        super().create_rectangle(0,0, self.width, self.height, outline="black", width=2)
        match board_side:
            case "bottom":
                super().create_rectangle(0, 0, self.width, self.strip_height, fill=self.set_color, outline="black", width=2)
            case "left":
                super().create_rectangle(self.width-self.strip_height, 0, self.width, self.height, fill=self.set_color, outline="black", width=2)
            case "top":
                super().create_rectangle(0, self.height-self.strip_height, self.width, self.height, fill=self.set_color, outline="black", width=2)
            case "right":
                super().create_rectangle(0, 0, self.strip_height, self.height, fill=self.set_color, outline="black", width=2)
        super().create_text(self.width//2, self.height//2, text=self.tile_text, font=("Bahnschrift Condensed", self.font_size))

        size_tuple = (self.strip_height, self.strip_height)
        import_img = Image.open("house_" + self.board_side + ".png")
        resize_img = import_img.resize(size_tuple)
        self.house_img = ImageTk.PhotoImage(image=resize_img)

        self.houses = []

    def add_house(self):
        match self.board_side:
            case "bottom":
                start_x = self.width//8
                start_y = self.strip_height//2
                offset_x = self.width//4
                offset_y = 0
            case "left":
                start_x = self.width - (self.strip_height//2)
                start_y = self.height//8
                offset_x = 0
                offset_y = self.height//4
            case "top":
                start_x = self.width - (self.width//8)
                start_y = self.height - (self.strip_height//2)
                offset_x = -self.width//4
                offset_y = 0
            case "right":
                start_x = self.strip_height//2
                start_y = self.height - (self.height//8)
                offset_x = 0
                offset_y = -self.height//4

        spacing_x = offset_x * len(self.houses)
        spacing_y = offset_y * len(self.houses)
        house_id = self.create_image(start_x+spacing_x, start_y+spacing_y, image=self.house_img)
        self.houses.append(house_id)
    
    def remove_house(self):
        house_id = self.houses.pop()
        self.delete(house_id)


class otherGUI(spaceGUI):
    def __init__(self, tile_text: str, master=None, **kwargs):
        super().__init__(tile_text, master, bd=0, highlightthickness=0, **kwargs)
        self.font_size = (self.height + self.width) // 15
        super().create_rectangle(0,0, self.width, self.height, outline="black", width=2)
        self.create_text(self.width//2, self.height//2, text=self.tile_text, font=("Bahnschrift Condensed", self.font_size), tags="text")

    def edit_text(self, text: str):
        small_font_size = self.font_size // 3
        self.itemconfig("text", text=text, font=("Bahnschrift Light", small_font_size), width=(self.height+self.width)//3)

class cornerGUI(spaceGUI):
    def __init__(self, tile_text: str, master=None, **kwargs):
        super().__init__(tile_text, master, bd=0, highlightthickness=0, **kwargs)
        self.font_size = (self.height + self.width) // 15
        self.strip_height = (self.height + self.width) // 10
        super().create_rectangle(0,0, self.width, self.height, outline="black", width=2)
        match self.tile_text:
            case "FREE PARKING":
                self.create_text(self.width//2, self.height//2, text=self.tile_text, font=("Bahnschrift Condensed", self.font_size), angle=45)
            case "GO TO JAIL":
                self.create_text(self.width//2, self.height//2, text=self.tile_text, font=("Bahnschrift Condensed", self.font_size), angle=315)
            case "GO":
                self.create_text(self.width//2, self.height//2, text=self.tile_text, font=("Bahnschrift Condensed", self.font_size*2), angle=0)
            case "IN JAIL\nJUST VISITING":
                #self.tile_text = "JAIL" # Just commented this out and not sure if it will have unintended consequences
                super().create_rectangle(self.strip_height,0,self.width,self.height-self.strip_height, fill="orange", outline="black", width=2)
                self.create_text(self.width-(self.strip_height//2), self.strip_height//2, text="IN", font=("Bahnschrift Condensed", self.font_size), angle=315)
                self.create_text(self.strip_height*2, self.height-(self.strip_height*2), text="JAIL", font=("Bahnschrift Condensed", self.font_size), angle=315)
                self.create_text(self.strip_height//2, (self.height-self.strip_height)//2, text="JUST", font=("Bahnschrift Condensed", self.font_size), angle=270)
                self.create_text(self.width-((self.width-self.strip_height)//2),self.height-(self.strip_height//2), text="VISITING", font=("Bahnschrift Condensed", self.font_size))

class playerGUI:
    def __init__(self, player: player, window: tk.Tk, width: int, row: int, col: int):
        self.player = player
        self.balance_str = tk.StringVar(window, ("$" + str(self.player.balance.get())))
        self.balance_num = self.player.balance
        self.inactive_color = "light grey"

        self.width = width
        self.height = (width//4)
        margin = 0

        colspan = 2
        if col == 0 or col == 10:
            colspan = 1
        self.canvas = tk.Canvas(window, width=width, height=self.height, bd=0, highlightthickness=0)
        self.canvas.grid(row=row, column=col, columnspan=colspan)

        self.rect_id = self.canvas.create_rectangle(margin, margin, width-(margin), self.height-(margin), fill="light grey", outline="black", width=2)
        self.canvas.create_image(width//5,width//8, image=player.get_piece())
        self.text_id = self.canvas.create_text(width//3, width//8, anchor="w", text=(self.balance_str.get()), font=("Bahnschrift SemiBold", width//8))

        self.balance_num.trace_add('write', self.change_balance)

    def change_balance(self, *args):
        
        self.balance_str.set("$" + str(self.balance_num.get()))
        self.canvas.itemconfigure(self.text_id, text=(self.balance_str.get()))

    def highlight(self, bool=True):
        if bool:
            self.canvas.itemconfigure(self.rect_id, fill="red")
        else:
            self.canvas.itemconfigure(self.rect_id, fill=self.inactive_color)

    def auction_highlight(self, bool=True):
        if bool:
            self.canvas.itemconfigure(self.rect_id, fill="green")
        else:
            self.canvas.itemconfigure(self.rect_id, fill=self.inactive_color)

    def eliminate(self):
        self.inactive_color = "gray15"
        self.canvas.itemconfigure(self.rect_id, fill=self.inactive_color)
        self.canvas.itemconfigure(self.text_id, fill="red4")
    


def review_properties(player: player):
    while (answer != "Y" or answer != "N"):
        answer = input("Review your properties? (Y/N) ")
        if answer == "Y":
            while (answer != str(len(player.property_list))):
                i = 0
                for prop in player.property_list:
                    print(str(i) + " " + str(prop))
                    i += 1
                print(str(i) + " Done")
                answer = input("Select the corresponding number to view the property: ")
                if answer == str(i):
                    return None
                player.property_list[answer].print_detail()
                return player.property_list[answer]

class sidebarGUI:
    '''FUTURE BLAINE:
    I have copied all the side panel stuff to this one GUI class but have not yet
    deleted the originals and made sure it works here.
    What I'm thinking is write an explicit tap() method, an explicit land() method,
    and explicit click() method, and then use the stuff from display_title_deeds and 
    display_actions and have it be more clean and explicitly tied to what action is occurring. 
    
    Advantages to all this under one class: critical boolean can be of more use.
    For example when a space is clicked while in critical section, could have it 
    not change anything in the sidebar. Just return/pass without doing anything.'''
    def __init__(gui, window: tk.Tk, width: int):
            
            gui.window = window
            gui.space = None
            gui.critical = False
            gui.width = width
            gui.multiplier = 1
            unit = (gui.width * 3) // 14
            gui.unit = unit
            row1=10
            row2=10
            col1=11
            col2=13

            global player_list, turn_count
            gui.player = player_list.pop(0)
            player_list.append(gui.player)

            for p in player_list:
                def trade_placeholder(event, p=p):
                    return gui.trade(p)
                p.gui.canvas.bind("<Button-1>", trade_placeholder)

            gui.pool = player("Collections", "car", 0)
            gui.pool.set_space_list(gui.player.space_list)
            print(gui.pool.name)

            button_color = "green"
            gui.upgrade_pressed = False # deprecated 

            gui.broke_flag = False
            gui.broke_amount = 0
            gui.broke_owner = None
            gui.broke_text = tk.Label(window, text="", justify='center', font=("Bahnschrift Light", unit), fg="red", anchor=tk.S)
            gui.broke_text.grid(row=8, column=11, columnspan=2, sticky="s")
            gui.bankrupt_button = tk.Button(window, width=9, height=1, text="BANKRUPT", font=("Bahnschrift SemiBold", unit), command=lambda: gui.bankrupt(), bg="red", fg="white", bd=0, highlightthickness=0, activebackground="red4", activeforeground="white")

            gui.auction_text = tk.Label(window, text="", justify='center', font=("Bahnschrift Light", unit*2), fg="red", anchor=tk.S)
            gui.auction_total = 0
            gui.auction_player = None
            gui.auction_list = None
            gui.auction_property = None
            gui.auction_critical = tk.BooleanVar(master=gui.window,value=False)

            gui.buy_button = tk.Button(window, width=9, height=1, text="BUY", font=("Bahnschrift SemiBold", unit), command=lambda: gui.buy(), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.auction_button = tk.Button(window, width=9, height=1, text="AUCTION", font=("Bahnschrift SemiBold", unit), command=lambda: gui.auction(), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.draw_button = tk.Button(window, width=9, height=1, text="DRAW", font=("Bahnschrift SemiBold", unit), command=lambda: gui.draw(), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.upgrade_button = tk.Button(window, width=9,height=1, text="UPGRADE", font=("Bahnschrift SemiBold", unit), command=lambda: gui.upgrade(), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.mortgage_button = tk.Button(window, width=9,height=1, text="MORTGAGE", font=("Bahnschrift SemiBold", unit), command=lambda: gui.mortgage(), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.unmortgage_button = tk.Button(window, width=9,height=1, text="UNMORT.", font=("Bahnschrift SemiBold", unit), command=lambda: gui.unmortgage(), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.bail_button = tk.Button(window, width=9, height=1, text="PAY $50", font=("Bahnschrift SemiBold", unit), command=lambda: gui.bail(), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.use_card_button = tk.Button(window, width=9, height=1, text="USE CARD", font=("Bahnschrift SemiBold", unit), command=lambda: gui.use_card(), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.buy_house_button = tk.Button(window, width=9, height=1, text=emoji.emojize("BUY :house:"), font=("Bahnschrift SemiBold", unit), command=lambda: gui.buy_house(), bg="green", fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.sell_house_button = tk.Button(window, width=9, height=1, text=emoji.emojize("SELL :house:"), font=("Bahnschrift SemiBold", unit), command=lambda: gui.sell_house(), bg="green", fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.pay_button = tk.Button(window, width=9, height=1, text="PAY", font=("Bahnschrift SemiBold", unit), command=lambda: gui.pay(), bg="red4", fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white", state='disabled')

            gui.bid1 = tk.Button(window, width=9, height=1, text="BID $1", font=("Bahnschrift SemiBold", unit), command=lambda: gui.bid(1), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.bid10 = tk.Button(window, width=9, height=1, text="BID $10", font=("Bahnschrift SemiBold", unit), command=lambda: gui.bid(10), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.bid100 = tk.Button(window, width=9, height=1, text="BID $100", font=("Bahnschrift SemiBold", unit), command=lambda: gui.bid(100), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            gui.withdraw_button = tk.Button(window, width=9, height=1, text="WITHDRAW", font=("Bahnschrift SemiBold", unit), command=lambda: gui.withdraw(), bg=button_color, fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")


            gui.deed_canvas = tk.Canvas()
            gui.under_canvas = tk.Canvas()

            gui.roll_button = tk.Button(gui.window, width=6, height=1, text="ROLL", font=("Bahnschrift SemiBold", width//3), command=lambda: gui.roll(), bg="red", fg="white", bd=0, highlightthickness=0, activebackground="red", activeforeground="white")
            gui.roll_button.grid(row=10,column=12)

            gui.button_list = [gui.buy_button, 
                               gui.auction_button, 
                               gui.draw_button, 
                               gui.upgrade_button, 
                               gui.mortgage_button, 
                               gui.unmortgage_button,
                               gui.bail_button, 
                               gui.use_card_button,
                               gui.buy_house_button, 
                               gui.sell_house_button,
                               gui.pay_button]

            gui.dice1 = tk.Canvas(window, width=width, height=width, bd=0, highlightthickness=0)
            gui.dice1.grid(row=row1, column=col1, sticky="e")

            gui.dice2 = tk.Canvas(window, width=width, height=width, bd=0, highlightthickness=0)
            gui.dice2.grid(row=row2, column=col2, sticky="w")

            size_tuple = (width*3//2,width*3//2)

            import1 = Image.open('roll1.png')
            resize1 = import1.resize(size_tuple)
            gui.roll1 = ImageTk.PhotoImage(resize1)

            import2 = Image.open('roll2.png')
            resize2 = import2.resize(size_tuple)
            gui.roll2 = ImageTk.PhotoImage(resize2)

            import3 = Image.open('roll3.png')
            resize3 = import3.resize(size_tuple)
            gui.roll3 = ImageTk.PhotoImage(resize3)

            import4 = Image.open('roll4.png')
            resize4 = import4.resize(size_tuple)
            gui.roll4 = ImageTk.PhotoImage(resize4)

            import5 = Image.open('roll5.png')
            resize5 = import5.resize(size_tuple)
            gui.roll5 = ImageTk.PhotoImage(resize5)

            import6 = Image.open('roll6.png')
            resize6 = import6.resize(size_tuple)
            gui.roll6 = ImageTk.PhotoImage(resize6)

            gui.dice_images = [gui.roll1, gui.roll2, gui.roll3, gui.roll4, gui.roll5, gui.roll6]

            gui.dice_one = random.randint(1,6)
            gui.dice_two = random.randint(1,6)

            gui.dice1_image = gui.dice1.create_image(width//2,width//2,image=gui.dice_images[gui.dice_one-1])
            gui.dice2_image = gui.dice2.create_image(width//2,width//2,image=gui.dice_images[gui.dice_two-1])

            with open('chance.json') as f:
                file = json.load(f)

            gui.chance_cards = file["Chance"]

            random.shuffle(gui.chance_cards)

            with open('community_chest.json') as f:
                file = json.load(f)

            gui.community_cards = file["Community Chest"]

            random.shuffle(gui.community_cards)
            
            

    def roll(self):
        if self.critical:
            return
        self.multiplier = 1
        global player_list, turn_count
        self.dice_one = random.randint(1,6)
        self.dice_two = random.randint(1,6)

        self.dice1.itemconfig(self.dice1_image, image=self.dice_images[self.dice_one-1])
        self.dice2.itemconfig(self.dice2_image, image=self.dice_images[self.dice_two-1])

        print(self.player.name + " rolls " + str(self.dice_one + self.dice_two))

        self.dice1.update()
        
        self.roll_button.config(state='disabled')

        #self.critical = True
        time.sleep(1)
        self.player.move(self.dice_one, self.dice_two)
        #self.critical = False # This seems sus
        if self.critical or self.broke_flag:
            set_state = 'disabled'
        else:
            set_state = 'normal'

        jail_roll = (self.player.jail_sentence > 0)
        
        if (self.dice_one == self.dice_two and not jail_roll):
            self.roll_button.config(state=set_state)
        else:
            self.roll_button.config(state=set_state, text="DONE", command=lambda: self.done())

    def done(gui):
        if gui.critical:
            return
        global player_list, turn_count
        gui.player.gui.highlight(False)
        #turn_count += 1
        gui.player = player_list.pop(0)
        player_list.append(gui.player)
        gui.player.gui.highlight()
        for b in gui.button_list:
            b.grid_forget()
        if gui.player.jail_sentence > 0:
            gui.bail_button.grid(row=9,column=12)
        gui.roll_button.config(text="ROLL", command=lambda:gui.roll(), state='active')

        print("It is " + gui.player.name + "'s turn.")

        gui.render_buttons()

        # for p in player_list:
        #     print("\n" + p.name)
        #     for prop in p.property_list:
        #         print(prop.name)

    def click(gui, event: tk.Event):
        if gui.critical:
            return
        else:
            gui.space = event.widget
            gui.display_title_deed()
            # gui.upgrade_pressed = False # deprecated
            gui.render_buttons()

    def tap(gui, event: tk.Event):
        gui.space = event.widget
        gui.display_title_deed()

        if gui.space.property.type == "GO":
            gui.player.collect(gui.space.property.pay)

    def land(gui, event: tk.Event):

        gui.space = event.widget

        print(gui.player.name + " lands on " + gui.space.property.name)

        for b in gui.button_list:
            b.grid_forget()

        buyable = (gui.space.property.type == "COLOR" or gui.space.property.type == "RAILROAD" or gui.space.property.type == "UTILITY")

        # LAND ON OWN SPACE
        gui.render_buttons()

        # LAND ON ANOTHER PLAYER'S SPACE
        if buyable and gui.space.property not in gui.player.property_list and gui.space.property.owned():
            amount = gui.space.property.get_rent(dice_roll=gui.dice_one+gui.dice_two, multiplier=gui.multiplier)
            owner = gui.space.property.owner
            try:
                gui.player.pay(amount)
            except InsufficientFunds:
                gui.broke_protocol(amount, owner)
            else:
                print(gui.player.name + " pays " + owner.name + " $" + str(amount))
                owner.collect(amount)

        # LAND ON TAX SPACE        
        if type(gui.space) == otherGUI and (gui.space.property.type == "TAX"):
            try:
                gui.player.pay(gui.space.property.amount)
            except InsufficientFunds:
                gui.broke_protocol(gui.space.property.amount, gui.pool)
            else:
                gui.pool.collect(gui.space.property.amount)

        # LAND ON DRAW SPACE
        if type(gui.space) == otherGUI and (gui.space.property.type == "DRAW"):
            gui.draw_button.grid(row=9,column=12)
            gui.critical = True
            gui.roll_button.configure(state='disabled')

        # LAND ON FREE PARKING
        if gui.space.property.type == "FREE" and gui.space.property.house_rule:
            payout = gui.pool.balance.get()
            gui.pool.pay(payout)
            gui.player.collect(payout)
            
        # LAND ON UNOWNED SPACE (BUY OPPORTUNITY):
        if buyable and not gui.space.property.owned():
            if gui.player.balance.get() > gui.space.property.price:
                gui.buy_button.grid(row=9, column=12)
            gui.auction_button.grid(row=9, column=13, sticky="w")
            gui.critical = True
            gui.roll_button.configure(state='disabled')

        # LAND ON GO TO JAIL
        if gui.space.property.type == "GOTOJAIL":
            jail_coord = 10
            target = jail_coord
            gui.player.jail_sentence += 3
            gui.player.teleport(target)

        # LAND ON JAIL WHEN JAILED
        if gui.space.property.type == "JAIL" and gui.player.jail_sentence > 0:
            gui.bail_button.grid(row=9,column=12)

    def buy(gui):
        gui.player.add_property(gui.space.property)
        gui.critical = False
        gui.roll_button.configure(state='normal')
        gui.render_buttons()

    def auction(gui, auction_property=None):

        gui.auction_critical.set(True)

        if (auction_property is None):
            gui.auction_property = gui.space.property
        else:
            gui.auction_property = auction_property

        print(gui.auction_property.name + " is up for AUCTION.")


        for b in gui.button_list:
            b.grid_forget()

        global player_list
        gui.auction_list = player_list[:]
        gui.auction_player = gui.auction_list.pop(0)
        gui.auction_list.append(gui.auction_player)
        gui.auction_player.gui.auction_highlight()

        state1 = 'normal'
        state10 = 'normal'
        state100 = 'normal'

        if gui.auction_player.balance.get() < (1 + gui.auction_total):
            state1 = 'disabled'
        if gui.auction_player.balance.get() < (10 + gui.auction_total):
            state10 = 'disabled'
        if gui.auction_player.balance.get() < (100 + gui.auction_total):
            state100 = 'disabled'

        gui.bid1.config(state=state1)
        gui.bid10.config(state=state10)
        gui.bid100.config(state=state100)

        gui.bid1.grid(row=9, column=11)
        gui.bid10.grid(row=9, column=12)
        gui.bid100.grid(row=9, column=13)
        gui.withdraw_button.grid(row=8, column=13, sticky="sw")
        gui.auction_text.grid(row=8, column=11, columnspan=2, sticky="s")

        gui.auction_total = 10

        gui.auction_text.config(text=("$" + str(gui.auction_total)))

    def bid(gui, amount: int):
        
        gui.auction_total += amount
        gui.auction_text.config(text=("$" + str(gui.auction_total)))

        print(gui.auction_player.name + " bids $" + str(amount))

        gui.auction_player.gui.auction_highlight(False)
        if (gui.auction_player is gui.player):
            gui.player.gui.highlight()
        gui.auction_player = gui.auction_list.pop(0)
        gui.auction_list.append(gui.auction_player)
        gui.auction_player.gui.auction_highlight()

        state1 = 'normal'
        state10 = 'normal'
        state100 = 'normal'

        if gui.auction_player.balance.get() < (1 + gui.auction_total):
            state1 = 'disabled'
        if gui.auction_player.balance.get() < (10 + gui.auction_total):
            state10 = 'disabled'
        if gui.auction_player.balance.get() < (100 + gui.auction_total):
            state100 = 'disabled'

        gui.bid1.config(state=state1)
        gui.bid10.config(state=state10)
        gui.bid100.config(state=state100)

    def withdraw(gui):
        gui.auction_list.remove(gui.auction_player)
        gui.auction_player.gui.auction_highlight(False)
        if (gui.auction_player is gui.player):
            gui.player.gui.highlight()
        print(gui.auction_player.name + " withdraws from the auction.")
        gui.auction_player = gui.auction_list.pop(0)
        gui.auction_list.append(gui.auction_player)

        if (len(gui.auction_list) == 1):
            gui.auction_player.add_property(gui.auction_property, buy=False, amount=gui.auction_total)
            gui.auction_player = None
            gui.auction_property = None
            gui.auction_text.config(text="")
            gui.auction_text.grid_forget()
            gui.bid1.grid_forget()
            gui.bid10.grid_forget()
            gui.bid100.grid_forget()
            gui.withdraw_button.grid_forget()
            gui.auction_list = None
            gui.auction_total = 0
            gui.auction_critical.set(False)
            gui.critical = False
            gui.roll_button.configure(state='normal')
            gui.render_buttons()
            gui.display_title_deed()
        else:
            gui.auction_player.gui.auction_highlight()

            state1 = 'normal'
            state10 = 'normal'
            state100 = 'normal'

            if gui.auction_player.balance.get() < (1 + gui.auction_total):
                state1 = 'disabled'
            if gui.auction_player.balance.get() < (10 + gui.auction_total):
                state10 = 'disabled'
            if gui.auction_player.balance.get() < (100 + gui.auction_total):
                state100 = 'disabled'

            gui.bid1.config(state=state1)
            gui.bid10.config(state=state10)
            gui.bid100.config(state=state100)


    def trade(gui, target_player: player):
        if gui.critical:
            return
        gui.critical = True

        select_bg_color = "white"
        select_fg_color = "black"
        listbox_height = max(len(target_player.property_list)+target_player.free_cards+2, len(gui.player.property_list)+gui.player.free_cards+2)
        listbox_width = 20 # length of 'Get Out of Jail Free" + 1

        if target_player is gui.player:
            properties_window = tk.Tk()
            properties_window.title(gui.player.name)
            properties_window.attributes('-toolwindow', True)

            name_label = tk.Label(properties_window, text=gui.player.name, font=("Bahnschrift Semibold Condensed", gui.unit*2))
            name_label.grid(row=0, column=0)

            assets_label = tk.Label(properties_window, text="ASSETS", font=("Bahnschrift Semibold", gui.unit))
            assets_label.grid(row=1, column=0)
            
            assets = tk.Listbox(properties_window, selectmode=tk.SINGLE, activestyle='none', selectbackground=select_bg_color, selectforeground=select_fg_color, font=("Bahnschrift Semibold", gui.unit), highlightthickness=0, height=len(gui.player.property_list)+gui.player.free_cards+2)
            assets.grid(row=2, column=0)

            for p in gui.player.property_list:
                assets.insert(tk.END, p.name)
            
            for i in range(gui.player.free_cards):
                assets.insert(tk.END, "Get Out Of Jail Free")

            gui.color_highlight(assets)

            def on_closing():
                gui.critical = False
                properties_window.destroy()
            properties_window.protocol("WM_DELETE_WINDOW", on_closing)

            return          


        trade_window = tk.Tk()
        trade_window.title("Trade with " + target_player.name)

        def initiate_trade():
            if trader_offer.size() == 0 and target_offer.size() == 0:
                return
            trader_label.config(background="SystemButtonFace")
            target_label.config(background="red")
            # this would be where it switches control to target player for them to accept or decline
            initiate_trade_button.grid_forget()

            trader_assets.unbind("<Button-1>")
            trader_assets.unbind("<ButtonRelease-1>")
            trader_offer.unbind("<Button-1>")
            trader_offer.unbind("<ButtonRelease-1>")            
            target_assets.unbind("<Button-1>")
            target_assets.unbind("<ButtonRelease-1>")
            target_offer.unbind("<Button-1>")
            target_offer.unbind("<ButtonRelease-1>")

            def accept_trade():
                
                for i in range(trader_offer.size()):
                    property_string = trader_offer.get(i)
                    if ("$" in property_string):
                        amount = int(property_string[1:])
                        gui.player.pay(amount)
                        target_player.collect(amount)
                    elif (property_string == "Get Out Of Jail Free"):
                        gui.player.free_cards -= 1
                        target_player.free_cards =+ 1
                    else:
                        property = gui.player.remove_property(property_string)
                        target_player.add_property(property, buy=False)

                for i in range(target_offer.size()):
                    property_string = target_offer.get(i)
                    if ("$" in property_string):
                        amount = int(property_string[1:])
                        target_player.pay(amount)
                        gui.player.collect(amount)
                    elif (property_string == "Get Out Of Jail Free"):
                        target_player.free_cards -= 1
                        gui.player.free_cards =+ 1
                    else:
                        property_string = target_offer.get(i)
                        property = target_player.remove_property(property_string)
                        gui.player.add_property(property, buy=False)

                on_closing()

            accept_button = tk.Button(trade_window, width=10, height=2, text="ACCEPT", font=("Bahnschrift SemiBold", gui.unit), command=accept_trade, bg="green", fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
            accept_button.grid(row=2,column=2)

            def decline_trade():

                on_closing()

            decline_button = tk.Button(trade_window, width=10, height=2, text="DECLINE", font=("Bahnschrift SemiBold", gui.unit), command=decline_trade, bg="red", fg="white", bd=0, highlightthickness=0, activebackground="red4", activeforeground="white")
            decline_button.grid(row=3,column=2)


        initiate_trade_button = tk.Button(trade_window, width=10, height=2, text="INITIATE\nTRADE", font=("Bahnschrift SemiBold", gui.unit), command=lambda: initiate_trade(), bg="green", fg="white", bd=0, highlightthickness=0, activebackground="dark green", activeforeground="white")
        initiate_trade_button.grid(row=2, column=2)

        trader_label = tk.Label(trade_window, text=gui.player.name, font=("Bahnschrift Semibold Condensed", gui.unit*2), background="red")
        trader_label.grid(row=0, column=0)

        trader_assets_label = tk.Label(trade_window, text="ASSETS", font=("Bahnschrift Semibold", gui.unit))
        trader_assets_label.grid(row=1, column=0)
        
        trader_assets = tk.Listbox(trade_window, selectmode=tk.SINGLE, activestyle='none', selectbackground=select_bg_color, selectforeground=select_fg_color, font=("Bahnschrift Semibold", gui.unit), highlightthickness=0, height=listbox_height, width=listbox_width)
        trader_assets.grid(row=2, column=0, rowspan=3)

        for p in gui.player.property_list:
            if p.type != "COLOR" or (p.type == "COLOR" and p.num_houses == 0):
                trader_assets.insert(tk.END, p.name)
        
        for i in range(gui.player.free_cards):
            trader_assets.insert(tk.END, "Get Out Of Jail Free")

        trader_assets.insert(tk.END, ("$"+str(gui.player.balance.get())))

        trader_offer_label = tk.Label(trade_window, text="OFFER", font=("Bahnschrift Semibold", gui.unit))
        trader_offer_label.grid(row=1, column=1)

        trader_offer = tk.Listbox(trade_window, selectmode=tk.SINGLE, activestyle='none', selectbackground=select_bg_color, selectforeground=select_fg_color, font=("Bahnschrift Semibold", gui.unit), highlightthickness=0, height=listbox_height, width=listbox_width)
        trader_offer.grid(row=2, column=1, rowspan=3)

        def button_release(event):
            global hold_press_flag
            hold_press_flag = False

        def trader_assets_bind(event: tk.Event, trader_offer=trader_offer):
            global hold_press_flag, delay_int
            hold_press_flag = True
            delay_int = 200
            listbox = event.widget
            index = listbox.nearest(event.y)
            gui.trade_add(index, listbox, trader_offer)
        trader_assets.bind("<ButtonPress-1>", trader_assets_bind)
        trader_assets.bind("<ButtonRelease-1>", button_release)

        def trader_offer_bind(event: tk.Event, trader_assets=trader_assets):
            global hold_press_flag, delay_int
            hold_press_flag = True
            delay_int = 200
            listbox = event.widget
            index = listbox.nearest(event.y)
            gui.trade_add(index, listbox, trader_assets)
        trader_offer.bind("<ButtonPress-1>", trader_offer_bind)
        trader_offer.bind("<ButtonRelease-1>", button_release)

        target_label = tk.Label(trade_window, text=target_player.name, font=("Bahnschrift Semibold Condensed", gui.unit*2))
        target_label.grid(row=0, column=4)

        target_assets_label = tk.Label(trade_window, text="ASSETS", font=("Bahnschrift Semibold", gui.unit))
        target_assets_label.grid(row=1, column=4)
        
        target_assets = tk.Listbox(trade_window, selectmode=tk.SINGLE, activestyle='none', selectbackground=select_bg_color, selectforeground=select_fg_color, font=("Bahnschrift Semibold", gui.unit), highlightthickness=0, height=listbox_height, width=listbox_width)
        target_assets.grid(row=2, column=4, rowspan=3)

        for p in target_player.property_list:
            if p.type != "COLOR" or (p.type == "COLOR" and p.num_houses == 0):
                target_assets.insert(tk.END, p.name)

        for i in range(target_player.free_cards):
            target_assets.insert(tk.END, "Get Out Of Jail Free")

        target_assets.insert(tk.END, ("$"+str(target_player.balance.get())))

        target_offer_label = tk.Label(trade_window, text="OFFER", font=("Bahnschrift Semibold", gui.unit))
        target_offer_label.grid(row=1, column=3)

        target_offer = tk.Listbox(trade_window, selectmode=tk.SINGLE, activestyle='none', selectbackground=select_bg_color, selectforeground=select_fg_color, font=("Bahnschrift Semibold", gui.unit), highlightthickness=0, height=listbox_height, width=listbox_width)
        target_offer.grid(row=2, column=3, rowspan=3)

        gui.color_highlight(trader_assets)
        gui.color_highlight(trader_offer)
        gui.color_highlight(target_assets)
        gui.color_highlight(target_offer)
        
        def target_assets_bind(event: tk.Event, target_offer=target_offer):
            global hold_press_flag, delay_int
            hold_press_flag = True
            delay_int = 200
            listbox = event.widget
            index = listbox.nearest(event.y)
            gui.trade_add(index, listbox, target_offer)
        target_assets.bind("<ButtonPress-1>", target_assets_bind)
        target_assets.bind("<ButtonRelease-1>", button_release)

        def target_offer_bind(event: tk.Event, target_assets=target_assets):
            global hold_press_flag, delay_int
            hold_press_flag = True
            delay_int = 200
            listbox = event.widget
            index = listbox.nearest(event.y)
            gui.trade_add(index, listbox, target_assets)
        target_offer.bind("<ButtonPress-1>", target_offer_bind)
        target_offer.bind("<ButtonRelease-1>", button_release) 

        def on_closing():
            gui.critical = False
            trade_window.destroy()
        trade_window.protocol("WM_DELETE_WINDOW", on_closing)

        trade_window.mainloop()

    def trade_add(gui, index: int, source_listbox: tk.Listbox, dest_listbox: tk.Listbox, button=None):
        item = source_listbox.get(index)
        if "$" in item:
            global hold_press_flag, delay_int
            if hold_press_flag:
                if delay_int > 5:
                    delay_int -= 5
                amount_num = int(item[1:])
                source_listbox.delete(index)
                if (amount_num-1>0):
                    amount_str = "$"+str(amount_num-1)
                    source_listbox.insert(index, amount_str)
                dest_amount_index = tk.END
                dest_amount = 0
                for i in range(dest_listbox.size()):
                    if "$" in dest_listbox.get(i):
                        dest_amount_index = i
                        dest_amount = int(dest_listbox.get(i)[1:])
                        break
                if dest_amount_index != tk.END:
                    dest_listbox.delete(dest_amount_index)
                dest_listbox.insert(dest_amount_index, ("$"+str(dest_amount+1)))
                if hold_press_flag:
                    gui.window.after(delay_int,gui.trade_add,index,source_listbox,dest_listbox)
        else:
            source_listbox.delete(index)
            dest_listbox.insert(tk.END, item)
            #source_listbox.after(100, source_listbox.selection_clear(tk.ACTIVE))
            gui.color_highlight(source_listbox)
            gui.color_highlight(dest_listbox)

    def color_highlight(gui, listbox: tk.Listbox):
        color_map = {
            "Mediterranean Avenue": "brown",
            "Baltic Avenue": "brown",
            "Reading Railroad": "black",
            "Oriental Avenue": "teal",
            "Vermont Avenue": "teal",
            "Connecticut Avenue": "teal",
            "St. Charles Place": "pink",
            "Electric Company": "white",
            "States Avenue": "pink",
            "Virginia Avenue": "pink",
            "Pennsylvania Railroad": "black",
            "St. James Place": "orange",
            "Tennessee Avenue": "orange",
            "New York Avenue": "orange",
            "Kentucky Avenue": "red",
            "Indiana Avenue": "red",
            "Illinois Avenue": "red",
            "B & O Railroad": "black",
            "Atlantic Avenue": "yellow",
            "Ventnor Avenue": "yellow",
            "Water Works": "white",
            "Marvin Gardens": "yellow",
            "Pacific Avenue": "green",
            "North Carolina Avenue": "green",
            "Pennsylvania Avenue": "green",
            "Short Line": "black",
            "Park Place": "navy",
            "Boardwalk": "navy",
            "Get Out Of Jail Free": "white",
            "$": "white",
            "": "white"
        }
        for i in range(listbox.size()):
            item = listbox.get(i)
            if "$" in item:
                item = "$"
            bg_color = color_map[item]
            if (bg_color == "pink" or bg_color == "yellow" or bg_color == "white"):
                fg_color = "black"
            else:
                fg_color = "white"
            listbox.itemconfig(i,background=bg_color,selectbackground=bg_color,foreground=fg_color,selectforeground=fg_color)


    def mortgage(gui):
        gui.space.property.mortgaged = True
        gui.space.mortgage()
        print(gui.player.name + " mortgages " + gui.space.property.name)
        gui.player.collect(gui.space.property.mortgage_price)

        gui.render_buttons()
        gui.display_title_deed()

    def unmortgage(gui):
        gui.space.property.mortgaged = False
        gui.space.unmortgage()
        print(gui.player.name + " unmortgages " + gui.space.property.name)
        gui.player.pay(int(gui.space.property.mortgage_price*1.10))

        gui.render_buttons()
        gui.display_title_deed()        

    # deprecated 
    def upgrade(gui):
        if not gui.upgrade_pressed:
            gui.buy_house_button.grid(row=9,column=11, sticky="e")
            gui.sell_house_button.grid(row=9,column=12)
            gui.upgrade_button.config(bg="dark green")
            gui.upgrade_pressed = True
        else:
            gui.buy_house_button.grid_forget()
            gui.sell_house_button.grid_forget()
            gui.upgrade_button.config(bg="green")
            gui.upgrade_pressed = False

    def buy_house(gui):
        print(gui.player.name + " buys a house on " + gui.space.property.name)
        gui.player.pay(gui.space.property.upgrade)
        gui.space.property.num_houses += 1
        gui.space.add_house()

        gui.render_buttons()

    def sell_house(gui):
        print(gui.player.name + " sells a house on " + gui.space.property.name)
        gui.player.collect(gui.space.property.upgrade//2)
        gui.space.property.num_houses -= 1
        gui.space.remove_house()

        gui.render_buttons()

    def bail(gui): # this might be wonky with the try/except
        gui.render_buttons()
        try:
            gui.player.pay(gui.space.property.fine)
        except InsufficientFunds:
            gui.broke_protocol(gui.space.property.fine, gui.pool)
        finally:
            gui.pool.collect(gui.space.property.fine)
            gui.player.jail_sentence = 0
            gui.space.remove_piece(gui.player)
            gui.space.put_piece(gui.player)

    def use_card(gui):
        gui.player.free_cards -= 1
        gui.player.jail_sentence = 0
        gui.space.remove_piece(gui.player)
        gui.space.put_piece(gui.player)
        gui.render_buttons()

    def pay(gui): # for when player sells/mortgages properties to be able to pay rent
        gui.player.pay(gui.broke_amount)
        print(gui.player.name + " pays " + gui.broke_owner.name + " $" + str(gui.broke_amount))
        gui.broke_owner.collect(gui.broke_amount)
        gui.broke_flag = False
        gui.broke_amount = 0
        gui.broke_owner = None
        gui.broke_text.config(text="")
        gui.roll_button.config(state='normal')
        gui.pay_button.config(bg="red4",state='disabled')
        gui.pay_button.grid_forget()
        gui.bankrupt_button.grid_forget()

    def draw(gui):

        if gui.space.tile_name == "Community Chest":
            card = gui.community_cards.pop()
            gui.community_cards.insert(0, card)
        if gui.space.tile_name == "Chance":
            card = gui.chance_cards.pop()
            gui.chance_cards.insert(0, card)

        card_text = card["text"]
        card_type = card["type"]
        card_target = card["target"]
        card_amount = card["amount"]

        gui.draw_button.configure(text="OKAY", command=lambda: gui.execute_draw(card_type, card_target, card_amount))

        print(gui.player.name + " draws \"" + card_text + "\"")

        unit = gui.space.width + gui.space.height
        width = unit * 1.5
        height = unit * 2

        other_gui = otherGUI(card_text, gui.window, width=width,height=height)
        other_gui.grid(row=0, column=11, rowspan=5, columnspan=3)
        other_gui.edit_text(card_text)

    def execute_draw(gui, card_type, card_target, card_amount):

        gui.critical = False
        gui.draw_button.configure(text="DRAW", command=lambda: gui.draw())
        gui.draw_button.grid_forget()
        gui.roll_button.configure(state='normal')

        global player_list

        match card_type:
            case "ADVANCE":
                if card_target == "RAILROAD" or card_target == "UTILITY":
                    gui.multiplier=2
                    for i in range(gui.player.position, gui.player.position+40):
                        p = i%40
                        if (gui.player.space_list[p].property.type == card_target):
                            target = gui.player.space_list[p].position
                            break
                else:
                    for s in gui.player.space_list:
                        if s.tile_name == card_target:
                            target = s.position
                            break

                if (gui.player.position < target):
                    distance = target - gui.player.position
                else:
                    distance = (target + 40) - gui.player.position
                gui.player.move(distance,0)
            case "BACK":
                target = (gui.player.position - card_amount) % 40
                gui.player.teleport(target)
            case "JAIL":
                jail_coord = 10
                target = jail_coord
                gui.player.jail_sentence += 3
                gui.player.teleport(target)
            case "FREE":
                gui.player.free_cards += 1
            case "RECEIVE":
                if card_target == "BANK":
                    gui.player.collect(card_amount)
                if card_target == "PLAYERS":
                    for p in player_list:
                        if p is gui.player:
                            continue
                        p.pay(card_amount) # idk how to bankrupt-proof this
                        gui.player.collect(card_amount)
            case "PAY":
                if card_target == "BANK":
                    try:
                        gui.player.pay(card_amount)
                    except InsufficientFunds:
                        gui.broke_protocol(card_amount, gui.pool)
                    else:
                        gui.pool.collect(card_amount)
                if card_target == "PLAYERS":
                    for p in player_list:
                        if p is gui.player:
                            continue
                        try:
                            gui.player.pay(card_amount)
                        except InsufficientFunds:
                            gui.broke_protocol(card_amount, p)
                        else:
                            p.collect(card_amount)
            case "REPAIR":
                house_cost = 0
                hotel_cost = 0
                if card_amount == 100:
                    house_cost = 25
                    hotel_cost = 100
                if card_amount == 115:
                    house_cost = 40
                    hotel_cost = 115
                total_houses = 0
                total_hotels = 0
                for prop in gui.player.property_list:
                    if prop.type == "COLOR":
                        if prop.num_houses == 5:
                            total_hotels += 1
                        else:
                            total_houses += prop.num_houses
                total_cost = (total_hotels * hotel_cost) + (total_houses * house_cost)
                try:
                    gui.player.pay(total_cost)
                except InsufficientFunds:
                    gui.broke_protocol(total_cost, gui.pool)
                else:
                    gui.pool.collect(total_cost)
                

    def render_buttons(gui):
        for b in gui.button_list:
            b.grid_forget()

        if gui.broke_flag:
            gui.pay_button.grid(row=9,column=13)
            if gui.player.balance.get() > gui.broke_amount:
                gui.pay_button.config(bg="green", state='normal')
        
        if gui.space.property in gui.player.property_list:
            if (gui.space.property.type == "COLOR"):
                if (gui.space.property.monopoly_flag 
                    and gui.space.property.num_houses > 0
                    and gui.player.house_check(gui.space.property, "sell")):
                    gui.sell_house_button.grid(row=9, column=12)
                elif(gui.space.property.num_houses == 0):
                    if not gui.space.property.mortgaged:
                        gui.mortgage_button.grid(row=9, column=12)
                    else:
                        gui.unmortgage_button.grid(row=9, column=12) 
                if (gui.space.property.monopoly_flag 
                    and not gui.space.property.mortgaged 
                    and gui.space.property.num_houses < 5
                    and gui.player.house_check(gui.space.property, "buy")):
                    gui.buy_house_button.grid(row=9,column=11, sticky="e")
            else:
                if not gui.space.property.mortgaged:
                    gui.mortgage_button.grid(row=9, column=12)
                else:
                    gui.unmortgage_button.grid(row=9, column=12) 

        if gui.space.property.type == "JAIL" and gui.player.jail_sentence > 0:
            gui.bail_button.grid(row=9,column=12)
            if gui.player.free_cards > 0:
                gui.use_card_button.grid(row=9, column=11)

    def display_title_deed(gui):
        #deed_window = tk.Tk()
        #deed_window.title(space.tile_name)
        #deed_window.geometry(f"+{event.x_root}+{event.y_root}")


        unit = gui.space.width + gui.space.height # far too late for this lol
        if type(gui.space) == colorGUI:
            color = gui.space.set_color
            if color == "yellow" or color == "magenta":
                text_color = "black"
            else:
                text_color = "white"
            justify = 'center'
        elif type(gui.space) == cornerGUI:
            unit = unit * .75
        else:
            color = "white"
            text_color = "black"
            justify = 'left'
        width = unit * 1.5
        height = unit * 2
        m = unit // 15
        m2 = m*2
        m0 = m // 2
        font_size = int(unit // 12)
        strip_height = font_size * 5

        gui.deed_canvas.grid_forget()
        gui.deed_canvas = tk.Canvas(gui.window, width=width+m, height=height, bd=0, highlightthickness=0)
        gui.deed_canvas.grid(row=0, column=11, rowspan=5, columnspan=3)

        gui.under_canvas.grid_forget()
        gui.under_canvas = tk.Canvas(gui.window, width=width+m, height=m*10, bd=0, highlightthickness=0)
        row = 5
        undertext = ""

        if type(gui.space) == cornerGUI:
            corner_gui = cornerGUI(gui.space.tile_text, gui.window, width=width, height=width)
            corner_gui.grid(row=0, column=11, rowspan=4, columnspan=3)
            row=4

            match gui.space.tile_name:
                case "GO":
                    undertext = ("Salary:\t$" + str(gui.space.property.pay))
                case "IN JAIL JUST VISITING":
                    undertext = ("Fine:\t$" + str(gui.space.property.fine))
                case "GO TO JAIL":
                    undertext = ("WEE WOO WEE WOO")
                case "FREE PARKING":
                    undertext = ("It's FREE!")

        elif gui.space.property.type == "DRAW" or gui.space.property.type == "TAX":
            other_gui = otherGUI(gui.space.tile_text, gui.window, width=width,height=height)
            other_gui.grid(row=0, column=11, rowspan=5, columnspan=3)

            if gui.space.property.type == "TAX":
                undertext = ("Tax:\t$" + str(gui.space.property.amount))

        else:

            #canvas.create_rectangle(0,0,width+10,height+10)
            gui.deed_canvas.create_rectangle(m0,m0,width,height-m,outline="black", width=1)
            gui.deed_canvas.create_rectangle(m,m,width-m0,strip_height-m0, fill=color, outline="black", width=3)
            gui.deed_canvas.create_text((width+m)//2,(strip_height//4)+(m0),text="T I T L E   D E E D", font=("Bahnschrift Semibold", int(font_size*.7)), fill=text_color)
            gui.deed_canvas.create_text((width+m)//2,((strip_height//5)*3)+(m0//2),text=gui.space.property.name.upper(), font=("Bahnschrift Semibold Condensed", int((font_size*1.5)//1)), fill=text_color)
            gui.deed_canvas.create_text((width+m)//2,(height//2)+strip_height//3,text=gui.space.property.get_detail(), justify=justify, font=("Bahnschrift Light", font_size), fill="black")

            undertext = ("Cost:\t$" + str(gui.space.property.price) +
                    "\nOwner:\t" + str(gui.space.property.owner) +
                    "\nMtg'd:\t" + str(gui.space.property.mortgaged))

        gui.under_canvas.grid(row=row, column=11, rowspan=2, columnspan=3)
        gui.under_canvas.create_text(m2, m2, text=undertext, anchor="nw", font=("Bahnschrift Light", font_size))

    def broke_protocol(gui, amount, owner):
        gui.roll_button.config(state='disabled')
        gui.broke_flag = True
        gui.broke_amount = amount
        gui.broke_owner = owner

        gui.broke_text.config(text=("You owe $" + str(amount) + "."))

        gui.pay_button.grid(row=9,column=13, sticky="w")
        gui.bankrupt_button.grid(row=8, column=13, sticky="sw")

    def bankrupt(gui):
        global player_list, turn_count # turn count might be deprecated
        player_list.remove(gui.player)

        remaining_balance = gui.player.balance.get()
        gui.player.pay(remaining_balance)
        gui.broke_owner.collect(remaining_balance)


        gui.bankrupt_button.grid_forget()
        gui.broke_text.config(text="")

        print("\033[1m\033[38;2;205;49;49m" + gui.player.name + " has gone bankrupt." + "\033[0m")

        gui.player.space_list[gui.player.position].remove_piece(gui.player)

        gui.player.gui.eliminate()
        
        if not (gui.broke_owner.name == "Collections") or len(player_list) == 1:

            if len(player_list) == 1:
                gui.broke_owner = player_list[0]

            for prop in gui.player.property_list:
                gui.broke_owner.add_property(prop, buy=False)

            gui.broke_owner.free_cards += gui.player.free_cards

        else:
            for prop in gui.player.property_list:
                prop.owner = None

            for prop in gui.player.property_list:
                gui.critical
                gui.space = prop.space
                gui.display_title_deed()
                # gui.auction_critical.set(True)
                gui.auction(prop)
                gui.window.wait_variable(gui.auction_critical)

        
        if (len(player_list) == 1):
            gui.critical = True
            print("\033[1m\033[38;2;35;209;139m" + "WINNER! " + player_list[0].name + " has won the game!" + "\033[0m")

        gui.broke_flag = False
        gui.broke_amount = 0
        gui.broke_owner = None

        gui.done()

class game:
    def __init__(self, window: tk.Tk, sidebar: sidebarGUI):
        self.window = window
        self.sidebar = sidebar

def main(player_list: list):
    with open('properties.json') as f:
        file = json.load(f)

    properties = file["properties"]

    tile_list = []

    railroad_list = properties["railroads"]
    utility_list = properties["utilities"]

    tile_list.append(go("GO", "GO", 200))

    i = 0
    rr = 0
    p = 0
    u = 0

    while i < 39:
        i = i+1
        prop =  properties["colors"][p]

        if i == 2 or i == 17 or i == 33:
            tile_list.append(draw("DRAW", "Community Chest"))
            continue
        if i == 7 or i == 22 or i == 36:
            tile_list.append(draw("DRAW", "Chance"))
            continue
        if i == 4:
            tile_list.append(tax("TAX", "Income Tax", 200))
            continue
        if i == 38:
            tile_list.append(tax("TAX", "Luxury Tax", 100))
            continue
        if i == 10:
            tile_list.append(jail("JAIL", "JAIL", 50))
            continue
        if i == 20:
            tile_list.append(free("FREE", "FREE PARKING", house_rule=True))
            continue
        if i == 30:
            tile_list.append(gotojail("GOTOJAIL", "GO TO JAIL"))
            continue
        if i == 12 or i == 28:
            u_prop = utility_list[u]
            u = u+1
            tile_list.append(utility(u_prop["type"], u_prop["name"], u_prop["price"], u_prop["mults"]))
            continue
        if i == 5 or i == 15 or i == 25 or i == 35:
            rr_prop = railroad_list[rr]
            rr = rr + 1
            tile_list.append(railroad(rr_prop["type"], rr_prop["name"], rr_prop["price"], rr_prop["rents"]))
            continue
        tile_list.append(color(prop["type"], prop["color"], prop["name"], prop["price"], prop["upgrade"], prop["rents"]))
        p = p+1

    # for tile in tile_list:
    #     print(tile)

    # for tile in tile_list:
    #     if tile.type == "COLOR" or tile.type == "RAILROAD" or tile.type == "UTILITY":
    #         tile.print_detail()



    # ''' TODO: Determine who goes first via dice roll '''

    # while len(player_list) > 1:
    #     for player in player_list:
    #         # Give player opportunity to review properties (buy houses or mortgage)
    #         if len(player.property_list) > 0:
    #             choice = review_properties(player)

    dice_one = 0
    dice_two = 0
                
    main_window = tk.Tk()
    main_window.title("Monopoly")

    tile_width = 45
    tile_height = tile_width*2

    spaces = []

    go_gui = cornerGUI("GO", main_window, width=tile_height, height=tile_height)
    go_gui.grid(row=10, column=10, padx=0, pady=0)
    spaces.append(go_gui)

    mediterranean_gui = colorGUI("brown", "bottom", "Mediter-\nranean\nAvenue", main_window, width=tile_width, height=tile_height)
    mediterranean_gui.grid(row=10, column=9, padx=0, pady=0)
    spaces.append(mediterranean_gui)

    community2_gui = otherGUI("Community\nChest", main_window, width=tile_width, height=tile_height)
    community2_gui.grid(row=10, column=8, padx=0, pady=0)
    spaces.append(community2_gui)

    baltic_gui = colorGUI("brown", "bottom", "Baltic\nAvenue", main_window, width=tile_width, height=tile_height)
    baltic_gui.grid(row=10, column=7, padx=0, pady=0)
    spaces.append(baltic_gui)

    income_gui = otherGUI("Income\nTax", main_window, width=tile_width, height=tile_height)
    income_gui.grid(row=10, column=6, padx=0, pady=0)
    spaces.append(income_gui)

    reading_gui = otherGUI("Reading\nRailroad", main_window, width=tile_width, height=tile_height)
    reading_gui.grid(row=10, column=5, padx=0, pady=0)
    spaces.append(reading_gui)

    oriental_gui = colorGUI("teal", "bottom", "Oriental\nAvenue", main_window, width=tile_width, height=tile_height)
    oriental_gui.grid(row=10, column=4, padx=0, pady=0)
    spaces.append(oriental_gui)

    chance3_gui = otherGUI("Chance", main_window, width=tile_width, height=tile_height)
    chance3_gui.grid(row=10, column=3, padx=0, pady=0)
    spaces.append(chance3_gui)

    vermont_gui = colorGUI("teal", "bottom", "Vermont\nAvenue", main_window, width=tile_width, height=tile_height)
    vermont_gui.grid(row=10, column=2, padx=0, pady=0)
    spaces.append(vermont_gui)

    connecticut_gui = colorGUI("teal", "bottom", "Connect-\nicut\nAvenue", main_window, width=tile_width, height=tile_height)
    connecticut_gui.grid(row=10, column=1, padx=0, pady=0)
    spaces.append(connecticut_gui)

    jail_gui = cornerGUI("IN JAIL\nJUST VISITING", main_window, width=tile_height, height=tile_height)
    jail_gui.grid(row=10, column=0, padx=0, pady=0)
    spaces.append(jail_gui)

    stcharles_gui = colorGUI("magenta", "left", "St. Charles\nPlace", main_window, width=tile_height, height=tile_width)
    stcharles_gui.grid(row=9, column=0, padx=0, pady=0)
    spaces.append(stcharles_gui)

    electric_gui = otherGUI("Electric\nCompany", main_window, width=tile_height, height=tile_width)
    electric_gui.grid(row=8, column=0, padx=0, pady=0)
    spaces.append(electric_gui)

    states_gui = colorGUI("magenta", "left", "States\nAvenue", main_window, width=tile_height, height=tile_width)
    states_gui.grid(row=7, column=0, padx=0, pady=0)
    spaces.append(states_gui)

    virginia_gui = colorGUI("magenta", "left", "Virginia\nAvenue", main_window, width=tile_height, height=tile_width)
    virginia_gui.grid(row=6, column=0, padx=0, pady=0)
    spaces.append(virginia_gui)

    pennrr_gui = otherGUI("Pennsylvania\nRailroad", main_window, width=tile_height, height=tile_width)
    pennrr_gui.grid(row=5, column=0, padx=0, pady=0)
    spaces.append(pennrr_gui)

    stjames_gui = colorGUI("orange", "left", "St. James\nPlace", main_window, width=tile_height, height=tile_width)
    stjames_gui.grid(row=4, column=0, padx=0, pady=0)
    spaces.append(stjames_gui)

    community3_gui = otherGUI("Community\nChest", main_window, width=tile_height, height=tile_width)
    community3_gui.grid(row=3, column=0, padx=0, pady=0)
    spaces.append(community3_gui)

    tennessee_gui = colorGUI("orange", "left", "Tennessee\nAvenue", main_window, width=tile_height, height=tile_width)
    tennessee_gui.grid(row=2, column=0, padx=0, pady=0)
    spaces.append(tennessee_gui)

    newyork_gui = colorGUI("orange", "left", "New York\nAvenue", main_window, width=tile_height, height=tile_width)
    newyork_gui.grid(row=1, column=0, padx=0, pady=0)
    spaces.append(newyork_gui)

    free_gui = cornerGUI("FREE PARKING", main_window, width=tile_height, height=tile_height)
    free_gui.grid(row=0, column=0, padx=0, pady=0)
    spaces.append(free_gui)

    kentucky_gui = colorGUI("red", "top", "Kentucky\nAvenue", main_window, width=tile_width, height=tile_height)
    kentucky_gui.grid(row=0, column=1, padx=0, pady=0)
    spaces.append(kentucky_gui)

    chance1_gui = otherGUI("Chance", main_window, width=tile_width, height=tile_height)
    chance1_gui.grid(row=0, column=2, padx=0, pady=0)
    spaces.append(chance1_gui)

    indiana_gui = colorGUI("red", "top", "Indiana\nAvenue", main_window, width=tile_width, height=tile_height)
    indiana_gui.grid(row=0, column=3, padx=0, pady=0)
    spaces.append(indiana_gui)

    illinois_gui = colorGUI("red", "top", "Illinois\nAvenue", main_window, width=tile_width, height=tile_height)
    illinois_gui.grid(row=0, column=4, padx=0, pady=0)
    spaces.append(illinois_gui)

    bando_gui = otherGUI("B & O\nRailroad", main_window, width=tile_width, height=tile_height)
    bando_gui.grid(row=0, column=5, padx=0, pady=0)
    spaces.append(bando_gui)

    atlantic_gui = colorGUI("yellow", "top", "Atlantic\nAvenue", main_window, width=tile_width, height=tile_height)
    atlantic_gui.grid(row=0, column=6, padx=0, pady=0)
    spaces.append(atlantic_gui)

    ventnor_gui = colorGUI("yellow", "top", "Ventnor\nAvenue", main_window, width=tile_width, height=tile_height)
    ventnor_gui.grid(row=0, column=7, padx=0, pady=0)
    spaces.append(ventnor_gui)

    water_gui = otherGUI("Water\nWorks", main_window, width=tile_width, height=tile_height)
    water_gui.grid(row=0, column=8, padx=0, pady=0)
    spaces.append(water_gui)

    marvin_gui = colorGUI("yellow", "top", "Marvin\nGardens", main_window, width=tile_width, height=tile_height)
    marvin_gui.grid(row=0, column=9, padx=0, pady=0)
    spaces.append(marvin_gui)

    gotojail_gui = cornerGUI("GO TO JAIL", main_window, width=tile_height, height=tile_height)
    gotojail_gui.grid(row=0, column=10, padx=0, pady=0)
    spaces.append(gotojail_gui)

    pacific_gui = colorGUI("green", "right", "Pacific\nAvenue", main_window, width=tile_height, height=tile_width)
    pacific_gui.grid(row=1, column=10, padx=0, pady=0)
    spaces.append(pacific_gui)

    northcarolina_gui = colorGUI("green", "right", "North Carolina\nAvenue", main_window, width=tile_height, height=tile_width)
    northcarolina_gui.grid(row=2, column=10, padx=0, pady=0)
    spaces.append(northcarolina_gui)

    community1_gui = otherGUI("Community\nChest", main_window, width=tile_height, height=tile_width)
    community1_gui.grid(row=3, column=10, padx=0, pady=0)
    spaces.append(community1_gui)

    pennsylvania_gui = colorGUI("green", "right", "Pennsylvania\nAvenue", main_window, width=tile_height, height=tile_width)
    pennsylvania_gui.grid(row=4, column=10, padx=0, pady=0)
    spaces.append(pennsylvania_gui)

    shortline_gui = otherGUI("Short Line", main_window, width=tile_height, height=tile_width)
    shortline_gui.grid(row=5, column=10, padx=0, pady=0)
    spaces.append(shortline_gui)

    chance2_gui = otherGUI("Chance", main_window, width=tile_height, height=tile_width)
    chance2_gui.grid(row=6, column=10, padx=0, pady=0)
    spaces.append(chance2_gui)

    parkplace_gui = colorGUI("navy", "right", "Park\nPlace", main_window, width=tile_height, height=tile_width)
    parkplace_gui.grid(row=7, column=10, padx=0, pady=0)
    spaces.append(parkplace_gui)

    luxury_gui = otherGUI("Luxury Tax", main_window, width=tile_height, height=tile_width)
    luxury_gui.grid(row=8, column=10, padx=0, pady=0)
    spaces.append(luxury_gui)

    boardwalk_gui = colorGUI("navy", "right", "Boardwalk", main_window, width=tile_height, height=tile_width)
    boardwalk_gui.grid(row=9, column=10, padx=0, pady=0)
    spaces.append(boardwalk_gui)

    monopoly_center = tk.Canvas(main_window, width=tile_width*5, height=tile_width, bd=0, highlightthickness=0)
    monopoly_center.grid(row=5, column=3, columnspan=5)
    monopoly_center.create_rectangle(0,0,tile_width*5,tile_width, fill="red", outline="black", width=5)
    monopoly_center.create_text(tile_width*2.5,tile_width//2,text="MONOPOLY", font=("Bahnschrift SemiBold", 28), fill="white")

    right_pane_canvas = tk.Canvas(main_window, width=(tile_width)*4.7, height=(tile_height), bd=0, highlightthickness=0)
    right_pane_canvas.grid(row=0,column=11,columnspan=3)

    bottom_pane_canvas = tk.Canvas(main_window, width=(tile_width)*17.7, height=tile_width//2, bd=0, highlightthickness=0, bg="light grey")
    bottom_pane_canvas.grid(row=11,column=0,columnspan=14)

    dice_spacing_canvas1 = tk.Canvas(main_window, width=((tile_width)*4.7)//3, height=tile_width//2, bd=0, highlightthickness=0)
    dice_spacing_canvas1.grid(row=10,column=11)
    dice_spacing_canvas2 = tk.Canvas(main_window, width=((tile_width)*4.7)//3, height=tile_width//2, bd=0, highlightthickness=0)
    dice_spacing_canvas2.grid(row=10,column=12)
    dice_spacing_canvas3 = tk.Canvas(main_window, width=((tile_width)*4.7)//3, height=tile_width//2, bd=0, highlightthickness=0)
    dice_spacing_canvas3.grid(row=10,column=13)

    # player_list = []
    # player_one = player(spaces, "Player One", "car", balance=1500)
    # player_two = player(spaces, "Player Two", "hat", balance=1500)
    # player_three = player(spaces, "Player Three", "iron", balance=1500)
    # player_four = player(spaces, "Player Four", "shoe", balance=1500)

    # player_list.append(player_one)
    # player_list.append(player_two)
    # player_list.append(player_three)
    # player_list.append(player_four)

    # num_players = input("How many players? ")

    # player_list = []

    for p in player_list:
        # print("For player " + str(p+1) + ": ")
        # name = input("Enter name: ")
        # piece = input("Choose piece: ")
        # Starting balance default $1500
        #player_list.append(player(spaces, name, piece, 1500))
        p.set_space_list(spaces)

    turn_count = 0

    i = 0
    for space in spaces:
        space.link_property(tile_list, i)
        i +=1

    i=0
    for p in player_list:
        spaces[0].put_piece(p)
        player_gui = playerGUI(p, main_window, tile_width*2, row=11, col=i)
        p.link_gui(player_gui)
        if i == 0:
            i +=1
        else:
            i += 2

    sidebar_gui = sidebarGUI(main_window, tile_width)
    #roll_button.bind("<ButtonRelease-1>", lambda event: dice_gui.toss())
    #roll_button.invoke()

    for i in range(10):
        main_window.grid_columnconfigure(i, pad=0)
        main_window.grid_rowconfigure(i, pad=0)

    i = 0
    for space in spaces:
        space.bind("<Button-1>", sidebar_gui.click)
        #space.bind("<Button-1>", sidebar_gui.display_actions)
        space.bind("<<Land>>", sidebar_gui.land)
        space.bind("<<Tap>>", sidebar_gui.tap)
        #space.bind("<<Land>>", sidebar_gui.display_actions)

        i += 1

    player_list[-1].gui.highlight()
    print("It is " + player_list[-1].name + "'s turn.")
    go_gui.event_generate("<<Land>>")

    # player_one.add_property(tile_list[11])
    # player_one.add_property(tile_list[13])
    # player_one.add_property(tile_list[14])
    # player_two.add_property(tile_list[16])
    # player_two.add_property(tile_list[18])
    # player_two.add_property(tile_list[19])
    # player_three.add_property(tile_list[21])
    # player_three.add_property(tile_list[23])
    # player_three.add_property(tile_list[24])
    # player_four.add_property(tile_list[26])
    # player_four.add_property(tile_list[27])
    # player_four.add_property(tile_list[29])



    main_window.mainloop()

    monopoly_game = game(main_window, sidebar_gui)
    return monopoly_game

if __name__ == "__main__":
    player_list = [
        player("Player One", "car", balance=1500),
        player("Player Two", "hat", balance=1500),
        player("Player Three", "iron", balance=1500),
        player("Player Four", "shoe", balance=1500)
    ]
    main(player_list)
