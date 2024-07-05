import psycopg2
def access_command_panel(command):
    account =  open("account_information.txt","r")
    conn = psycopg2.connect(database = account.readline(), 
                        user = account.readline(), 
                        host= account.readline(),
                        password = account.readline(),
                        port = account.readline())
    cur = conn.cursor()
    account.close()
    # Execute a command:
    cur.execute(command)
    # Make the changes to the database  persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()

def new_player(first_name, last_name, wins, losses, draws, email, phone_number):
    account =  open("account_information.txt","r")
    conn = psycopg2.connect(database = str(account.readline().replace('\n', '')), 
                        user = str(account.readline().replace('\n', '')), 
                        host = str(account.readline().replace('\n', '')),
                        password = str(account.readline().replace('\n', '')),
                        port = int(account.readline()))
    account.close()

    cur = conn.cursor()
    # Execute a command:
    cur.execute("INSERT INTO players (first_name, last_name, wins, losses, draws, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s)", (first_name, last_name, wins, losses, draws, email, phone_number))
    # Make the changes to the database  persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()
   
def new_tournament():
    print("Starting new tournament: \n")



new_player("jenny", "smith", 0, 0, 0, "jenny.smith@gmail.com", "203-555-5555")