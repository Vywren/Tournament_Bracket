import psycopg2
tournament_number = 0
def access_command_panel(command):
    conn = psycopg2.connect(database = "Bracket", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "2987tubby2987",
                        port = 5432)
    cur = conn.cursor()
    # Execute a command: create datacamp_courses table
    cur.execute(command)
    # Make the changes to the database  persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()


def new_tournament():
    print("Starting new tournament: \n")


new_tournament()