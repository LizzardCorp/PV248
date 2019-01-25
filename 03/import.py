import scorelib
import sqlite3
import sys
import re

def database(data, output):
    conn = sqlite3.connect(output)
    with open('scorelib.sql', 'r') as fd:
        script = fd.read()
        conn.executescript(script)
        conn.commit()

    prints = scorelib.load(data)
    for p in prints:
        process_print(p, conn)
    conn.close()

def process_print(data, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM print WHERE id=(?)", [data.print_id])
    row = cur.fetchone()
    if row is not None:
        return
    edition_id = process_edition(data.edition, conn)
    if data.partiture is None:
        data.partiture = "N"
    cur.execute( "insert into print( id, partiture, edition) values (?,?,?)", (data.print_id, data.partiture, edition_id))
    conn.commit()

def process_edition(data, conn):
    authors = []

    for author in data.authors:
        if (author is not None and author.name is not None and len(author.name) is not 0):
            authors.append(process_person(author, conn))

    score_id = process_composition(data.composition, conn)
    cur = conn.cursor()
    cur.execute("SELECT * FROM edition WHERE score=(?) and name=(?)", (score_id, data.name))
    rows = cur.fetchall()
    for row in rows:
        counter = 0
        for author in authors:
            cur.execute("SELECT * FROM edition_author WHERE edition=(?) and editor=(?)", (row[0], author))
            if cur.fetchone() is not None:
                counter += 1
        if counter == len(authors):
            return row[0]
    cur.execute( "insert into edition( score, name, year) values (?,?,?)", (score_id, data.name, None))
    conn.commit()
    id = cur.lastrowid
    for author in authors:
        cur.execute( "insert into edition_author( edition, editor) values (?,?)", (id, author))
        conn.commit()
    return id

def process_composition(composition, conn):
    authors = []
    voices = []

    for author in composition.authors:
        if (author is not None and author.name is not None and len(author.name) is not 0):
            authors.append(process_person(author, conn))
    cur = conn.cursor()
    cur.execute("SELECT * FROM score WHERE name=(?) and genre=(?) and key=(?) and incipit=(?) and year=(?)", (composition.name, composition.genre, composition.key, composition.incipit, composition.year))
    rows = cur.fetchall()
    for row in rows:
        counter = 0
        for author in authors:
            cur.execute("SELECT * FROM score_author WHERE score=(?) and composer=(?)", (row[0], author))
            if cur.fetchone() is not None:
                counter += 1
        if counter == len(authors):
            return row[0]
        index = 1
        counter = 0
        for voice in voices:
            cur.execute("SELECT * FROM voice WHERE number=(?) and score=(?) and range=(?) and name=(?)", (index, row[0], voice.range, voice.name))
            if cur.fetchone() is not None:
                counter += 1
            index +=1
        if counter == len(voices):
            return row[0]
    cur.execute( "insert into score( name, genre, key, incipit, year) values (?,?,?,?,?)", (composition.name, composition.genre, composition.key, composition.incipit, composition.year))
    conn.commit()
    id = cur.lastrowid
    for author in authors:
        cur.execute( "insert into score_author( score, composer) values (?,?)", (id, author))
        conn.commit()
    index = 1
    for voice in composition.voices:
        if voice is not None:
            voices.append(process_voice(voice, id, index, conn))
        index += 1
    return id

def process_voice(voice, id, index, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM voice WHERE number=(?) and score=(?) and range=(?) and name=(?)", (index, id, voice.range, voice.name))
    row = cur.fetchone()
    if row is not None:
        return row[0]
    cur.execute( "insert into voice( number, score, range, name) values (?,?,?,?)", (index, id, voice.range, voice.name))
    conn.commit()
    return cur.lastrowid

def process_person(person, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM person WHERE name=(?)", [person.name])
    entity = cur.fetchone()
    if entity is not None:
        born = entity[1]
        died = entity[2]
        if born is None:
            born = person.born
        if died is None:
            died = person.died
        cur.execute("UPDATE person SET born=?, died=? WHERE name=?",(born, died, person.name))
        conn.commit()
        return entity[0]
    cur.execute( "insert into person( name, born, died) values (?,?,?)", (person.name, person.born, person.died))
    conn.commit()
    return cur.lastrowid

if __name__ == '__main__':
    if len(sys.argv) !=3:
        print("Wrong number of arguments!")
    else:
        database(sys.argv[1], sys.argv[2])
