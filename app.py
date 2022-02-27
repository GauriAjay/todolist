from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'todo'
mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()
    return render_template('inedx.html', students=data )

    
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        
        name = request.form['name']
        todolist = request.form['todolist']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, todolist) VALUES (%s, %s)", (name, todolist))
        mysql.connection.commit()
        return redirect('/')

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        todolist = request.form['todolist']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, todolist=%s
               WHERE id=%s
            """, (name, todolist, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))


if __name__=="__main__":
    app.run(debug=True)