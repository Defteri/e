import psycopg2
from flask import Flask, render_template, request, redirect, flash, session
app = Flask(__name__)
app.secret_key='your_secret_key'

@app.route('/', methods=['GET','POST'])
def hello():

    automobile=[]
    conn=psycopg2.connect(
                      host='localhost',
                      user='tert',
                      password='Teratra14',
                      dbname='postgres',
                      )
    
    if request.method=='POST':
        cur=conn.cursor()
        
        harp=request.form['harp']
        cur.execute("SELECT * FROM automobile WHERE name LIKE %s;",('%' + harp + '%',))
        automobile=cur.fetchall()

        cur.close()
    
    conn.close()    
    return render_template('auto.html', automobile=automobile)

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/login')
    
    username=session['username']

    conn=psycopg2.connect(
        host='localhost',
        user='tert',
        password='Teratra14',
        dbname='postgres',
        )
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s",(username,))
    user=cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return render_template('profile.html', user=user)
    else:
        flash('Ошибка')
        return redirect('/auto')
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
    
        conn=psycopg2.connect(
            host='localhost',
            user='tert',
            password='Teratra14',
            dbname='postgres',
            )
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);",(username, password))
        conn.commit()

        cur.close()
        conn.close()

        flash('Регистрация прошла')
        return redirect('/login')
        
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        conn=psycopg2.connect(
                      host='localhost',
                      user='tert',
                      password='Teratra14',
                      dbname='postgres',
                      )
        cur=conn.cursor()

        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s",(username, password,))
        user=cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session['username']=username
            flash("Вы вошли")
            return redirect('/')
        else:
            flash("Неверный пользователь или пароль")
    return render_template('login.html')

@app.route('/logout')
def logout():
   session.pop('username', None)
   flash("Вы вышли из аккаунта")
   return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=80)

