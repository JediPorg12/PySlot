import random

# Constants for game configuration
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

# Symbols and their respective counts and values
symbols = {
    "A": {"count": 2, "value": 5},
    "B": {"count": 4, "value": 4},
    "C": {"count": 6, "value": 3},
    "D": {"count": 8, "value": 2}
}

# Add a Wild symbol to the symbol dictionary
symbols['W'] = {"count": 1, "value": 10}  # Wild symbol with a higher value


def get_deposit_amount():
    """Prompt the player to deposit an initial amount."""
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit() and int(amount) > 0:
            return int(amount)
        else:
            print("Please enter a valid positive amount.")


def get_valid_input(prompt, valid_range):
    """Prompt the player for a valid integer input within the specified range."""
    while True:
        value = input(prompt)
        if value.isdigit() and valid_range[0] <= int(value) <= valid_range[1]:
            return int(value)
        else:
            print(f"Please enter a valid number between {valid_range[0]} and {valid_range[1]}.")


def get_bet_amount():
    """Prompt the player to enter the bet amount per line."""
    prompt = f"What would you like to bet on each line? (${MIN_BET} - ${MAX_BET}) "
    return get_valid_input(prompt, (MIN_BET, MAX_BET))


def get_slot_machine_spin(rows, cols, symbols):
    """Generate a spin of the slot machine with wild symbols included."""
    all_symbols = []
    for symbol, data in symbols.items():
        all_symbols.extend([symbol] * data["count"])

    columns = []
    for _ in range(cols):
        column = random.choices(all_symbols, k=rows)
        columns.append(column)

    return columns


def print_slot_machine(columns):
    """Print the current state of the slot machine grid."""
    for row in zip(*columns):
        print(" | ".join(row))


def calculate_winnings(columns, lines, bet):
    """Calculate winnings based on the slot machine result."""
    winnings = 0
    winning_lines = []

    for line in range(lines):
        unique_symbols = set(columns[col][line] for col in range(COLS))

        # Check for winning combinations with Wild symbol
        if len(unique_symbols) == 2 and 'W' in unique_symbols:
            # Wild symbol replaces any other symbol to form a winning line
            symbol = (unique_symbols - {'W'}).pop()
            winnings += symbols[symbol]['value'] * bet
            winning_lines.append(line + 1)
        elif len(unique_symbols) == 1 and 'W' not in unique_symbols:
            symbol = columns[0][line]
            winnings += symbols[symbol]['value'] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def spin_slot_machine(balance):
    """Simulate a single spin of the slot machine."""
    lines = get_valid_input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ", (1, MAX_LINES))
    bet = get_bet_amount()
    total_bet = bet * lines

    if total_bet > balance:
        print(f"You do not have enough to bet ${total_bet}. Your current balance is: ${balance}")
        return 0

    print(f"You are betting ${bet} on {lines} lines. Total bet is: ${total_bet}")

    # Spin the slot machine to get the result
    columns = get_slot_machine_spin(ROWS, COLS, symbols)
    print_slot_machine(columns)

    # Calculate winnings
    winnings, winning_lines = calculate_winnings(columns, lines, bet)
    print(f"You won ${winnings}.")
    if winning_lines:
        print(f"You won on lines: {', '.join(map(str, winning_lines))}")

    return winnings - total_bet


def main():
    balance = get_deposit_amount()

    while True:
        print(f"Current balance: ${balance}")
        answer = input("Press ENTER to play or 'q' to quit: ")

        if answer.lower() == 'q':
            break

        winnings = spin_slot_machine(balance)
        balance += winnings

    print(f"You left with ${balance}")


if __name__ == "__main__":
    main()
