from flask import Flask, render_template,request, redirect
import mysql.connector as msc
import os


db= msc.connect(user="root",passwd="root",auth_plugin='mysql_native_password')
cursor=db.cursor(buffered=True)
cursor.execute("USE PHARMACY_MANAGEMENT")

PEOPLE_FOLDER = os.path.join('static', 'people')
app=Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/', methods=['POST','GET'])
def login():
    full_loginbackground = os.path.join(app.config['UPLOAD_FOLDER'], 'login_image2.jpg')
    full_collegelogo = os.path.join(app.config['UPLOAD_FOLDER'], 'collegelogo.jpeg')
    if request.method == 'POST':
        uid=request.form['username']
        pwd=request.form['password']
        try:
            cursor.execute('SELECT * FROM OWNER WHERE OWNER_ID=\'%s\''%uid)
            c=0
            for t in cursor:
                c+=1;
            if c!=0:
                return redirect('/owner')
        
            cursor.execute('SELECT * FROM EMPLOYEE WHERE EMP_ID=\'%s\''%uid)
            c=0
            for t in cursor:
                c+=1
            if c!=0:
                return redirect('/employee')
            
            cursor.execute('SELECT * FROM DOCTOR WHERE DOC_ID=\'%s\''%uid)
            c=0
            for t in cursor:
                c+=1
            if c!=0:
                return redirect('/doctor')
                    
        except:
            return redirect('/')
        
    else:
        full_loginbackground = os.path.join(app.config['UPLOAD_FOLDER'], 'login_image2.jpg')
        full_collegelogo = os.path.join(app.config['UPLOAD_FOLDER'], 'collegelogo.jpeg')
        return render_template('login.html',user_background = full_loginbackground,user_collegelogo = full_collegelogo)


@app.route('/owner',methods=['POST','GET'])
def owner():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'home_page2.jpg')
    return render_template('owner.html',user_image = full_filename)


@app.route('/employee',methods=['POST','GET'])
def employee():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'home_page2.jpg')
    return render_template('employee.html',user_image = full_filename)


@app.route('/doctor',methods=['POST','GET'])
def doctor():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo1.jpg')
    return render_template('doctor.html',user_image = full_filename)


@app.route('/addemp',methods=['POST','GET'])
def addemp():
    
    if request.method == 'POST':
        fname=request.form['fname']
        lname=request.form['lname']
        eid=request.form['eid']
        mail=request.form['mail']
        ph=request.form['ph']
        dob=request.form['dob']
        cursor.execute(r"INSERT INTO EMPLOYEE VALUES('%s','%s',%s,'%s','%s','%s')"%(fname,lname,eid,mail,ph,dob))
        db.commit()
        return redirect('/empo')
    else:
        return render_template('addemployee.html')


@app.route('/empo',methods=['POST','GET'])
def empo():
   
    cursor.execute('SELECT * FROM EMPLOYEE')
    tasks=cursor.fetchall()
    return render_template('viewemployeeo.html',tasks=tasks)


@app.route('/delempo/<int:eid>', methods=['POST', 'GET'])
def delempo(eid):
    
    cursor.execute(r"DELETE FROM EMPLOYEE WHERE EMP_ID=%d" % (eid))
    db.commit()
    return redirect('/empo')


@app.route('/upempo/<int:eid>',methods=['POST','GET'])
def upempo(eid):
    
    cursor.execute('SELECT * FROM EMPLOYEE WHERE EMP_ID=%d' % eid)
    tasks = cursor.fetchone()
    if request.method == 'POST':
        fname=request.form['fname']
        lname=request.form['lname']
        mail=request.form['mail']
        ph=request.form['ph']
        dob=request.form['dob']
        cursor.execute(r"UPDATE EMPLOYEE SET F_NAME='%s',L_NAME='%s',EMAIL='%s',PHONE='%s',DOB='%s' WHERE EMP_ID='%s'" %(fname,lname,mail,ph,dob,eid))
        db.commit()
        return redirect("/empo")
    else:
        return render_template('upemployee.html',tasks = tasks)


@app.route('/requiremento',methods=['POST','GET'])
def requiremento():

    cursor.execute('SELECT * FROM REQUIREMENT')
    tasks = cursor.fetchall()
    return render_template('requiremento.html',tasks=tasks)


@app.route('/addrequiremento',methods=['POST','GET'])
def addrequiremento():
   
    if request.method == 'POST':
        did = request.form['did']
        dname=request.form['dname']
        quantity=request.form['quantity']
        cost=request.form['cost']
        sup=request.form['sup']
        manu = request.form['manu']
        if(check_did(did)):
            sentence = 'Drug detail not available. Please add drug details and complete this process'
            return render_template('addrequiremento.html',sentence = sentence)
        if(check_did_available(did)):
            sentence = 'Still stock is available. Raise new request for after completion exciting stock'
            return render_template('addrequiremento.html',sentence = sentence)
        cursor.execute(r"INSERT INTO REQUIREMENT (D_ID,D_NAME,QUANTITY,COST,SUPPLIER,MANUFACTURER) VALUES('%s','%s','%s','%s','%s','%s')"%(did,dname,quantity,cost,sup,manu))
        db.commit()
        return redirect('/requiremento')
    else:
        return render_template('addrequiremento.html')



@app.route('/uprequiremento/<int:did>',methods=['POST','GET'])
def uprequiremento(did):

    cursor.execute('SELECT * FROM REQUIREMENT WHERE D_ID=%d' % did)
    tasks = cursor.fetchone()
    if request.method == 'POST':
        quantity=request.form['quantity']
        sup=request.form['sup']
        manu = request.form['manu']
        cursor.execute(r"UPDATE REQUIREMENT SET QUANTITY='%s',SUPPLIER='%s',MANUFACTURER='%s' WHERE D_ID = '%s'"%(quantity,sup,manu,did))
        db.commit()
        return redirect('/requiremento')
    else:
        return render_template('uprequiremento.html',tasks = tasks)


@app.route('/upstocka/<float:cost>',methods=['POST','GET'])
def upstocka(cost):

    cursor.execute('SELECT * FROM STOCK WHERE COST=%d' % cost)
    tasks = cursor.fetchone()
    if request.method == 'POST':
        num=request.form['quantity']
        cursor.execute(r"UPDATE STOCK SET QUANTITY = %s WHERE COST = %f"%(num,cost))
        db.commit()
        return redirect('/stocka')
    else:
        return render_template('upstocka.html', tasks=tasks)


@app.route('/delrequiremento/<int:did>',methods=['POST','GET'])
def delrequiremento(did):
    
    cursor.execute(r"DELETE FROM REQUIREMENT WHERE D_ID=%d"%(did))
    db.commit()
    return redirect('/requiremento')


@app.route('/costupdate/<int:did>',methods=['POST','GET'])
def costupdate(did):

    cursor.execute('SELECT * FROM REQUIREMENT WHERE D_ID=%d' % did)
    tasks = cursor.fetchone()
    if request.method == 'POST':
        num=request.form['cost']
        #print(num)
        cursor.execute(r"UPDATE REQUIREMENT SET COST = %s WHERE D_ID = %d"%(num,did))
        db.commit()
        return redirect('/requiremento')
    else:
        return render_template('costupdate.html',tasks = tasks)

@app.route('/stockreceived/<int:did>',methods=['POST','GET'])
def stockreceived(did):
    
    cursor.execute(r"SELECT * FROM REQUIREMENT WHERE D_ID=%d"%(did))
    tasks = cursor.fetchone()
    did = tasks[0]
    dname= tasks[1]
    quantity= tasks[2]
    cost=tasks[3]
    sup=tasks[4]
    manu = tasks[5]
    cursor.execute(r"INSERT INTO STOCK (D_ID,D_NAME,QUANTITY,COST,SUPPLIER,MANUFACTURER) VALUES('%s','%s','%s','%s','%s','%s')"%(did,dname,quantity,cost,sup,manu))
    cursor.execute(r"DELETE FROM REQUIREMENT WHERE D_ID=%s"%(did))
    db.commit()
    return redirect('/requiremento')



    
@app.route('/requiremente',methods=['POST','GET'])
def requiremente():
    
    cursor.execute('SELECT * FROM REQUIREMENT')
    tasks = cursor.fetchall()
    return render_template('requiremente.html',tasks=tasks)


@app.route('/addrequiremente',methods=['POST','GET'])
def addrequiremente():
    
    if request.method == 'POST':
        did = request.form['did']
        dname=request.form['dname']
        quantity=request.form['quantity']
        cost=request.form['cost']
        sup=request.form['sup']
        manu = request.form['manu']
        if(check_did(did)):
            sentence = 'Drug detail not available. Please add drug details and complete this process'
            return render_template('addrequiremente.html',sentence = sentence)
        if(check_did_available(did)):
            sentence = 'Still stock is available. Raise new request for after completion exciting stock'
            return render_template('addrequiremente.html',sentence = sentence)
        cursor.execute(r"INSERT INTO REQUIREMENT (D_ID,D_NAME,QUANTITY,COST,SUPPLIER,MANUFACTURER) VALUES('%s','%s','%s','%s','%s','%s')"%(did,dname,quantity,cost,sup,manu))
        db.commit()
        return redirect('/requiremente')
    else:
        return render_template('addrequiremente.html')


@app.route('/uprequiremente/<int:did>',methods=['POST','GET'])
def uprequiremente(did):
    
    cursor.execute('SELECT * FROM REQUIREMENT WHERE D_ID=%d' % did)
    tasks = cursor.fetchone()
    if request.method == 'POST':   
        quantity=request.form['quantity']
        sup=request.form['sup']
        manu = request.form['manu']
        cursor.execute(r"UPDATE REQUIREMENT SET QUANTITY='%s',SUPPLIER='%s',MANUFACTURER='%s' WHERE D_ID = '%s'"%(quantity,sup,manu,did))
        db.commit()
        return redirect('/requiremente')
    else:
        return render_template('uprequiremente.html',tasks = tasks)



@app.route('/delrequiremente/<int:did>',methods=['POST','GET'])
def delrequiremente(did):
    
    cursor.execute(r"DELETE FROM REQUIREMENT WHERE D_ID=%d"%(did))
    db.commit()
    return redirect('/requiremente')


@app.route('/stocke',methods=['POST','GET'])
def stocke():
   
    cursor.execute('SELECT * FROM STOCK')
    tasks = cursor.fetchall()
    return render_template('stocke.html', tasks=tasks)

@app.route('/stocko',methods=['POST','GET'])
def stocko():
   
    cursor.execute('SELECT * FROM STOCK')
    tasks = cursor.fetchall()
    return render_template('stocko.html',tasks=tasks)

@app.route('/updatestock/<int:did>',methods=['POST','GET'])
def updatestock(did):
    
    cursor.execute('SELECT * FROM STOCK WHERE D_ID=%d' % did)
    tasks = cursor.fetchone()
    if request.method == 'POST':   
        quantity=request.form['quantity']
        sup=request.form['sup']
        manu = request.form['manu']
        cursor.execute(r"UPDATE STOCK SET QUANTITY='%s',SUPPLIER='%s',MANUFACTURER='%s' WHERE D_ID = '%s'"%(quantity,sup,manu,did))
        db.commit()
        return redirect('/stocko')
    else:
        return render_template('updatestock.html',tasks = tasks)


@app.route('/delstock/<int:did>',methods=['POST','GET'])
def delstock(did):
    
    cursor.execute(r"DELETE FROM STOCK WHERE D_ID=%d"%(did))
    db.commit()
    return redirect('/stocko')


@app.route('/costupdatestock/<int:did>',methods=['POST','GET'])
def costupdatestock(did):
   
    cursor.execute('SELECT * FROM STOCK WHERE D_ID=%d' % did)
    tasks = cursor.fetchone()
    if request.method == 'POST':
        num=request.form['cost']
        #print(num)
        cursor.execute(r"UPDATE STOCK SET COST = %s WHERE D_ID = %d"%(num,did))
        db.commit()
        return redirect('/stocko')
    else:
        return render_template('costupdatestock.html',tasks = tasks)







@app.route('/addstock',methods=['POST','GET'])
def addstock():
    
    if request.method == 'POST':
        dname=request.form['dname']
        quantity=request.form['quantity']
        cost=request.form['cost']
        sup=request.form['sup']
        cursor.execute(r"INSERT INTO STOCK VALUES('%s',%s,%s,'%s')"%(dname,quantity,cost,sup))
        db.commit()
        return redirect('/stocko')
    else:
        return render_template('addstock.html')




@app.route('/prescripo',methods=['POST','GET'])
def prescripo():
    
    if request.method == 'POST':
        docname = request.form['Doctor Name']
        docid = request.form['Doctor ID']
        pname = request.form['Patient Name']
        page = request.form['Patient Age']
        pphone = request.form['Patient Phone']
        eid = request.form['Employee id']
        pid = request.form['Prescription id']
        dna = request.form['Drug Name']
        quantity = request.form['Quantity']
        dose = request.form['Dose']
        did = request.form['Drug ID']
        date = request.form['Date']
        
        if(check_pid_employee_owner(pid)):
            sentence = 'Prescription ID is not available. Please add correct prescription details and complete this process'
            return render_template('prescripo.html',sentence = sentence)
        
        if(check_docid(docid)):
            sentence = 'Doctor ID is invalid. Please enter correct Doctor ID'
            return render_template('prescripo.html',sentence = sentence)
        
        
        if(check_did(did)):
            sentence = 'Drug detail not available. Please add drug details and complete this process'
            return render_template('prescripo.html',sentence = sentence)
        if(check_eid(eid)):
            sentence = 'Employee detail not available. Please add employee details and complete this process'
            return render_template('prescripo.html',sentence = sentence)
        if(check_quantity(quantity,did)):
            sentence = 'Required quantity not available. Please order for requirement details and complete this process'
            return render_template('prescripo.html',sentence = sentence)
        
        cursor.execute("SELECT * FROM STOCK where D_ID = '%s'" % (did))
        tasks=cursor.fetchone()
        price = str(int(tasks[3])*int(quantity))
        cursor.execute("INSERT INTO PRESCRIPTION VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (eid,pid, quantity, dose, did,dna,pname,date,page,pphone))
        cursor.execute("INSERT INTO INVOICE VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (eid,pid, quantity, dose, did,dna,pname,date,page,pphone,price))
        cursor.execute(r"UPDATE STOCK SET QUANTITY=QUANTITY-'%s' WHERE D_ID='%s'"%(quantity,did))
        db.commit()
        return redirect("/invo")
    else:
        return render_template('prescripo.html')

@app.route('/prescripe',methods=['POST','GET'])
def prescripe():
    
    if request.method == 'POST':
        docname = request.form['Doctor Name']
        docid = request.form['Doctor ID']
        pname = request.form['Patient Name']
        page = request.form['Patient Age']
        pphone = request.form['Patient Phone']
        eid = request.form['Employee id']
        pid = request.form['Prescription id']
        dna = request.form['Drug Name']
        quantity = request.form['Quantity']
        dose = request.form['Dose']
        did = request.form['Drug ID']
        date = request.form['Date']
        
        if(check_pid_employee_owner(pid)):
            sentence = 'Prescription ID is not available. Please add correct prescription details and complete this process'
            return render_template('prescripe.html',sentence = sentence)
        
        if(check_docid(docid)):
            sentence = 'Doctor ID is invalid. Please enter correct Doctor ID'
            return render_template('prescripe.html',sentence = sentence)
        
        
        if(check_did(did)):
            sentence = 'Drug detail not available. Please add drug details and complete this process'
            return render_template('prescripe.html',sentence = sentence)
        if(check_eid(eid)):
            sentence = 'Employee detail not available. Please add employee details and complete this process'
            return render_template('prescripe.html',sentence = sentence)
        if(check_quantity(quantity,did)):
            sentence = 'Required quantity not available. Please order for requirment details and complete this process'
            return render_template('prescripe.html',sentence = sentence)
        
        
        cursor.execute("SELECT * FROM STOCK where D_ID = '%s'" % (did))
        tasks=cursor.fetchone()
        price = str(int(tasks[3])*int(quantity))
        cursor.execute("INSERT INTO PRESCRIPTION VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (eid,pid, quantity, dose, did,dna,pname,date,page,pphone))
        cursor.execute("INSERT INTO INVOICE VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (eid,pid, quantity, dose, did,dna,pname,date,page,pphone,price))
        cursor.execute(r"UPDATE STOCK SET QUANTITY=QUANTITY-'%s' WHERE D_ID='%s'"%(quantity,did))
        db.commit()
        return redirect("/inve")
    else:
        return render_template('prescripe.html',sentence = '')


@app.route('/prescripd',methods=['POST','GET'])
def prescripd():
    
    if request.method == 'POST':
        docname = request.form['Doctor Name']
        docid = request.form['Doctor ID']
        pname = request.form['Patient Name']
        page = request.form['Patient Age']
        pphone = request.form['Patient Phone']
        pid = request.form['Prescription ID']
        dna = request.form['Drug Name']
        quantity = request.form['Quantity']
        dose = request.form['Dose']
        date = request.form['Date']
        
        if(check_docid(docid)):
            sentence = 'Doctor ID is invalid. Please enter correct Doctor ID'
            return render_template('prescripd.html',sentence = sentence)
        if(check_pid(pid)):
            sentence = 'Prescription ID is already available. Please add New Prescription ID and complete this process'
            return render_template('prescripd.html',sentence = sentence)
        
        
        cursor.execute("INSERT INTO MASTER_PRESCRIPTION VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (docid,docname,pname,pid, page,quantity, dose,dna,date,pphone))
        
        db.commit()
        return redirect("/doctor")
    else:
        return render_template('prescripd.html')


def check_docid(docid):
    test = True
    cursor.execute('SELECT * FROM DOCTOR WHERE DOC_ID=%s' % str(docid))
    c=0
    for t in cursor:
        c+=1;
        if c!=0:
            test = False
    return test


def check_pid(pid):
    test = False
    cursor.execute('SELECT * FROM MASTER_PRESCRIPTION WHERE PRES_ID=%s' % str(pid))
    c=0
    for t in cursor:
        c+=1;
        if c!=0:
            test = True
    return test

def check_pid_employee_owner(pid):
    test = True
    cursor.execute('SELECT * FROM MASTER_PRESCRIPTION WHERE PRES_ID=%s' % str(pid))
    c=0
    for t in cursor:
        c+=1;
        if c!=0:
            test = False
    return test


def check_did(did):
    
    test = True
    cursor.execute('SELECT * FROM DRUG WHERE D_ID=%d' % int(did))
    c=0
    for t in cursor:
        c+=1;
        if c!=0:
            test = False
    return test

def check_eid(eid):
    test = True
    cursor.execute('SELECT * FROM EMPLOYEE WHERE EMP_ID=%d' % int(eid))
    c=0
    for t in cursor:
        c+=1;
        if c!=0:
            test = False
    return test

def check_quantity(quantity,did):
    test = False
    cursor.execute('SELECT * FROM STOCK WHERE D_ID=%d' % int(did))
    tasks = cursor.fetchone()
    if((int(tasks[2])-int(quantity)) < 0):
        test = True
    return test

def check_did_available(did):
    test = False
    cursor.execute('SELECT * FROM STOCK WHERE D_ID=%d' % int(did))
    c=0
    for t in cursor:
        c+=1;
        if c!=0:
            test = True
    return test



@app.route('/invo',methods=['POST','GET'])
def invo():
    
    cursor.execute('SELECT * FROM INVOICE')
    tasks=cursor.fetchall()
    return render_template('invo.html',tasks=tasks)

@app.route('/inve',methods=['POST','GET'])
def inve():
   
    cursor.execute('SELECT * FROM INVOICE')
    tasks = cursor.fetchall()
    return render_template('inve.html', tasks=tasks)



@app.route('/viewdrugo',methods=['POST','GET'])
def viewdrugo():
    
    cursor.execute('SELECT * FROM DRUG')
    tasks=cursor.fetchall()
    return render_template('viewdrugo.html',tasks=tasks)

@app.route('/viewdruge',methods=['POST','GET'])
def viewdruge():
    
    cursor.execute('SELECT * FROM DRUG')
    tasks = cursor.fetchall()
    return render_template('viewdruge.html', tasks=tasks)



@app.route('/viewprescripd',methods=['POST','GET'])
def viewprescripd():
    
    cursor.execute('SELECT * FROM MASTER_PRESCRIPTION')
    tasks = cursor.fetchall()
    return render_template('viewprescripd.html', tasks=tasks)

@app.route('/delprescripd/<int:pid>',methods=['POST','GET'])
def delprescripd(pid):
    cursor.execute(r"DELETE FROM MASTER_PRESCRIPTION WHERE PRES_ID=%d"%(pid))
    db.commit()
    return redirect('/viewprescripd')



@app.route('/adddrugo',methods=['POST','GET'])
def adddrugo():
    
    if request.method == 'POST':
        did = request.form['did']
        dname=request.form['dname']
        sup=request.form['sup']
        manu = request.form['manu']
        uses = request.form['uses']
        side = request.form['side']
        cursor.execute(r"INSERT INTO DRUG (D_ID,D_NAME,SUPPLIER,MANUFACTURER,USES,SIDE_EFFECT) VALUES('%s','%s','%s','%s','%s','%s')"%(did,dname,sup,manu,uses,side))
        db.commit()
        return redirect('/viewdrugo')
    else:
        return render_template('adddrugo.html')


@app.route('/updrugo/<int:did>',methods=['POST','GET'])
def updrugo(did):
    cursor.execute('SELECT * FROM DRUG WHERE D_ID=%d' % did)
    tasks = cursor.fetchone()
    if request.method == 'POST':   
        sup=request.form['sup']
        manu = request.form['manu']
        uses = request.form['uses']
        side = request.form['side']
        cursor.execute(r"UPDATE DRUG SET USES='%s',SUPPLIER='%s',MANUFACTURER='%s',SIDE_EFFECT='%s' WHERE D_ID = '%s'"%(uses,sup,manu,side,did))
        db.commit()
        return redirect('/viewdrugo')
    else:
        return render_template('updrugo.html',tasks = tasks)



@app.route('/deldrugo/<int:did>',methods=['POST','GET'])
def deldrugo(did):
    cursor.execute(r"DELETE FROM DRUG WHERE D_ID=%d"%(did))
    db.commit()
    return redirect('/viewdrugo')




if __name__== '__main__':
    app.run(debug=True)