from flask import Flask , make_response,request,jsonify
from flask_mongoengine import MongoEngine
# from api_constants import mongodb_password

app = Flask(__name__)
database_name = "API"
DB_URI = "mongodb+srv://7764835755:<Manish@12345>@cluster0.gm6nkpx.mongodb.net/?retryWrites=true&w=majority"
# DB_URI = "mongodb+srv://7764835755:{}@cluster0.gm6nkpx.mongodb.net/?retryWrites=true&w=majority".format(mongodb_password,database_name)
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
db.init_app(app)

'''
Sample Request Body
{
    "book_id": 1,
    "name": "A Game of Thrones",
    "author": "George R.R.Martin"
}
'''

class Book(db.Document):
    book_id = db.IntField()
    name = db.StringField()
    author = db.StringField()

    def to_json(self):
        #convert this document to json
        return{
            "book_id": self.book_id,
            "name": self.name,
            "author": self.author
        }
'''
Let's go over what each of the http methods for our API does-

POST /api/db_populate -> Populates the db and returns 201 success code(empty response body)

GET /api/books -> Returns the details of all books (with code 200 success code)

POST /api/books -> Creates a new book and returns 201 success code (empty response body)

GET /api/books/3 -> Returns the details of book 3 (with 200 success code if document found,404 if not found)

PUT /api/books/3 -> Update author and name fields of book 3 (with 204 success code)

DELETE / api/books/3 -> deletes book 3 (with 204 success code)
'''

@app.route('/api/db_populate',methods = ['POST'])
def db_populate():
    book1 = Book(book_id=1,name="A Game of Thrones",author="George RR Martin")
    book2 = Book(book_id=2,name="Lord of the Rings",author="JRR Tolkin")
    book1.save()
    book2.save()
    return make_response("",201)

@app.route('/api/books',methods = ['GET','POST'])
def api_books():
    if request.method == "GET":
        books = []
        for book in Book.objects:
            books.append(book)
        return make_response(jsonify(books),200)
    elif request.method == "POST":
        '''
        Sample Request Body
        {
            "book_id": 1,
            "name": "A Game of Thrones",
            "author": "George R.R.Martin"
        }
        '''
        content = request.json
        book = Book(book_id=content['book_id'],name=content['name'],author=content['author'])
        book.save()
        return make_response("",201)


@app.route('/api/books/<book_id>',methods = ['GET','PUT','DELETE'])
def api_each_book(book_id):
    if request.method == "GET":
        book_obj = Book.objects(book_id=book_id).first()
        if book_obj:
            return make_response(jsonify(book_obj.to_json()),200)
        else :
            return make_response("",404)
    elif request.method == "PUT":
        '''
        Sample Request Body
        {
            "book_id": 1,
            "name": "A Game of Thrones",
            "author": "George R.R.Martin"
        }
        '''
        content = request.json
        book = Book.objects(book_id=book_id).first()
        book_obj.update(author = content['author'],name = content['name'])
        return make_response("",204)
    elif request.method == "DELETE":
        book_obj = Book.objects(book_id=book_id).first()
        book_obj.delete()
        return make_response("",204)
    



if __name__ == '__main__':
    app.run()