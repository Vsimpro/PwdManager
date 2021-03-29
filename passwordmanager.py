import os
import base64
import sqlite3

global file
file = "wallet.db"

GRAY = "\033[90m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"

def refresh_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    size = f"{os.get_terminal_size()}"
    terminal = int(size.split("=")[1].split(",")[0])
    if terminal <= 100:
        print(GRAY,"-- small monitor mode --",BLUE, end="")
        print(f"""
╔═╗┌─┐┌─┐┌─┐┬ ┬┌─┐┬─┐┌┬┐  
╠═╝├─┤└─┐└─┐││││ │├┬┘ ││  
╩  ┴ ┴└─┘└─┘└┴┘└─┘┴└──┴┘{CYAN}""",f"""
╔╦╗╔═╗╔╗╔╔═╗╔═╗╔═╗╦═╗     
║║║╠═╣║║║╠═╣║ ╦║╣ ╠╦╝     
╩ ╩╩ ╩╝╚╝╩ ╩╚═╝╚═╝╩╚═  {YELLOW} -- by Vsim""")
        return
    print(BLUE, end="")
    print("""                                                                   
 ███████████                                                                   █████     v1.0        
░░███░░░░░███                                                                 ░░███              
 ░███    ░███  ██████    █████   █████  █████ ███ █████  ██████  ████████   ███████              
 ░██████████  ░░░░░███  ███░░   ███░░  ░░███ ░███░░███  ███░░███░░███░░███ ███░░███              
 ░███░░░░░░    ███████ ░░█████ ░░█████  ░███ ░███ ░███ ░███ ░███ ░███ ░░░ ░███ ░███              
 ░███         ███░░███  ░░░░███ ░░░░███ ░░███████████  ░███ ░███ ░███     ░███ ░███              
 █████       ░░████████ ██████  ██████   ░░████░████   ░░██████  █████    ░░████████  """,CYAN,"""                                                                               
 ██████   ██████   █████████   ██████   █████   █████████     █████████  ██████████ ███████████  
░░██████ ██████   ███░░░░░███ ░░██████ ░░███   ███░░░░░███   ███░░░░░███░░███░░░░░█░░███░░░░░███ 
 ░███░█████░███  ░███    ░███  ░███░███ ░███  ░███    ░███  ███     ░░░  ░███  █ ░  ░███    ░███ 
 ░███░░███ ░███  ░███████████  ░███░░███░███  ░███████████ ░███          ░██████    ░██████████  
 ░███ ░░░  ░███  ░███░░░░░███  ░███ ░░██████  ░███░░░░░███ ░███    █████ ░███░░█    ░███░░░░░███ 
 ░███      ░███  ░███    ░███  ░███  ░░█████  ░███    ░███ ░░███  ░░███  ░███ ░   █ ░███    ░███ 
 █████     █████ █████   █████ █████  ░░█████ █████   █████ ░░█████████  ██████████ █████   █████
░░░░░     ░░░░░ ░░░░░   ░░░░░ ░░░░░    ░░░░░ ░░░░░   ░░░░░   ░░░░░░░░░  ░░░░░░░░░░ ░░░░░   ░░░░░ 
    """,YELLOW ,"""                                                                                             
    -- Handcrafted with love, by Vsim.\n 
    """, WHITE)

def check_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Exception as e:
        print(e, RED, " -- an error occured! Trying to creat a new .db")
        with open(path, "a+") as temp:
            temp.close()
        connection = sqlite3.connect(path)
        check_table(connection)       
    return connection

def check_table(connection):
    try:
        connection.execute("CREATE TABLE IF NOT EXISTS HASHED ([Service] text, [Password] text)")
    except Exception as e:
        print(e)
        connection.execute("CREATE TABLE HASHED ([Service] text, [Password] text)")

def hash_encode(passw):
    hash_encoded = base64.b64encode(passw.encode())
    hash_encoded = base64.b32encode(hash_encoded)
    return hash_encoded

def hash_decode(passw):
    hash_decoded = base64.b32decode(passw)
    hash_decoded = base64.b64decode(hash_decoded)
    return hash_decoded.decode()

def insert_data(service, password):
    global connection
    password = hash_encode(password).decode()
    entry_data = f"INSERT INTO HASHED (Service, Password) VALUES ('{service}', '{password}');"
    try:
        connection.execute(entry_data) 
    except Exception as e:
        check_table(connection)
        connection.execute(entry_data)

def read_data():
    refresh_screen()
    data = connection.execute("SELECT * FROM HASHED")
    space = " "
    print(GREEN,"SERVICE:",space*24,"PASSWORD:",WHITE)
    for post in data:
        password = post[1].encode()
        service = post[0]  
        print(f" {post[0]}",space*7, space*(24 - (len(post[0]) )), f"{hash_decode(password)}")
    input("\nPRESS ENTER TO GO BACK\n")
    main(False)    

def new_service():
    refresh_screen()
    service = input(f"\n{GREEN}Service name:{WHITE} ")
    if "DROP TABLE" in service:
        warning = f"{RED}INVALID INPUT: {service} might contain malicious contents.\n{YELLOW}PRESS ENTER TO TRY AGAIN\n"
        input(warning)
        new_service()
    insert_data(service, input(f"{GREEN}Password for the service:{WHITE} "))
    input("PRESS ENTER TO GO BACK\n")
    main(False)    

def main(invalidinput):
    refresh_screen()
    print(RED, "\nInvalid input!"*invalidinput, WHITE)
    user = input("Welcome! Select [R]ead or [W]rite: ").replace(" ","").lower()
    if user == "":
        main(True) 
    if user[0] == "r":
        try:
            read_data()
        except Exception as e:
            input(f"{RED}Either an error occured or database is empty! ENTER TO TRY AGAIN{WHITE}\n")
            main(False)
    if user[0] == "w":
        new_service()
    else:
        main(True)

if __name__ == "__main__":
    global connection
    connection = check_connection(file)
    try:
        main(False)
    except KeyboardInterrupt:
        print(WHITE)
        connection.commit()
        connection.close()
