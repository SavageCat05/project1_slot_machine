import random

MAX_LINES = 3 #this is the maximum number of lines on which we can bet
MIN_BET = 100 
MAX_BET = 10000

Rows = 3
Cols = 3
Symbols = {
    "\1" : 6,
    "\3" : 7,
    "7" : 3,
    "\5" : 5
}
value_of_symbols = {
    "\1" : 3,
    "\3" : 1,
    "7" : 10,
    "\5" : 5
}
# jackpot for 7, if 3 in a row 

def check_winnings(columns, lines, bet, values:dict)->int:
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:  
            winning_lines.append(line+1)
            winnings = values.get(symbol) * bet * len(winning_lines)

    return winnings,winning_lines


def get_slot_machine_spin(rows,cols,symbols:dict):
    sym_list = []
    for sym, sym_count in symbols.items():
        for _ in range(sym_count):
                sym_list.append(sym)

    columns = []
    for _ in range(cols): #basically we are creating a [[], [], []] so 3 colums , jisme har ek column ek reel ko represent kr rha hai jo ghume gi 
        column = [] # every single mini column is represented by this column
        #very less chance to win this way, lets create some more possibilities
        #changed Symbols in line below to sym_list
        current_symbols = list(sym_list) #this creates a copy of my list, other method to do this was to Symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value) #removes first instace of value present in our list
            column.append(value)
        columns.append(column)
    return columns

#we basically want to transpose our matrix 
def print_slot_machine(columns):
    for row in range((len(columns[0]))):
        for i,column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], "|", end = " | ")
            else:
                print(column[row], end = "")
        print()


def get_deposit():
    """This takes in the deposit a player will make"""
    while True:
        amount = input("Enter the amount you would like to deposit \nRs. ")
        if amount.isdigit(): 
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount should be greater than 0.")
        else:
            print("Please enter a valid number")
    return amount 

def get_no_of_lines(): 
    """This takes in the no of lines on which player will bet"""
    while True:
        lines = input(f"Enter the number of lines you would like to bet on from 1 to {MAX_LINES}\n> ")
        if lines.isdigit(): 
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Number of lines to play can only lie between 1 to 3.\n> ")
        else:
            print("Please enter a valid number")
    return lines 

def get_bet():
    """This function takes in the amount player will bet on each line"""
    while True:
        amount = input(f"Enter the amount you would like to bet on each line: Rs.{MIN_BET} to Rs.{MAX_BET}\n> ")
        if amount.isdigit(): 
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount should lie between {MIN_BET} to {MAX_BET}.")
        else:
            print("Please enter a valid number")
    return amount 

def spin(balance):
    while True:
        lines = get_no_of_lines()
        bet = get_bet()
        total_bet = bet * lines 

        if total_bet>balance:
            print(f"you do not have sufficient balance. Your current balance is: Rs.{balance}")
            ask_more = input("Would you like to deposit more? \n>1 - Yes, 2- No ")
            if ask_more.isdigit():
                if int(ask_more) == 1:
                    #some sort of error will occur that global balance is not updated
                    new_balance = get_deposit()
                    balance = balance + new_balance
                else:
                    exit()
        else:
            break

    print(f"You are betting Rs.{bet} on {lines}. Total bet is:{bet*lines}")

    slots = get_slot_machine_spin(Rows,Cols,Symbols)
    print_slot_machine(slots)

    #changing "bet" to "total_bet"
    winnings,winning_lines = check_winnings(slots, lines, total_bet, value_of_symbols)
    print(f"You Won: Rs.{winnings}")
    print(f"You won on lines:", *winning_lines )
    return winnings - total_bet


def main():
    balance = get_deposit()
    while True:
        print(f"current balance is: {balance}")
        spin1 = input("Press enter to play (q to quit)\n> ")
        if spin1 == "q":
            break
        balance += spin(balance)
    
    print(f"You are left with: {balance}")
main()