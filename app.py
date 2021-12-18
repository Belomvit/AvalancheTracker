from time import sleep
import urllib.request, json 
import winsound
from datetime import datetime

UPDATE_TIME = 60


# Check (addr) number of transactions  
def check_address_activity(addr): 
    try:
        with urllib.request.urlopen(f'https://api.snowtrace.io/api?module=account&action=txlist&address={addr}&startblock=1&endblock=99999999&sort=asc&apikey=YourApiKeyToken') as url:
            data = json.loads(url.read().decode())
        return len(data["result"])
    except Exception as e:
        print (f"ERROR in check_address_activity {e}")
    

# Check & print last trassaction type 
def check_last_transaction(addr):
    try:
        with urllib.request.urlopen(f'https://api.snowtrace.io/api?module=account&action=txlist&address={addr}&startblock=1&endblock=99999999&sort=asc&apikey=YourApiKeyToken') as url:
            data = json.loads(url.read().decode())
        data = data["result"]
        value = data[-1]['input']
        if(value[:10] == "0x38ed1739"):
            print("Type: Swap Tokens")
            play_sound()
            return True
        elif(value[:10] == "0x9ebea88c"):
            print("Type: Unstake")
            play_sound_2()
            return True
        else:
            print("Type: Unknown")
            return False
    except Exception as e:
        print (f"ERROR in check_last_transaction {e}")


# 2 beep notification 
def play_sound():
    winsound.Beep(300,400)
    sleep(0.3)
    winsound.Beep(300,400)


# 3 beep notification 
def play_sound_2():
    winsound.Beep(800,300)
    sleep(0.1)
    winsound.Beep(800,300)
    sleep(0.1)
    winsound.Beep(800,300)


# Loading animation
def wait(sec):
    animation = [
    "[          ]",
    "[=         ]",
    "[==        ]",
    "[===       ]",
    "[====      ]",
    "[=====     ]",
    "[======    ]",
    "[=======   ]",
    "[========  ]",
    "[========= ]",
    "[==========]"
    ]
    for i in animation:
        print(f"{i}", end='\r')
        sleep(sec/10)


# Generate link for address 
def gen_link(addr):
    return f"https://snowtrace.io/address/{addr}"


# Check config file for new addresses
def check_file_update(oldLng):
    f = open("address.txt", "r")
    data = f.read().splitlines()
    f.close()
    if(oldLng != len(data)-1):
        return True
    else:
        return False

# Read config file.
# Return: dict with addresses and default (0) transaction number
def read_file_data():
    f = open("address.txt", "r")
    data = f.read().splitlines()
    f.close()
    return dict.fromkeys(data, 0)


# Init dict with actual transaction number for each address
def init_all_addresses(wallets):
    for i in wallets:
        lng = check_address_activity(i)
        wallets[i] = lng
    return wallets


# Show all my addresses
def show_addresses(wallets):
    print("==========================================\nMy Address List:\n")
    for i,k in wallets.items():
        print(f"{i}")
    print("\n==========================================")


# Show user notification
def alert_user(addr):
    print(f"[{datetime.now()}] New Transaction")
    print(f"-----------------------------------------------------------------------------")
    print(f"Wallet: {addr}")
    check_last_transaction(addr)  
    print(f"Link: {gen_link(addr)}")
    print(f"-----------------------------------------------------------------------------")





wallets = read_file_data()
init_all_addresses(wallets)
file_len = len(wallets)

show_addresses(wallets)

while 1:
    for i in wallets:
        lng = check_address_activity(i)
        #print(f"<w:{i} / {lng} / {wallets[i]}>")
        if(lng != wallets[i]):
            diff = lng - wallets[i]
            if((diff > 0 and diff < 5) or (diff < 0 and diff > -5) ):
                wallets[i] = lng
                alert_user(i)

    print(f"[{datetime.now()}] OK")

    if(check_file_update(file_len)):
        print(f"[{datetime.now()}] New Addres Found")
        wallets = read_file_data()
        init_all_addresses(wallets)
        show_addresses(wallets)
        file_len = len(wallets)

    wait(UPDATE_TIME)
