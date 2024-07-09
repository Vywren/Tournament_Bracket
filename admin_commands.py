from psycopg2 import *
#base functions to execute commands
def do_execute(command, param):
    account =  open("account_information.txt","r")
    conn = connect(database = str(account.readline().replace('\n', '')), 
                        user = str(account.readline().replace('\n', '')), 
                        host = str(account.readline().replace('\n', '')),
                        password = str(account.readline().replace('\n', '')),
                        port = int(account.readline()))
    account.close()

    cur = conn.cursor()
    # Execute a command:
    cur.execute(command,param)
    # Make the changes to the database  persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()
def search(command, param):
    account =  open("account_information.txt","r")
    conn = connect(database = str(account.readline().replace('\n', '')), 
                        user = str(account.readline().replace('\n', '')), 
                        host = str(account.readline().replace('\n', '')),
                        password = str(account.readline().replace('\n', '')),
                        port = int(account.readline()))
    account.close()

    cur = conn.cursor()
    # Execute a command:
    cur.execute(command,param)
    # Make the changes to the database  persistent
    msg = cur.fetchall()
    print(msg)
    ids = []
    for i in msg:
        ids.append(i[0])
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()
    return ids
#player editing related commands
def new_player(first_name, last_name, email, phone_number):
    do_execute("INSERT INTO players (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)", (str(first_name), str(last_name), str(email), str(phone_number)))

   
def update_player_phone_number(phone_number, id):
    do_execute("UPDATE players SET phone_number = %s where user_id = %s",(str(phone_number), str(id)))

def search_player(name):
    search("SELECT * FROM players WHERE first_name = %s OR last_name = %s;",(str(name),str(name)))

def update_player_email(email, id):
    do_execute("UPDATE players SET email = %s where user_id = %s",(str(email), str(id)))

def remove_player(id):
    do_execute("DELETE FROM players WHERE user_id = %s", (str(id),))

def check_in(id):
    do_execute("UPDATE players SET looking_for_match = true WHERE user_id = %s", (str(id),))
def check_out(id):
    do_execute("UPDATE players SET looking_for_match = false WHERE user_id = %s", (str(id),))
def check_out_all():
    do_execute("UPDATE players SET looking_for_match = false",None)
    
#match editing functions
def new_match(tournament_round, tournament_id, id1,id2):
    do_execute("INSERT INTO matches (round, id, player1_id, player2_id, complete) VALUES (%s,%s,%s,%s,%s)", (str(tournament_round),str(tournament_id),str(id1),str(id2), str("false")))
def report_match(wins,losses,draws,match_id):
    do_execute("UPDATE matches SET player1_wins = %s, player1_losses = %s, player1_draws = %s, complete = True WHERE match_id = %s",(wins, losses, draws, match_id))
def display_current_matches():
    search("SELECT * FROM matches WHERE complete = false;",None)    
#todo: complete tournament editing functions
def new_tournament():
    print("Starting new tournament: \n")
    do_execute("INSERT INTO tournaments (tournament_round) VALUES (1)",None)
    player_list =  search("SELECT * FROM players WHERE looking_for_match = true",None)
    print(player_list)
def print_bracket():
    print("will print bracket when finished")
def crown_winner(winner_id, tournament_id):
    do_execute("UPDATE tournaments SET winner_id = %s WHERE tournament_id = %s", (winner_id, tournament_id))
    
    
