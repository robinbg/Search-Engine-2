import db
import json
import sys
from nltk.stem.lancaster import LancasterStemmer

def query(bk, connection, q):
    count = 0
    for i in connection.query("select * from tfidf where term=%s", [q]):
        for p in i[1].split(';'):
            print p, bk[p]
            count += 1
    print count

if __name__ == "__main__":
    connection = db.DB('localhost', 'root', '', 'cs121')
    bk = json.loads(open('www/bookkeeping.json').read())
    st = LancasterStemmer()
    if len(sys.argv) == 1:
        while(1):
            q = input("> ")
            query(bk, connection, q)
    else:
        query(bk, connection, sys.argv[1])
    connection.close()
