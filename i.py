import argparse

from prettytable import PrettyTable

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=False,
                help="path to the input file")
ap.add_argument("-i", "--interactive", required=False, type=bool, help="run program in interactive mode")
p_args = ap.parse_args()


class ParkingSpace:
    EMPTY_SPL_CHARACTER = "<E>"

    def __init__(self):
        self.slots: int = None
        self.spaces: list = None
        self.allocations: dict = dict()

    def create_parking_lot(self, n_slots: int):
        self.slots = n_slots
        self.spaces = [self.EMPTY_SPL_CHARACTER] * self.slots
        print(f'Created a parking lot with {n_slots} spaces')

    def park(self, *args):
        plate, color = args
        try:
            slot_number = self.spaces.index(self.EMPTY_SPL_CHARACTER)
        except ValueError:
            print("Parking full!")
            return
        self.spaces[slot_number] = 1
        if slot_number in self.allocations:
            raise RuntimeError(f"Slot already assigned: {self.allocations[slot_number]}")
        self.allocations[slot_number] = dict(plate=plate, color=color)
        print(f"Allotted slot number: {slot_number + 1}")

    def leave(self, slot_number: int):
        zero_indexed_slot_number = slot_number - 1
        if slot_number not in self.allocations:
            raise RuntimeError(f"Cannot leave an empty spot: {slot_number}")
        self.spaces[zero_indexed_slot_number] = self.EMPTY_SPL_CHARACTER
        del self.allocations[zero_indexed_slot_number]
        print(f"Slot number {slot_number} freed.")

    def status(self):
        table = PrettyTable(["Slot No.", "Registration No.", "Color"])
        list(map(lambda x: table.add_row([x[0] + 1, *x[1].values()]), sorted(self.allocations.items())))
        print(table)

    def get_slot_number_by_reg(self, reg):
        try:
            slot, deets = list(filter(lambda x: x[1]["plate"] == reg, self.allocations.items()))[0]
            print(slot + 1)
        except (ValueError, IndexError):
            print(f"Registration {reg} not found in parking spaces.")

    def get_slot_number_by_color(self, color, print_var):
        try:
            deets = filter(lambda x: x[1]["color"] == color, self.allocations.items())
            if print_var == "registration":
                print(" ,".join(d[1]["plate"] for d in deets))
            if print_var == "slots":
                print(" ,".join(str(d[0] + 1) for d in deets))
        except ValueError:
            print(f"No car with color: {color} found in parking spaces.")


space = ParkingSpace()

if not any(vars(p_args).values()):
    print("Invalid arguments / no arguments passed.")
    exit(0)

if p_args.file:
    try:
        cmd_file = open(p_args.file)
    except FileNotFoundError:
        print("File not found. Please check the path.")
        exit(0)

while True:
    if p_args.interactive:
        command = input().split()
    else:
        try:
            command = next(cmd_file).split()
        except StopIteration:
            break
    if command[0] == "park":
        space.park(*command[1:])
    elif command[0] == "leave":
        space.leave(int(command[1]))
    elif command[0] == "create_parking_lot":
        space.create_parking_lot(int(command[1]))
    elif command[0] == "status":
        space.status()
    elif command[0] == "registration_numbers_for_cars_with_colour":
        space.get_slot_number_by_color(command[1], print_var="registration")
    elif command[0] == "slot_numbers_for_cars_with_colour":
        space.get_slot_number_by_color(command[1], print_var="slots")
    elif command[0] == "slot_number_for_registration_number":
        space.get_slot_number_by_reg(command[1])
    elif command[0] == "exit":
        break
    else:
        print("Invalid Command. Try again")

'''
create_parking_lot 6
park KA-01-HH-1234 White
park KA-01-HH-9999 White
park KA-01-BB-0001 Black
park KA-01-HH-7777 Red
park KA-01-HH-2701 Blue
park KA-01-HH-3141 Black
leave 4
status
park KA-01-P-333 White
park DL-01-P-9999 White
registration_numbers_for_cars_with_colour White
slot_numbers_for_cars_with_colour White
slot_number_for_registration_number DL-01-P-9999
slot_number_for_registration_number KA-01-HH-9999
'''
