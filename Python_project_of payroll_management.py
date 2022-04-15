#first create a flask application to perform below operation om payroll

#A] Insertion(Save Data):

from flask import Flask,render_template,request,redirect
import pymysql


app=Flask(__name__)

@app.route('/')
def index():
    return render_template("Employee_Entry.html")


          
@app.route('/insertrecord',methods=["POST"])
def insert():
    id=int(request.form["id"])
    n=request.form["Employee_Name"]
    a=request.form["Employee_Age"]
    c=request.form["Employee_City"]
    cont=request.form["Contact"]
    sal=int(request.form["Employee_Salary"])
    email=request.form["Employee_email"]

    
    if sal<50000:
        HR=sal*5/100
        Medical=sal*6/100
    else:
        HR=sal*6/100
        Medical=sal*7/100
    GP=sal+HR+Medical   #GP means Gross Pay

    
    #first create connection string
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',db='payroll_management')
    except Exception as e:
        msg="Connection Error"

    else:
        msg="Connection Create Successfully"

    #fire insert query
    query="INSERT into employee_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(id,n,a,c,cont,sal,email,HR,Medical,GP)   #val is a tuple

    #create cursor for run the sql query
    cur=conn.cursor()

    #query run then use inbuilt method Execute(): it is define in cursor
    #call with object of cursor
    try:
        cur.execute(query,val)
    except Exception as e:
        msg="Query Error"

    else:
        msg="Record Insert Successfully"
        conn.commit()
        conn.close()

    return render_template("result.html",msg=msg)


#Showrecord(show data):
@app.route('/showrecord')
def show():
    #first create a connection string
    
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',db='payroll_management')
    except Exception as e:
        msg="Connection Error"

    else:
        msg="Connection Create Successfully"

    #fire select query
    query="select*from employee_details"
    #create cursor for run the sql query
    cur=conn.cursor()

    #query run then use inbuilt method Execute(): it is define in cursor
    #call with object of cursor
    try:
        cur.execute(query)
    except Exception as e:
        msg="Query Error"

    else:
        result=cur.fetchall()
        conn.commit()
        conn.close()

    return render_template("PEmployee_show.html",result=result)

#Searchrecord(Search Data):
@app.route('/search/<int:id>')
def search(id):
    
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',db='payroll_management')
    except Exception as e:
        msg="Connection Error"

    else:
        msg="Connection Create Successfully"

    
    cur=conn.cursor()
    query="select*FROM EMPLOYEE_DETAILS where id=%s"

    cur.execute(query,id)
    result=cur.fetchall()
    conn.commit()
    conn.close()
    if result:#condition true
        return render_template("PEmployee_search.html",result=result)
    else:
        msg="Record Not Found"
        return render_template("result.html",msg=msg)
    return redirect('/showrecord')



# Updaterecord(Update Data):
@app.route('/update/<int:id>')
def update(id):
    
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',db='payroll_management')
    except Exception as e:
        msg="Connection Error"

    else:
        msg="Connection Create Successfully"

    
    cur=conn.cursor()
    query="select*FROM EMPLOYEE_DETAILS where id=%s"

    cur.execute(query,id)
    result=cur.fetchall()
    conn.commit()
    conn.close()
    if result:#condition true
        return render_template("PEmployee_update.html",result=result)
    else:
        msg="Record Not Found"
        return render_template("result.html",msg=msg)
@app.route('/updaterecord',methods=['POST'])
def updaterecord():
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',db='payroll_management')
    except Exception as e:
        msg="Connection Error"

    else:
        msg="Connection Create Successfully"
    msg=''
    if request.method=='POST':
        data=request.form
        id=data['id']
        name=data['name']
        age=data['age']
        city=data['city']
        cont=data['contact']
        sal=data['salary']
        email=data['email']

        val=(name,age,city,cont,sal,email,id)
        cur=conn.cursor()
        query="update employee_details set Employee_Name=%s,Employee_Age=%s,Employee_City=%s,Contact=%s,Employee_Salary=%s,Employee_email=%s where id=%s"

        cur.execute(query,val)

        conn.commit()
        msg="Employee Record Updated!"
        return redirect('/showrecord')
    return render_template('PEmployee_update.html')

#Deleterecord(Delete Data):
@app.route('/delete/<int:id>')
def delete(id):
    
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',db='payroll_management')
    except Exception as e:
        msg="Connection Error"

    else:
        msg="Connection Create Successfully"

    
    cur=conn.cursor()
    query="DELETE FROM EMPLOYEE_DETAILS where id=%s"

    cur.execute(query,id)
    
    conn.commit()
    conn.close()
    return redirect('/showrecord')

#main program
app.run(debug=True,use_reloader=False)

        
        
    
        
