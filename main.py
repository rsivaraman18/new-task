from flask import Flask,render_template,request,flash
import sqlite3
app = Flask(__name__)
app.secret_key = '1234'





def createdb():
    con = sqlite3.connect('newtask.db')
    query1 = """
     CREATE TABLE IF NOT EXISTS Employees
            (emp_id INTEGER PRIMARY KEY,
            emp_name TEXT ,
            emp_dob TEXT,
            emp_address TEXT,
            emp_gender TEXT) """
    con.execute(query1)
    con.commit()
    con.close()
    print('Db successfully created')

createdb()





@app.route('/',methods=['POST',"GET"])
def index():
    try:
        if request.method=='POST':
            id = request.form['eid']
            name = request.form['ename']
            dob = request.form['edob']
            address = request.form['eaddress']
            gender = request.form['egender']

            print(id ,name,dob,address,gender)
            con = sqlite3.connect('newtask.db')
            cur = con.cursor()
            qry="INSERT INTO employees (emp_id,emp_name,emp_dob,emp_address,emp_gender) VALUES (?,?,?,?,?)"
            tup_word=(id,name,dob,address,gender)
            cur.execute(qry,tup_word)
            con.commit()
            flash('added Successfully','success')
    except:
        flash("ID already in use",'danger')
    return render_template('index.html')



@app.route('/view',methods=['POST',"GET"])
def view():
    return render_template("view.html")


@app.route('/view2',methods=['POST',"GET"])
def view2():
    if request.method=='POST':
        id = request.form['sid']
        con = sqlite3.connect('newtask.db')
        cur = con.cursor()
        try:
            q="SELECT * FROM employees WHERE emp_id=? "
            tup=(id,)
            cur.execute(q,tup)
            view= cur.fetchone()
            data = {'id':view[0],'name':view[1],'dob':view[2],'address':view[3],'gender':view[4],'error':''}
        except:
            data = {'error':'Enter Only valid ID'}
        return render_template('display.html',data =data)
    return render_template('view.html')


if __name__ == '__main__':
    app.run(debug=True)