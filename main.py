import time

from flask import Flask, render_template, request, redirect, session
import sqlite3 as sq
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '1b1966f2c38fe40af77584ebb9957d67a6b2637a'


def sort_db_request(db_array, length):
    index = 0
    requests_arr=[]
    while index < length:
        one_line = db_array[index]
        requests_arr.append({
        'product_id':one_line[0],
        'img_src':one_line[1],
        'processor':one_line[2],
        'frequency':one_line[3],
        'socket':one_line[4],
        'cores':one_line[5],
       'threads':one_line[6],
        'ram_size':one_line[7],
        'ram_type':one_line[8],
        'price':one_line[9],
        'quantity':one_line[10],
        'index': index,
        })
        index += 1
    return requests_arr

request_string = ''
def sql_request_correcting(key,value,previous_string):

    if value != None:

        arr = value.split(',')
        arr.remove('')

        if len(arr) == 1:
            previous_string += f"({key}='{arr[0]}')"  ### processor = 'something'
        elif len(arr) > 1:
            previous_string += '('
            for s in arr:
                previous_string += f"{key}='{s}' or " ### '(processor = 'onething' or processor = 'twothing')'
            previous_string = previous_string[0:-4]
            previous_string += ')'

        return previous_string + 'and'
    else:
        return previous_string

###### index.html ###################################################
@app.route("/")
def index():
    return render_template("index.html")
##### index.html end #####################################################

###### catalog.html ###################################################
@app.route("/catalog")
def catalog():
    processor = request.args.get('processor')
    frequency = request.args.get('frequency')
    socket = request.args.get('socket')
    cores = request.args.get('cores')
    threads = request.args.get('threads')
    ram_size = request.args.get('ram_size')
    ram_type = request.args.get('ram_type')
    request_string = ''
    # request_string = ("SELECT product_id, img_src, processor, frequency, socket, cores, threads, ram_size, ram_type, price, quantity FROM products WHERE")
    if(processor != None or frequency != None or socket != None or cores != None or threads != None or ram_size != None or ram_type != None):
        print("есть фильтры")
        request_string = sql_request_correcting("processor",processor,request_string)
        request_string = sql_request_correcting("frequency", frequency, request_string)
        request_string = sql_request_correcting("socket", socket, request_string)
        request_string = sql_request_correcting("cores", cores, request_string)
        request_string = sql_request_correcting("threads", threads, request_string)
        request_string = sql_request_correcting("ram_size", ram_size, request_string)
        request_string = sql_request_correcting("ram_type", ram_type, request_string)
        request_string = request_string[0:-3]
        with sq.connect("products.db") as con:
            cur = con.cursor()
            db_array = cur.execute(
            f"SELECT product_id, img_src, processor, frequency, socket, cores, threads, ram_size, ram_type, price, quantity FROM products WHERE {request_string}").fetchall()
            length = cur.execute(f"SELECT count(*) from products WHERE {request_string}").fetchall()
            length = length[0][0]

        template =  sort_db_request(db_array,length)
        zero_requests = ''
        if len(template) == 0:
            zero_requests = ("Нет результата. Попробуйте поменять фильтры")
        return render_template("catalog.html", template=template, zero_requests=zero_requests)

    else:
        print('нет фильтров')

        with sq.connect("products.db") as con:
            cur= con.cursor()
            db_array = cur.execute("SELECT product_id, img_src, processor, frequency, socket, cores, threads, ram_size, ram_type, price, quantity FROM products").fetchall()
            length = cur.execute("SELECT count(*) from products").fetchall()
            length = length[0][0]

        template = sort_db_request(db_array,length)
        return render_template("catalog.html", template=template, zero_requests='')

@app.route('/reserved_board',methods=['POST','GET'])
def reserved_board():
    boards_id = request.form['id']
    boards_id = boards_id[0:-1]
    time = str(datetime.date(datetime.now()))
    time += '|'
    time += str(datetime.time(datetime.now()))
    time = time[0:-7]
    with sq.connect("products.db") as con:
        cur = con.cursor()
        query =(f"INSERT INTO reserved_boards (time, boards_id) VALUES('{time}','{boards_id}')")
        print(query)
        insert = cur.execute(query)
    return 'about:blank'

######## catalog.html end ####################################################################################

######## maintenance.html ####################################################################################
@app.route("/maintenance",methods=['POST','GET'])
def maintenance():
    return render_template("maintenance.html")

@app.route("/reg_form", methods=['POST'])
def reg_form():
    name = request.form['name']
    email = request.form['email']
    tel = request.form['tel']
    problem = request.form['problem']
    date = str(datetime.date(datetime.now()))
    date += ' | '
    date += str(datetime.time(datetime.now()))
    date = date[0:-7]
    with sq.connect("products.db") as con:
        cur = con.cursor()
        query =(f"INSERT INTO requests (name,email,tel,problem,date) VALUES('{name}','{email}',{tel}, '{problem}','{date}')")
        insert = cur.execute(query)

    return 'about:blank'
######## maintenance.html end ####################################################################################

######## admin panel ####################################################################################

@app.route("/login", methods=['GET','POST'])
def login_page():
    if 'isAdmin' in session:
        print('ты давно админ')
        print(session)
        return redirect('/admin')

    error = request.args.get('error')
    if (error == '1'):
        return render_template("login.html", error="*Неправильный логин или пароль")
    else:
        session['isAdmin'] = 1
        print('ты наконец стал админом')
        print(session)
        return render_template('login.html')


@app.route("/admin", methods=['POST'])
def admin():
    if request.method =="GET":
        return redirect('login')
    login = ''
    password = ''

    try:
        login = request.form['login']
        password = request.form['password']
    except:
        print("запрос без пароля")

    if login == "a" and password == "a" or session['isAdmin'] == 1:


        print('успешный вход по логину и паролю')

        ########### boards part ###############################

        with sq.connect("products.db") as con:
            cur= con.cursor()
            db_array = cur.execute("SELECT product_id, img_src, processor, frequency, socket, cores, threads, ram_size, ram_type, price, quantity FROM products").fetchall()
            length = cur.execute("SELECT count(*) from products").fetchall()
            length = length[0][0]

        product_template = sort_db_request(db_array,length)

        ########### requests part ###############################

        with sq.connect("products.db") as con:
            cur= con.cursor()
            db_array = cur.execute("SELECT name, email, tel, problem, date, viewed, request_id FROM requests REVERSE LIMIT 30").fetchall()
            length = cur.execute("SELECT count(*) from requests").fetchall()
        length = length[0][0]
        index = 0
        requests_arr=[]
        while index < length:
            one_line = db_array[index]

            if one_line[5] == 1:    #кортеж не даёт менять one_line[5] нужна другая переменная
                viewed = 0.5        # opacity: {{ viewed }} делает прозрачнее уже просмотренные заявки
            else:
                viewed = 1

            requests_arr.append({'name':one_line[0], 'email':one_line[1],'tel':one_line[2], 'problem':one_line[3],'date':one_line[4],'viewed':viewed, 'request_id':one_line[6]})
            index += 1
        requests_arr = requests_arr[::-1]

        ########### reserved_boards part ###############################

        with sq.connect("products.db") as con:
            cur= con.cursor()
            idArray = cur.execute("SELECT time, boards_id FROM reserved_boards REVERSE LIMIT 30").fetchall()

        idArray = list(idArray)
        index = 0
        while index < len(idArray):                     # если не сделать list(), не будет менять значения
            idArray[index] = list(idArray[index])
            idArray[index][1] = (idArray[index][1].split(','))
            ## вставить оператор удаления пустых значений

            index2 = 0
            while index2 < len(idArray[index][1]):                # Сравнение product_id из кортежа product_template и из списка idArray
            # for variable_from_idArray in idArray[index][1]:     # for не меняет переменные. бесполезный

                for item_from_tuple in product_template:  # Перебор по кортежу product_template

                    if int(idArray[index][1][index2]) == item_from_tuple.get('product_id'):
                        idArray[index][1][index2] = item_from_tuple
                        break
                index2 += 1

            index += 1
        idArray = idArray[::-1]
        #### return function ############

        return  render_template("admin.html", templates=requests_arr, product_template=product_template,reserved_boards_template=idArray)
    else:
        print("Неправильный логин или пароль")
        return redirect('/login?error=1')

@app.route("/new_board", methods=['POST','GET'])
def new_board():
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

    with sq.connect("products.db") as con:
        cur = con.cursor()
        product_id = cur.execute("SELECT seq from sqlite_sequence where name='products'").fetchall()
        product_id = product_id[0][0]

    product_id += 1
    img.save(f'static/IMG/products/{product_id}.jpg')
    img_src = f'{product_id}.jpg'
    sql_request_bd = f"(img_src,processor,frequency,socket,cores,threads,ram_size,ram_type,price,quantity) VALUES('{img_src}','{processor}','{frequency}','{socket}','{cores}','{threads}','{ram_size}','{ram_type}','{price}','{quantity}')"
    print(sql_request_bd)


    with sq.connect("products.db") as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO products {sql_request_bd}")

    return redirect('/maintenance')

@app.route('/change_board', methods=['POST','GET'])
def change_board():
    delete = request.form.getlist('del')
    quantity = request.form['quantity']
    price = request.form['price']
    product_id = request.form['product_id']
    if len(delete) > 0:
        with sq.connect("products.db") as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM products WHERE product_id={product_id}')
            print(f'DELETE FROM products WHERE product_id={product_id}')
    else:
        with sq.connect("products.db") as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE products SET quantity='{quantity}', price='{price}' WHERE product_id = '{product_id}'""")
            print(f"""UPDATE products SET quantity='{quantity}', price='{price}' WHERE product_id = '{product_id}'""")
    return redirect('/login')

@app.route('/request_is_viewed', methods=['POST','GET'])
def request_is_viewed():
    request_id = request.form['request_id']
    print(f"""UPDATE requests SET viewed='1' WHERE request_id='{request_id}'""")
    with sq.connect("products.db") as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE requests SET viewed='1' WHERE request_id='{request_id}'""")
    return redirect('/admin')

######## admin panel end ####################################################################################

##################### НЕ ТРОГАТЬ #####################
if __name__ == "__main__":
    # app.run( host='192.168.0.105',debug=True, port=5000)
    app.run(debug=True)
#######################################################
