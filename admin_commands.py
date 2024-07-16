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
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()
    return msg
#player editing related commands
def new_player(first_name, last_name, email, phone_number):
    do_execute("INSERT INTO players (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)", (str(first_name), str(last_name), str(email), str(phone_number)))

def update_player_phone_number(phone_number, id):
    do_execute("UPDATE players SET phone_number = %s where user_id = %s",(str(phone_number), str(id)))

def search_player(name):
    msg = search("SELECT * FROM players WHERE first_name = %s OR last_name = %s;",(str(name),str(name)))
    ids = []
    for i in msg:
        ids.append(i[0])
    return ids
def find_name(id):
    msg = search("SELECT * FROM players WHERE user_id = %s;",(str(id),))
    return msg[0]
def update_player_email(email, id):
    do_execute("UPDATE players SET email = %s where user_id = %s",(str(email), str(id)))

def remove_player(id):
    do_execute("DELETE FROM players WHERE user_id = %s", (str(id),))

def check_in(email):
    do_execute("UPDATE players SET looking_for_match = true WHERE email = %s", (str(email),))
    
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
    msg = search("SELECT * FROM matches WHERE complete = false;",None)    
    ids = []
    for i in msg:
        ids.append(i[0])
    return ids

#seeding related functions
def unseed(tournament_id, seed):
    return search("SELECT * FROM seeding WHERE tournament_id = %s and seed = %s", (str(tournament_id),str(seed)))[0][0]
#def seed(id,seed,tournament):
 #   "INSERT INTO seeding (tournament_name, tournament_date, tournament_round) VALUES (%s, %s, 1)"
#tournament functions
def quick_tournament_round_robin(tournament_name, tournament_date):
    print("Starting new tournament: \n")
    #TODO CHECK IF TOURNAMENT ALREADY EXISTS BEFORE MAKING A NEW ONE
    print(search("SELECT tournament_id FROM tournaments WHERE tournament_name = %s and tournament_date = %s",(tournament_name, tournament_date)) != None)
    if(search("SELECT tournament_id FROM tournaments WHERE tournament_name = %s and tournament_date = %s",(tournament_name, tournament_date))!= []):
        print("Tournament with the same name was already created today, please try another name")
        return -1
    #makes new tournament table entry
    do_execute("INSERT INTO tournaments (tournament_name, tournament_date, tournament_round) VALUES (%s, %s, 1)",(tournament_name, tournament_date))
    tournament_id = search("SELECT tournament_id FROM tournaments WHERE tournament_name = %s and tournament_date = %s",(tournament_name, tournament_date))[0][0]
    #looks for available players
    msg = search("SELECT * FROM players WHERE looking_for_match = true LIMIT 8",None)
    print(msg)
    if((len(msg) > 4 and len(msg) < 7)):
        msg = msg[0:3]
    if(len(msg) < 4):
        print("too few players, terminating")
        return -1
    player_list = []
    seeded_list = []
    seed = 0
    for i in msg:
        seed = seed + 1
        seeded_list.append(seed)
        player_list.append(i[0])
        check_out(i[0])
        do_execute("INSERT INTO seeding (tournament_id, player_id, seed) VALUES (%s, %s, %s)",(tournament_id, i[0], seed))
    #assign seeds for convenience
    if len(seeded_list) % 2 != 0:
        do_execute("INSERT INTO seeding (tournament_id, player_id, seed) VALUES (%s, %s, %s)",(tournament_id, 1, seed))
    save = 0
    for x in range(1,4):
        if x != 1:
            for player in range(0, len(seeded_list), 4):
                save = seeded_list[player + 2]
                seeded_list[player + 2] = seeded_list[player + 3]
                seeded_list[player + 3] = save
        pair_up(x, tournament_id, seeded_list)
        for player in range(0, len(seeded_list), 4):
            save = seeded_list[player] 
            seeded_list[player] = seeded_list[player + 3]
            seeded_list[player+3] = save
        print_pairings(x, tournament_id)

def quick_tournament_bracket(tournament_name, tournament_date):     
    tournament_id = search("SELECT tournament_id FROM tournaments WHERE tournament_name = %s and tournament_date = %s",(tournament_name, tournament_date))[0][0]
    player_list = search("SELECT DISTINCT player2_id FROM matches WHERE id = %s",(tournament_id,))
    print(player_list)
    for player in player_list:
        print(int (search("SELECT sum(player1_wins) FROM matches WHERE player1_id = %s AND id = %s",(str(player[0]), str(tournament_id)))[0][0] or 0) + int(search("SELECT sum(player1_losses) FROM matches WHERE player2_id = %s AND id = %s",(str(player[0]), str(tournament_id)))[0][0] or 0))
        print(int (search("SELECT sum(player1_losses) FROM matches WHERE player1_id = %s AND id = %s",(str(player[0]), str(tournament_id)))[0][0] or 0) + int(search("SELECT sum(player1_wins) FROM matches WHERE player2_id = %s AND id = %s",(str(player[0]), str(tournament_id)))[0][0] or 0))
        print(int (search("SELECT sum(player1_draws) FROM matches WHERE player1_id = %s OR player2_id = %s AND id = %s",(str(player[0]),str(player[0]), str(tournament_id)))[0][0] or 0))
def pair_up(round_num, tournament_id, seeded_player_list):
    skip = 0
    saved_player = -1
    for player in seeded_player_list:
        #print(unseed(tournament_id, player))
        if skip == 0:
            skip = 1
            saved_player = unseed(tournament_id, player)
        else:
            new_match(round_num, tournament_id, saved_player, unseed(tournament_id, player))
            skip = 0
            
def display_unfinished():
    search("SELECT * FROM tournaments WHERE winner_id IS NULL;", None)
    
def print_pairings(round_num, tournament):
    msg = search("SELECT * FROM matches WHERE round = %s AND id = %s;", (round_num, tournament))
    for match in msg:
        player_1 = find_name(match[3])
        player_1 = "#" + str(player_1[0]) + " " + str(player_1[1]) + " " + str(player_1[2])
        player_2 = find_name(match[4])
        player_2 = "#" + str(player_2[0]) + " " + str(player_2[1]) + " " + str(player_2[2])
        print(player_1 + " VS " + player_2)
    
def increment_round(tournament_id):
    msg = search("SELECT * FROM tournaments WHERE tournament_id = %s;", (tournament_id,))
    if msg != []:
        round = msg[0][4] + 1
        do_execute("UPDATE tournaments SET tournament_round = %s WHERE tournament_id = %s;",(round, tournament_id))
    else:
        print("tournament does not exist")
        
    
    
def crown_winner(winner_id, tournament_id):
    do_execute("UPDATE tournaments SET winner_id = %s WHERE tournament_id = %s", (winner_id, tournament_id))
    
    
#notes test unseed and all tournament functions