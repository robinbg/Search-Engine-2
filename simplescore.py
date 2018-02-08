import nltk
import db
import json
from bs4 import BeautifulSoup as bs
from collections import defaultdict

def parse(loc, connection):
    doc = open('www/'+loc) 
    content = bs(doc.read(), "lxml")
    print loc
    try:
        tokens = set(nltk.word_tokenize(content.get_text()))
        for token in set(nltk.word_tokenize(content.get_text())):
            connection.query("insert into tfidf (term, posting) values (%s, %s) on duplicate key update posting=%s", [token, loc, loc])
    except Exception as e:
        print e
        errfile = open('failed.txt', 'a')
        errfile.write(loc+'\n')
        errfile.close()
    doc.close()

if __name__ == '__main__':
    f = open('www/bookkeeping.json')
    bk = json.loads(f.read())
    f.close()
    connection = db.DB('localhost', 'root', '', 'cs121new')

    for k,v in sorted(bk.items(), key=lambda items: (int(items[0].split("/")[0]), int(items[0].split("/")[1]))):
        parse(k, connection)

    connection.close()
