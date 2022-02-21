from flask import Flask, render_template, jsonify, request, redirect
import cx_Oracle
from datetime import datetime
app = Flask(__name__)


con = cx_Oracle.connect("TEMA_BD", "Maria26", "localhost/xe")

@app.route("/")
@app.route('/books')
def books():
  books = []
  sql = con.cursor()
  sql.execute('SELECT b.book_id, b.title, b.book_author, b.price, b.ISBN13, b.num_pages, b.publication_date, p.publisher_name, b.quantity FROM book b JOIN publisher p USING(publisher_id)')

  for result in sql:
    book = {}
    book['book_id'] = result[0]
    book['title'] = result[1]
    book['book_author'] = result[2]
    book['price'] = result[3]
    book['ISBN13'] = result[4]
    book['num_pages'] = result[5]
    book['publication_date'] = datetime.strptime(str(result[6]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')
    book['publisher_name'] = result[7]
    book['quantity'] = result[8]
    books.append(book)
  sql.close()
  return render_template('books.html', books=books)

# @app.route('/books1')
# def books1():
#   books = []
#   sql = con.cursor()
#   sql2=con.cursor()
#   sql.execute('select * from book')
#
#   for result in sql:
#     book = {}
#     book['book_id'] = result[0]
#     book['title'] = result[1]
#     book['book_author'] = result[2]
#     book['price'] = result[3]
#     book['ISBN13'] = result[4]
#     book['num_pages'] = result[5]
#     book['publication_date'] = datetime.strptime(str(result[6]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')
#     #book['publisher_id'] = result[7]
#     book['quantity'] = result[8]
#     a=0
#     if result[7]!=None:
#       sql2.execute('select publisher_name from publisher where publisher_id='+str(result[7]))
#       for res in sql2:
#           book['publisher_name']=res[0]
#     books.append(book)
#   sql.close()
#   return render_template('books1.html', books=books)

@app.route('/addBook', methods=['GET', 'POST'])
def add_book():
   error = None
   if request.method == 'POST':
     sql = con.cursor()
     sql.execute(f"insert into book (title,book_author,price,ISBN13,num_pages,publication_date,publisher_id,quantity) values (\'{request.form['title']}\',\'{request.form['book_author']}\',{request.form['price']},\'{request.form['ISBN13']}\',{request.form['num_pages']},TO_DATE(\'{request.form['publication_date']}\', 'DD-MM-YYYY'),{request.form['publisher_id']},{request.form['quantity']})")
     sql.execute('commit')
     return redirect('/books')
   else:
     publishers= []
     sql = con.cursor()
     sql.execute('select publisher_id, publisher_name from publisher')
     for result in sql:
       publishers.append((result[0],result[1]))
     sql.close()

     return render_template('addBook.html', publishers=publishers)


# @app.route('/addBook', methods=['GET', 'POST'])
# def add_book():
#    error = None
#    if request.method == 'POST':
#      publish_id = {}
#      id = "'" + request.form['publisher_id'] + "'"
#      b = 0
#      sql = con.cursor()
#      sql.execute('select publisher_name from publisher where publisher_id=' + id)
#      for result in sql:
#        publish_id['publisher_name'] = result[0]
#      sql.close()
#      sql = con.cursor()
#      sql.execute('select max(book_id) from book')
#      for result in sql:
#        b = result[0]
#      sql.close()
#      b += 1
#      sql = con.cursor()
#      values = []
#      values.append("'" + str(b) + "'")
#
#      values.append("'" + request.form['title'] + "'")
#      values.append("'" + request.form['book_author'] + "'")
#      values.append("'" + request.form['price'] + "'")
#      values.append("'" + request.form['ISBN13'] + "'")
#      values.append("'" + request.form['num_pages'] + "'")
#      values.append("'" + datetime.strptime(str(request.form['publication_date']), '%d.%m.%Y').strftime('%d-%b-%y') + "'")
#      values.append("'" + str(publish_id['publisher_name']) + "'")
#      values.append("'" + request.form['quantity'] + "'")
#
#      fields = ['book_id', 'title', 'book_author', 'price', 'ISBN13', 'num_pages', 'publication_date', 'publisher_id',
#                'quantity']
#      query = 'INSERT INTO %s (%s) VALUES (%s)' % ('book', ', '.join(fields), ', '.join(values))
#
#      sql.execute(query)
#      sql.execute('commit')
#      return redirect('/book')
#    else:
#      publish= []
#      sql = con.cursor()
#      sql.execute('select publisher_id from publisher')
#      for result in sql:
#        publish.append(result[0])
#      sql.close()
#
#      return render_template('addBook.html', publisher=publish)

@app.route('/delAllBooks', methods=['POST'])
def del_Allbook():
  bid = request.form['book_id']
  sql = con.cursor()
  sql.execute('delete from book where book_id=' + bid)
  sql.execute('commit')
  return redirect('/books')

@app.route('/delBooks', methods=['POST'])
def del_book():
  bid = request.form['book_id']
  sql = con.cursor()
  sql.execute('update book set quantity = quantity -1 where book_id=' + bid)
  sql.execute('commit')
  return redirect('/books')

@app.route('/editBook/<int:book_id>', methods=['POST', 'GET'])
def edit_book(book_id:int):
  if request.method == 'POST':

    title="'"+request.form['title']+"'"
    book=str(book_id)
    book_author="'"+request.form['book_author']+"'"
    price = "'" + request.form['price'] + "'"
    ISBN13 = "'" + request.form['ISBN13'] + "'"
    num_pages = "'" + request.form['num_pages'] + "'"
    publication_date = "'" + datetime.strptime(str(request.form['publication_date']), '%d.%m.%Y').strftime('%d.%b.%y') + "'"
    quantity="'" + request.form['quantity'] + "'"

    publish=request.form['publisher_id']

    sql = con.cursor()
    query = "UPDATE book SET title=%s, book_author=%s, price=%s, ISBN13=%s, num_pages=%s, publication_date=%s, quantity=%s,publisher_id=%s where book_id=%s" % (
    title, book_author, price, ISBN13, num_pages, publication_date, quantity, publish, book)
    sql.execute(query)

    return redirect('/books')

  else:
    sql=con.cursor()
    sql.execute('select * from book where book_id=' + str(book_id))
    boks=sql.fetchone()
    title=boks[1]
    book_author=boks[2]
    price=boks[3]
    ISBN13=boks[4]
    num_pages=boks[5]
    publication_date = datetime.strptime(str(boks[6]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')
    quantity=boks[8]
    sql.close()

    publishers = []
    sql = con.cursor()
    sql.execute('select publisher_id, publisher_name from publisher')
    for result in sql:
      publishers.append((result[0], result[1]))
    sql.close()

    return render_template('editBook.html', publishers=publishers,
                                   title=title, book_author=book_author, price=price, ISBN13=ISBN13,
                                   num_pages=num_pages, publication_date=publication_date, quantity=quantity)

# @app.route('/getBook', methods=['POST'])
# def get_book():
#   book = request.form['book_id']
#   sql=con.cursor()
#   sql.execute('select * from book where book_id=' + book)
#   boks=sql.fetchone()
#   book_id=boks[0]
#   title=boks[1]
#   book_author=boks[2]
#   price=boks[3]
#   ISBN13=boks[4]
#   num_pages=boks[5]
#   publication_date = datetime.strptime(str(boks[6]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')
#   publisher_id=boks[7]
#   quantity=boks[8]
#   sql.close()
#   publisher_name=''
#   sql=con.cursor()
#   sql.execute('select publisher_name from publisher where publisher_id=' + str(publisher_id))
#   for result in sql:
#     publisher_name=result[0]
#   sql.close()
#   publish=[]
#   sql=con.cursor()
#   sql.execute('select publisher_name from publisher')
#   for result in sql:
#     publish.append(result[0])
#   sql.close()
#
#   return render_template('editBook.html', publisher=publish, publisher_name=publisher_name,
#                        title=title, book_author=book_author, price=price, ISBN13=ISBN13,
#                        num_pages=num_pages, publication_date=publication_date, quantity=quantity)


#------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/publishers')
def publish():
  publishers=[]

  sql=con.cursor()
  sql.execute('select * from publisher')

  for result in sql:
    publisher = {}
    publisher['publisher_id'] = result[0]
    publisher['publisher_name'] = result[1]
    publishers.append(publisher)
  sql.close()

  # book = []
  # sql=con.cursor()
  # sql.execute('select book_id from book')
  # for result in sql:
  #   book.append(result[0])
  # sql.close()
  return render_template('publishers.html', publishers=publishers)

@app.route('/delPublishers', methods=['POST'])
def del_publishers():
  publish = request.form['publisher_id']
  sql = con.cursor()
  sql.execute('delete from book where publisher_id=' + publish)
  sql.execute('delete from publisher where publisher_id=' + publish)
  sql.execute('commit')
  return redirect('/publishers')


@app.route('/addPublisher', methods=['GET','POST'])
def add_publisher():
  error = None
  if request.method == 'POST':
    sql = con.cursor()
    sql.execute(f"insert into publisher (publisher_name) values (\'{request.form['publisher_name']}\')")
    sql.execute('commit')
    return redirect('/publishers')
  else:
    return render_template('addPublisher.html')


#------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/orders')
def order():
  order_book=[]

  sql=con.cursor()
  sql.execute('SELECT order_id, c.first_name || \' \' || c.last_name, SUM(b.price) FROM order_book o JOIN order_to_book USING(order_id) JOIN book b USING(book_id) JOIN customer c USING(customer_id) GROUP BY order_id, c.first_name, c.last_name')

  for result in sql:
    order = {}
    order['order_id'] = result[0]
    order['customer_name'] = result[1]
    order['total_cost'] = result[2]
    order_book.append(order)
  sql.close()
  return render_template('orders.html', order_book=order_book)

@app.route("/showBooksOrder/<int:order_id>")
def show_order_books(order_id:int):
  order_books=[]

  sql=con.cursor()
  sql.execute(f"SELECT b.title FROM order_to_book o JOIN book b USING (book_id) WHERE o.order_id={order_id}")

  for result in sql:
    order_books.append(result[0])
  sql.close()
  return render_template('showBooksOrder.html', order_books=order_books)

@app.route('/returnOrders', methods=['POST'])
def return_Order():
  return redirect('/orders')

@app.route('/cancelOrder', methods=['POST'])
def cancel_Order():
  bid = request.form['order_id']
  sql = con.cursor()
  sql.execute('delete from order_book where order_id=' + bid)
  sql.execute('delete from order_to_book where order_id=' + bid)
  sql.execute('commit')
  return redirect('/orders')

@app.route('/sendOrder', methods=['POST'])
def send_Order():
  bid = request.form['order_id']
  sql = con.cursor()
  sql.execute('select book_id from order_to_book where order_id='+bid)
  results=sql.fetchall()
  for result in results:
    sql.execute('update book set quantity=quantity-1 where book_id='+str(result[0]))
  sql.execute('delete from order_book where order_id=' + bid)
  sql.execute('delete from order_to_book where order_id=' + bid)
  sql.execute('commit')
  return redirect('/orders')


#------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/customers')
def customer():
  customers=[]

  sql=con.cursor()
  sql.execute('select * from customer')

  for result in sql:
    customer = {}
    customer['customer_id'] = result[0]
    customer['first_name'] = result[1]
    customer['last_name'] = result[2]
    customer['email'] = result[3]
    customer['adress_customer'] = result[4]
    customer['number_of_orders'] = result[5]
    customers.append(customer)
  sql.close()
  return render_template('customers.html', customers=customers)


if __name__ == '__main__':
  app.run(debug=True)
  con.close()