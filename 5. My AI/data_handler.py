'''This is the database: create, read and write file'''
import sqlite3
import time
import datetime

### People table
def check_and_read_from_db(name, person):
    conn = sqlite3.connect('my_ai.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    print("Looking up %s in databse" % (name))
    try:
        fetch_string = ('SELECT * FROM people WHERE full_name="{}"'.format(name))
        c.execute(fetch_string)
        p_info = c.fetchone()
        if p_info is None:
            print("Not found in data base...")
            return(person)
        else:
            print("Found %s in database." % (name))
            person.full_name = p_info[0]
            person.first_name = p_info[1]
            person.last_name = p_info[2]
            person.birth_year = p_info[3]
            person.birth_place = p_info[4]
            person.death_year = p_info[5]
            person.death_place = p_info[6]
            person.gender = p_info[7]
            person.gender_nick = p_info[8]
            if p_info[9] == 0:
                person.deceased = False
            elif p_info[9] == 1:
                person.deceased = True
            person.summary = p_info[10]
            return(person)
    except:
        print("Totally failed to fetch data from database")

    conn.close()

def data_table_people(person): # Create a table called people if it does not exist
    conn = sqlite3.connect('my_ai.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS people (full_name TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, birth_year INTEGER, birth_place TEXT, death_year INTEGER, death_place TEXT, gender TEXT, gender_nick TEXT, deceased INTEGER, summary TEXT)')
    if person.deceased is False:
        person_deceased = 0
    else:
        person_deceased = 1
    try:
        c.execute("INSERT INTO people (full_name, first_name, last_name, birth_year, birth_place, death_year, death_place, gender, gender_nick, deceased, summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (person.full_name, person.first_name, person.last_name, person.birth_year, person.birth_place, person.death_year, person.death_place,person.gender, person.gender_nick, person_deceased, person.summary))
    except sqlite3.IntegrityError:
         print('ERROR: ID already exists in PRIMARY KEY column')
    conn.commit()
    conn.close()
        