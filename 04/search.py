import sqlite3
import sys
import json

def search(author):
    conn = sqlite3.connect('scorelib.dat')
    cur = conn.cursor()
    output = {}
    names = fetch_full_names(conn, author)
    for name in names:
        output_print = []
        prints = fetch_print_ids(conn, name[0])
        for p in prints:
            score_authors = fetch_score_authors(conn, p[0])
            edition_authors = fetch_edition_authors(conn, p[0])
            edition = fetch_edition(conn, p[2])
            score = fetch_score(conn, edition[0])
            voices = fetch_voices(conn, edition[0])
            result_print = {
                "print number" : p[0],
                "composer" : score_authors,
                "editor" : edition_authors,
                "partiture" : p[1],
                "edition" : edition[1],
                "title" : score[1],
                "genre" : score[2],
                "key" : score[3],
                "incipit" : score[4],
                "publication year" : int(score[5]) if score[5] is not None else None,
                "voices" : voices
            }
            output_print.append(result_print)
        output[name[0]] = output_print
    print(json.dumps(output, indent=4, ensure_ascii=False))
    conn.close()

def fetch_full_names(conn, name):
    cur = conn.cursor()
    cur.execute('SELECT person.name '
                'FROM print '
                'INNER JOIN edition ON print.edition = edition.id '
                'INNER JOIN score ON edition.score = score.id '
                'INNER JOIN score_author ON score.id = score_author.score '
                'INNER JOIN person ON person.id = score_author.composer '
                'WHERE person.name like (?)', ['%'+name+'%'])
    return cur.fetchall()

def fetch_print_ids(conn, name):
    cur = conn.cursor()
    cur.execute('SELECT print.id, print.partiture, print.edition '
                'FROM print '
                'INNER JOIN edition ON print.edition = edition.id '
                'INNER JOIN score ON edition.score = score.id '
                'INNER JOIN score_author ON score.id = score_author.score '
                'INNER JOIN person ON person.id = score_author.composer '
                'WHERE person.name=(?)', [name])
    return cur.fetchall()

def fetch_score_authors(conn, id):
    cur = conn.cursor()
    cur.execute('SELECT person.name, person.born, person.died '
                'FROM print '
                'INNER JOIN edition ON print.edition = edition.id '
                'INNER JOIN score ON edition.score = score.id '
                'INNER JOIN score_author ON score.id = score_author.score '
                'INNER JOIN person ON person.id = score_author.composer '
                'WHERE print.id=(?) ', [id])
    rows = cur.fetchall()
    output = []
    for row in rows:
        person = {
            "name" : row[0],
            "born" : int(row[1]) if row[1] is not None else None ,
            "died" : int(row[2]) if row[2] is not None else None
        }
        output.append(person)

    return output

def fetch_edition_authors(conn, id):
    cur = conn.cursor()
    cur.execute('SELECT person.name, person.born, person.died '
                'FROM print '
                'INNER JOIN edition ON print.edition = edition.id '
                'INNER JOIN edition_author ON edition.id = edition_author.edition '
                'INNER JOIN person ON person.id = edition_author.editor '
                'WHERE print.id=(?) ', [id])
    rows = cur.fetchall()
    output = []
    for row in rows:
        person = {
            "name" : row[0],
            "born" : int(row[1]) if row[1] is not None else None ,
            "died" : int(row[2]) if row[2] is not None else None
        }
        output.append(person)

    return output

def fetch_edition(conn, id):
    cur = conn.cursor()
    cur.execute('SELECT edition.score, edition.name '
                'FROM edition '
                'WHERE edition.id=(?) ', [id])
    return cur.fetchone()

def fetch_score(conn, id):
    cur = conn.cursor()
    cur.execute('SELECT * '
                'FROM score '
                'WHERE score.id=(?) ', [id])
    return cur.fetchone()

def fetch_voices(conn, score):
    cur = conn.cursor()
    cur.execute('SELECT * '
                'FROM voice '
                'WHERE voice.score=(?) '
                'ORDER BY voice.number ASC ', [score])
    rows = cur.fetchall()
    output = {}
    for row in rows:
        voice = {
            "name" : row[4],
            "range" : row[3]
        }
        output[row[1]] = voice

    return output









if __name__ == '__main__':
    if len(sys.argv) !=2:
        print("Wrong number of arguments!")
    else:
        search(sys.argv[1])
