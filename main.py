import random
import re
from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '1b1966f2c38fe40af77584ebb9957d67a6b2637a'

db_config = dict({
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'djentpc'
})


###### index.html ###################################################
@app.route("/")
def index():
    return render_template("index.html")


##### index.html end #####################################################

###### catalog.html ###################################################
@app.route("/catalog")
def catalog():
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
    )
    cursor = connection.cursor()
    request_string = ("SELECT "
                      "product_id,"
                      "img_src,"
                      "processor,"
                      "frequency,"
                      "socket,"
                      "cores,"
                      "threads,"
                      "ram_size,"
                      "ram_type,"
                      "price "
                      "FROM products")

    if (request.args.get('filters') == '1'):

        request_string += (" WHERE ")  # SELECT x,y FROM t WHERE ...

        for key, value in request.args.items():

            if key != 'filters':

                string1 = value.split(',')
                if '' in string1:
                    string1.remove('')
                if len(value.split(',')) > 1:
                    for item in string1:
                        request_string += f' ({key}= "{item}") OR'
                    request_string = request_string[0:-2]
                    request_string += ' OR '
                else:
                    request_string += f'({key}= "{item}") AND'

        request_string = request_string[0:-3]
        request_string += ' AND quantity > 0 and on_sale=1'
        cursor.execute(request_string)
        results = cursor.fetchall()

        template = []
        for list in results:
            item = \
                dict({
                    'product_id': list[0],
                    'img_src': list[1],
                    'processor': list[2],
                    'frequency': list[3],
                    'socket': list[4],
                    'cores': list[5],
                    'threads': list[6],
                    'ram_size': list[7],
                    'ram_type': list[8],
                    'price': list[9],
                })
            template.append(item)
            item = dict()
    else:
        request_string += ' WHERE quantity > 0 AND on_sale=1'
        cursor.execute(request_string)
        results = cursor.fetchall()

        template = []
        for list in results:
            item = \
                dict({
                    'product_id': list[0],
                    'img_src': list[1],
                    'processor': list[2],
                    'frequency': list[3],
                    'socket': list[4],
                    'cores': list[5],
                    'threads': list[6],
                    'ram_size': list[7],
                    'ram_type': list[8],
                    'price': list[9],
                })
            template.append(item)
            item = dict()

    return render_template("catalog.html", template=template)


@app.route('/reserved_board', methods=['POST', 'GET'])
def reserved_board():
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
    )
    cursor = connection.cursor()

    data = request.get_json()  # list [1,4,2]

    ##check if product exists in database
    query = 'SELECT * FROM products WHERE ('
    for i in data:
        query += (f'product_id = {i} OR ')
    query = query[0:-3]
    query += ') AND quantity > 0 AND on_sale = 1'
    cursor.execute(query)
    result = cursor.fetchall()

    if (len(result) != len(data)):
        error = dict({'error': '1'})  # product or products are not exists
        return (error)
    else:
        ## generation of new personal_number.
        personal_num = random.randint(00000, 99999)
        query = (f'SELECT personal_num from reservations WHERE personal_num = {personal_num}')
        cursor.execute(query)
        result = cursor.fetchall()
        while len(result) != 0:
            personal_num = random.randint(00000, 99999)
            cursor.execute(query)
            result = cursor.fetchall()

        query = (f"INSERT INTO reservations (product_id, personal_num) VALUES")
        for i in data:
            query += (f'({i},"{personal_num}"),')
        query = query[0:-1]
        cursor.execute(query)
        connection.commit()
        data2 = {'personal_num': personal_num}

        #minus one product in database
        query = 'UPDATE products SET quantity = quantity - 1 WHERE product_id IN ('
        for i in data:
            query += f'{i},'

        query = query[0:-1]
        query += ')'
        cursor.execute(query)
        connection.commit()

        return data2


######## catalog.html end ####################################################################################

######## maintenance.html ####################################################################################
@app.route("/maintenance", methods=['POST', 'GET'])
def maintenance():
    if request.method == 'GET':
        return render_template("maintenance.html")

    if request.method == 'POST':

        email = request.form.get('email')
        name = request.form.get('name')
        tel = request.form.get('tel')
        problem = request.form.get('problem')

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return 'error'

        if not name:
            return 'error'

        if not (tel.isdigit() and len(tel) == 11):
            return 'error'

        if not problem:
            return 'error'

        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
        )

        cursor = connection.cursor()

        query = (f"INSERT INTO orders"
                 f" (email, name, tel, problem)"
                 f" VALUES('{email}', '{name}', '{tel}','{problem}')")
        cursor.execute(query)
        connection.commit()

        return 'success'


####### maintenance.html end ####################################################################################

######## admin panel ####################################################################################
@app.route("/admin", methods=['POST', 'GET'])
def admin():

    def admin_actions(action):

        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
        )
        cursor = connection.cursor()

        if int(action) == 1:  # add new board
            try:
                img = request.files['img']
                processor = request.form['processor']
                frequency = request.form['frequency']
                socket = request.form['socket']
                cores = request.form['cores']
                threads = request.form['threads']
                ram_size = request.form['ram_size']
                ram_type = request.form['ram_type']
                price = request.form['price']
                quantity = request.form['quantity']
            except Exception as err:
                print('error', err)
                return 'error'

            pattern = r'^\d+(?:.\d+)?$'
            if not re.match(pattern, frequency):
                return 'error'

            if not cores.isdigit():
                return 'error'

            if not threads.isdigit():
                return 'error'

            if not ram_size.isdigit():
                return 'error'

            if not price.isdigit():
                return 'error'

            if not quantity.isdigit():
                return 'error'

            ### find max id for img_src (5.jpg or 3.jpg)
            query = ("SELECT MAX(product_id) AS max_product_id FROM products")
            cursor.execute(query)
            result = cursor.fetchall()[0][0] + 1

            img_src = f'{result}.jpg'
            try:
                query = (f"INSERT INTO products "
                         f"(img_src, "
                         f"processor, "
                         f"frequency, "
                         f"socket, "
                         f"cores, "
                         f"threads, "
                         f"ram_size, "
                         f"ram_type, "
                         f"price, "
                         f"quantity)"
                         f" VALUES('{img_src}', "
                         f"'{processor}', "
                         f"'{frequency}', "
                         f"'{socket}', "
                         f"'{cores}', "
                         f"'{threads}', "
                         f"'{ram_size}', "
                         f"'{ram_type}', "
                         f"'{price}', "
                         f"'{quantity}')")

                img.save(f'static/IMG/products/{img_src}')

                cursor.execute(query)
                connection.commit()
            except Exception as err:
                print('error 2', err)

            return 'success'

        if int(action) == 2:  ## change info about board

            connection = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
            )
            cursor = connection.cursor()

            try:
                price = request.form['price']
                quantity = request.form['quantity']
                delete = request.form['delete']
                product_id = request.form['product_id']
            except Exception as err:
                print('error ', err)
                return 'error'

            query = (f'UPDATE products '
                     f'SET price="{price}", '
                     f'quantity="{quantity}", '
                     f'on_sale="{int(not delete)}" '
                     f'WHERE product_id = {product_id}')

            cursor.execute(query)
            connection.commit()
            return 'success'

        if int(action) == 3: # order status
            connection = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
            )
            cursor = connection.cursor()

            order_id = request.form['order_id']
            status = request.form['status']

            query = f'UPDATE orders SET status={status} WHERE order_id={order_id}'
            cursor.execute(query)
            connection.commit()
            return 'success'

        if int(action) == 4: # reservations status
            connection = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
            )
            cursor = connection.cursor()

            personal_num = request.form['personal_num']
            status = request.form['status']

            if status != 2:
                query = f'UPDATE reservations SET status={status} WHERE personal_num={personal_num}'
            else:
                query = f'UPDATE reservations SET quantity=quantity + 1 WHERE personal_num={personal_num}'

                cursor.execute(query)
                connection.commit()

                query = f'UPDATE reservations SET status={status} WHERE personal_num={personal_num}'

            cursor.execute(query)
            connection.commit()
            return 'success'



    ####################################################################
    ##### end of admin actions func ####################################
    ####################################################################

    if not 'isAdmin' in session:
        try:

            login = request.form['login']
            password = request.form['password']

            if login == 'admin' and password == '123':
                session['isAdmin'] = 1
                return redirect('/admin')
        except Exception as err:
            print(f'error 1: {err}')

        return render_template('login.html')


    else:

        if 'action' in request.form:
            return (admin_actions(request.form.get('action')))

        ########### boards part ###############################

        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
        )

        cursor = connection.cursor()
        query = ("SELECT product_id, "
                 "img_src, "
                 "processor, "
                 "frequency, "
                 "socket, "
                 "cores, "
                 "threads, "
                 "ram_size, "
                 "ram_type, "
                 "price, "
                 "quantity,"
                 "on_sale "
                 "FROM products "
                 "ORDER BY on_sale DESC, product_id")

        cursor.execute(query)
        results = cursor.fetchall()

        products_arr = []
        for list in results:
            item = \
                dict({
                    'product_id': list[0],
                    'img_src': list[1],
                    'processor': list[2],
                    'frequency': list[3],
                    'socket': list[4],
                    'cores': list[5],
                    'threads': list[6],
                    'ram_size': list[7],
                    'ram_type': list[8],
                    'price': list[9],
                    'quantity': list[10],
                    'on_sale': list[11]
                })
            products_arr.append(item)
            item = dict()

        ########### orders part ###############################

        query = ("SELECT email, "
                 "name, "
                 "tel, "
                 "problem, "
                 "date, "
                 "status, "
                 "order_id "
                 "FROM orders "
                 "REVERSE LIMIT 30")

        cursor.execute(query)
        results = cursor.fetchall()

        orders_arr = []
        for list in results:
            item = \
                dict({
                    'email': list[0],
                    'name': list[1],
                    'tel': list[2],
                    'problem': list[3],
                    'date': list[4],
                    'status': list[5],
                    'order_id': list[6]
                })
            orders_arr.append(item)
            item = dict()

        ########### reservations part ###############################
        query = ("SELECT personal_num, "
                 "date, "
                 "status, "
                 "img_src, "
                 "processor, "
                 "frequency, "
                 "socket, "
                 "cores, "
                 "threads, "
                 "ram_size, "
                 "ram_type, "
                 "price, "
                 "quantity,"
                 "on_sale "
                 "FROM combined_reservations "
                 "REVERSE LIMIT 30")

        cursor.execute(query)
        results = cursor.fetchall()

        reservations_arr = []
        for list in results:
            item = \
                dict({
                    'personal_num': list[0],
                    'date': list[1],
                    'status': list[2],
                    'img_src': list[3],
                    'processor': list[4],
                    'frequency': list[5],
                    'socket': list[6],
                    'cores': list[7],
                    'threads': list[8],
                    'ram_size': list[9],
                    'ram_type': list[10],
                    'price': list[11],
                    'quantity': list[12],
                    'on_sale': list[13]
                })
            reservations_arr.append(item)
            item = dict()

        return render_template("admin.html",
                               orders_template=orders_arr,
                               products_template=products_arr,
                               reservations_template=reservations_arr)


######## admin panel end ####################################################################################

##################### DO NOT TOUCH #####################
if __name__ == "__main__":
    # app.run( host='192.168.0.105',debug=True, port=5000)
    app.run(debug=True, port=5000)
#######################################################
