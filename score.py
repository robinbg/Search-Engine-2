import nltk
import db
import json
import math
import sys
from bs4 import BeautifulSoup as bs
from collections import defaultdict

def tf(wc, tc):
    if wc == 0:
        return 0
    return float(wc)/float(tc)

def idf():
    pass

def parse(loc, connection):
    doc = open('www/'+loc) 
    content = bs(doc.read(), "lxml")
    counts = defaultdict(float)
    print loc
    try:
        st = nltk.stem.LancasterStemmer()
        tokens = nltk.word_tokenize(content.get_text())
        tc = len(tokens)
        for token in tokens:
            if token not in nltk.corpus.stopwords.words('english'):
                counts[st.stem(token.lower())] += 1
        for k,v in counts.items():
            k = k.encode('utf-8')
            tfscore = str(tf(v,tc))
            if tfscore > 0:
                if len(connection.query("select * from tfidf where term=%s", (k))):
                    connection.query("update tfidf set posting=concat(posting,%s) where term=%s",(";"+loc+":"+tfscore, k))
                else:
                    connection.query("insert into tfidf (term, posting) values (%s, %s)", (k, loc+":"+tfscore))
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
    connection = db.DB('localhost', 'root', '', 'cs121')

    for k,v in sorted(bk.items(), key=lambda items: (int(items[0].split("/")[0]), int(items[0].split("/")[1]))):
        parse(k, connection)
    connection.close()
