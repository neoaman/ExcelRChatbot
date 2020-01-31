try:
    import urllib
    import json
    import os
    from flask import Flask,request,make_response,render_template,redirect,session
    import processing as ps
    import datetime
    from flask_sqlalchemy import SQLAlchemy
    from datetime import datetime
except Exception as e:
    print("Module not found {}".format(e))


app = Flask(__name__)
with open("config.json") as c:
    params = json.load(c)["params"]
app.config['SQLALCHEMY_DATABASE_URI'] = params['neomi_uri']
app.secret_key = 'super-secret-key'

db = SQLAlchemy(app)
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    course = db.Column(db.String(40),nullable=False)
    branch = db.Column(db.String(40),nullable=False)
    phone_num = db.Column(db.String(13),nullable=False)
    date = db.Column(db.String(12),nullable=True)
    email = db.Column(db.String(20),nullable=False)


@app.route('/')
def home():

    return render_template('aman.html')

@app.route('/webhook', methods=['POST'])
def webhook():

    if request.method == "POST":
        req = request.get_json(silent=True,force=True)
        # print(req)
        # This req will get the json output of the chatbot everyting
        # res will process the data 
        res = processRequest(req)
        res = json.dumps(res,indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

def processRequest(req):
    query_response = req['queryResult']
    # print(query_response)
    if query_response.get('action',None) == 'course_check':
        parameters = query_response.get('parameters')
        if query_response.get('fulfillmentText',None) != None:
            print(query_response.get('fulfillmentText',None))
            parameters = query_response.get('parameters')
            print(parameters)
            return query_response.get('fulfillmentText',None)
            # return "query_response.get('fulfillmentText',None)"
        if parameters.get('geo-city') != "":
            # print("I am Listening ")
            parameters = query_response.get('parameters')
            print(parameters)
            # print("Parameters Added")
            keys = ['geo-city','Course','Phone','Email']
            values = list(map(parameters.get, keys))
            """ Add to the database"""
            values,speech=ps.appointmentset(values)
            name = 'Unknown'
            course = values[1]
            branch = values[0]
            date = datetime.now()
            phone_num = values[2]
            email = values[3]
            print(values)
            entry = Contacts(name =name,course = course, branch = branch, phone_num = phone_num, email=email ,date=date )
            db.session.add(entry)
            db.session.commit()
            print(speech)
            print('success')
            """ Added to database"""
            return speech
    else:
        print('not yet')
    
    if query_response.get('action',None) == 'input.duration':
        if query_response.get('fulfillmentText',None) != None:
            print(query_response.get('fulfillmentText',None))
            return query_response.get('fulfillmentText',None)
        else:
            parameters = query_response.get('parameters',None)
            keys = ['Course']
            values = list(map(parameters.get, keys))
            return ps.courseduration(*values)
    
    if query_response.get('action',None) == 'course_fee':
        if query_response.get('fulfillmentText',None) != None:
            print(query_response.get('fulfillmentText',None))
            return query_response.get('fulfillmentText',None)
        else:
            parameters = query_response.get('parameters',None)
            keys = ['Course']
            values = list(map(parameters.get, keys))
            return ps.coursefees(*values)





@app.route("/admin",methods=['GET','POST'])
def adminpage():
     
    if ('user' in session and session['user'] == params['admin_user']):
        if request.method =='POST':
            branch = request.form.get('branch')
            sdate = request.form.get('startdate')
            edate = request.form.get('enddate')
            if sdate == "" and branch!='All':
                contactinfo = Contacts.query.filter_by(branch=branch).all()
            elif sdate !="" and edate !="" and branch =='All':
                contactinfo = Contacts.query.filter(Contacts.date.between(sdate,edate)).filter_by().all()
            elif sdate =="" and edate =="" and branch =='All':
                contactinfo = Contacts.query.filter_by().all()            
            else:
                contactinfo = Contacts.query.filter(Contacts.date.between(sdate,edate)).filter_by(branch=branch).all()
        else:
            contactinfo = Contacts.query.filter_by().all()
        return render_template('admin.html',info=contactinfo)
    else:
        return render_template('login.html')
    
@app.route("/delete/<int:sno>")
def delete(sno):
    del_post= Contacts.query.filter_by(sno=sno).first()
    db.session.delete(del_post)
    db.session.commit()
    return redirect("/admin")

@app.route("/login",methods=['GET','POST'])
def logIn():
    if ('user' in session and session['user'] == params['admin_user']):
        contactinfo = Contacts.query.filter_by(branch='Bengaluru').all()
        return render_template('admin.html',info=contactinfo)
    if request.method =='POST':
        passs  = request.form.get('password')
        uname = request.form.get('loginid')
        if (uname == params['admin_user'] and passs == params['admin_pass']) :
            session['user'] = uname
            contactinfo = Contacts.query.filter_by(branch='Bengaluru').all()
            return render_template('admin.html',info=contactinfo)
        else:

            return render_template('login.html', warn = "Wrong Id or Password")
        # Redirect to admin
    return render_template('login.html',params=params)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)