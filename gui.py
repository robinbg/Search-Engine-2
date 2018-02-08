import db
import json
import tornado.ioloop
import tornado.web
from nltk.stem.lancaster import LancasterStemmer

connection = db.DB('localhost', 'root', '', 'cs121new')
bk = json.loads(open('www/bookkeeping.json').read())
st = LancasterStemmer()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("html/index.html") 

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        query = st.stem(self.get_argument("query"))
        page = int(self.get_argument("page"))
        searches = connection.query("""select * from tfidf where term=%s limit %s, %s""", [query, page*10, (page+1)*10])[0][1].split(";")
        self.render("html/search.html", searches=searches, query=query, page=page, bk=bk)

def start():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/search", SearchHandler)
    ])

if __name__ == "__main__":
    app = start()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
