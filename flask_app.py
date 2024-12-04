from flask import Flask, render_template, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Задайте URI для вашей БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=False, nullable=False)

# Создание базы данных и таблиц
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

# Функция для проверки email (валидация)
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

# Маршрут для обработки формы
@app.route('/submit', methods=['POST'])
def submit_form():
    # Получаем данные из формы
    email_input = request.form['textInput']

    # Удаляем лишние пробелы и преобразуем к нижнему регистру
    email = email_input.strip().lower()

    # Проверяем корректность email
    if not validate_email(email):
        return redirect(url_for('index'))

    # Проверяем, существует ли уже email в базе данных
    if User.query.filter_by(email=email).first():
        return redirect(url_for('index'))

    # Создаем новую запись
    new_user = User(email=email)
    
    # Добавляем запись в базу данных
    db.session.add(new_user)
    db.session.commit()
    
    # Перенаправляем на главную страницу или другую страницу
    #return redirect(url_for('index'))

    Users = User.query.all()
    Users_list = [
        {
            'id': user.id,
            'email': user.email,
        } for user in Users
    ]

    return Users_list

if __name__ == '__main__':
    app.run(debug=True)

# Преобразование к нижнему регистру: например EMAIL@gmail.com будет в базе данных как email@gmail.com
# Неккоректный эмейл в принципе не дает загрузить, а так должен перенаправлять на главную страницу
# Проверка на то, существует уже эмейл или нет: второй раз email@gmail.com не будет добавлен (возврвщает на главную страницк)