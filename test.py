import psycopg2
from flask import Flask, render_template, request
app = Flask(__name__)
conn=psycopg2.connect(
                      host='localhost',
                      user='tert',
                      password='Teratra14',
                      dbname='postgres',
                      )

@app.route('/', methods=['GET','POST'])
def hello():
    automobile=[]
    
    if request.method=='POST':
        cur=conn.cursor()
        
        harp=request.form['harp']
        cur.execute("SELECT * FROM automobile WHERE name LIKE %s;",('%' + harp + '%',))
        automobile=cur.fetchall()

        cur.close()
        conn.close()
        
    return render_template('auto.html', automobile=automobile)



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=80)

