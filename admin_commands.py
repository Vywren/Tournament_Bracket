import psycopg2
def access_command_panel(command):
    conn = psycopg2.connect(database = "Bracket", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "2987tubby2987",
                        port = 5432)
    cur = conn.cursor()
    # Execute a command:
    cur.execute(command)
    # Make the changes to the database  persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()

def new_player():
    conn = psycopg2.connect(database = "Bracket", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "2987tubby2987",
                        port = 5432)
    cur = conn.cursor()
    # Execute a command:
    cur.execute("INSERT INTO players (first_name, last_name, wins, losses, draws, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("john", "smith", 0, 0, 0, "john.smith@gmail.com", 203-555-5555))
    # Make the changes to the database  persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()
   
def new_tournament():
    print("Starting new tournament: \n")\



new_player()