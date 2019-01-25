import sqlite3
import sys
import json

def get_print(id):
    conn = sqlite3.connect('scorelib.dat')
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

    print(json.dumps(output, indent=4, ensure_ascii=False))
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) !=2:
        print("Wrong number of arguments!")
    else:
        get_print(sys.argv[1])
