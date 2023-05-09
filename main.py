from flask import Flask, request, redirect, render_template, make_response
import sqlite3


app = Flask(__name__)

# Создаем файл базы (если нет) и подключаемся
connection = sqlite3.connect('messages.sqlite', check_same_thread=False)

# Создаем курсор, специальный объект для взаимодействия с базой
cursor = connection.cursor()

# Выполняем команду создания таблицы
cursor.execute('''CREATE TABLE IF NOT EXISTS messages(
   id INTEGER PRIMARY KEY,
   user VARCHAR(32),
   date DATETIME,
   content TEXT);
''')


@app.route('/login', methods=["POST", "GET"])
def login():
    # if form is submited
    if request.method == 'POST':
        # record the user name
        response = make_response(redirect('/'))
        response.set_cookie('name', request.form.get('name'))
        # redirect to the main page
        return response
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    name = request.cookies.get('name')

    if not name:
        return redirect('/login')

    if request.method == 'POST':
        content = request.form['content']
        sql = 'INSERT INTO messages (user, date, content) VALUES (?, (datetime("now","localtime")), ?)'
        values = (name, content)
        cursor.execute(sql, values)

        # Подтверждаем изменение базы
        connection.commit()

        # Ответ сервера: успех
        return redirect('/')
    else:
        # Выполняем команду извлечения из таблицы всех сообщений
        cursor.execute('SELECT * FROM messages ORDER BY date DESC')

        # Считываем 7 сообщений
        messages = cursor.fetchmany(7)

        # Реверсируем сообщения
        messages.reverse()

        # Отдаем на фронт
        return render_template('index.html', messages=messages)


app.run(debug=True)
