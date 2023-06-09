import requests
from termcolor import colored
import pyfiglet

# Print OSINTAMBITION in a bigger font size
ascii_banner = pyfiglet.figlet_format("ETHERSCAN CLI")
print(colored(ascii_banner.rstrip(), "blue", attrs=["bold"]))
print()
print()

# Print the API information
print(colored("Developed by:", "cyan", attrs=["bold"]))
print(colored("OSINTAMBITION(@osintambition)", "cyan",attrs=["bold"]))
# Print the purpose of the program
print("Usage - For checking if the cryptocurrenvy address is suspicious or not")
print()
print()

def get_api_key():
    try:
        with open('api.txt', 'r') as file:
            api_key = file.read()
        return api_key
    except FileNotFoundError:
        print("API file not found.")
        exit()

def get_balance(address, api_key):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == '1':
        balance = int(data['result']) / 10**18  # Convert balance from Wei to Ether
        print(f"Balance of {address}: {balance} ETH")
    else:
        print("Error retrieving balance.")

def get_transactions(address, num_transactions, api_key):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == '1':
        transactions = data['result'][:num_transactions]  # Get the specified number of transactions
        print(f"{num_transactions} transactions of {address}:")
        for tx in transactions:
            tx_hash = tx['hash']
            recipient = tx['to']
            value = int(tx['value']) / 10**18
            print(f"TxHash: {tx_hash}, Recipient: {recipient}, Value: {value} ETH")
    else:
        print("Error retrieving transactions.")

def get_gas_price(api_key):
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == '1':
        gas_price = int(data['result']['FastGasPrice']) / 10**9  # Convert gas price from Wei to Gwei
        print(f"Current gas price: {gas_price} Gwei")
    else:
        print("Error retrieving gas price.")

def main_menu():
    print("Welcome to the Etherscan.io API menu!")
    print("1. Check address balance")
    print("2. Get transactions of an address")
    print("3. Get current gas price")
    print("4. Exit")
    choice = input("Enter your choice: ")
    print()
    print()

    if choice == '1':
        address = input("Enter Ethereum address: ")
        api_key = get_api_key()
        get_balance(address, api_key)
        print()
        print()
    elif choice == '2':
        address = input("Enter Ethereum address: ")
        num_transactions = int(input("Enter the number of transactions to retrieve: "))
        api_key = get_api_key()
        get_transactions(address, num_transactions, api_key)
        print()
        print()
    elif choice == '3':
        api_key = get_api_key()
        get_gas_price(api_key)
        print()
        print()
    elif choice == '4':
        print("Exiting...")
        print()
        print()
        return
    else:
        print("Invalid choice. Please try again.")
        print()
        print()

    print()  # Add an empty line for readability
    main_menu()

main_menu()
