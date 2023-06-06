from flask import Flask,render_template, redirect, request
import pyrebase

app = Flask(__name__)

firebaseConfig={
    "apiKey": "AIzaSyDh5zkx_8ZB4MDplR4i0azSmGi2XWDLMkQ",
    "authDomain": "indianinventions-83bb1.firebaseapp.com",
    "projectId": "indianinventions-83bb1",
    "storageBucket": "indianinventions-83bb1.appspot.com",
    "messagingSenderId": "280958057822",
    "appId": "1:280958057822:web:8ff73f5a8e337f02e4a3cf",
    "measurementId": "G-YNN46XYPVF",
    "serviceAccount": "serviceAccount.json",
    "databaseURL": "https://indianinventions-83bb1-default-rtdb.firebaseio.com"
}

firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
auth=firebase.auth()
storage=firebase.storage()

@app.route('/',methods=["GET","POST"])
def index():
    if request.method=="POST":
        name=request.form["name"]
        category=request.form.get('category')
        if name and category:
            try:
                invention=db.child("Inventions").child(category).child(name).get()
                invention=dict(invention.val())
                inventions=[]
                inventions.append(invention)
                return render_template("searchResults.html",inventions=inventions)
            except:
                return redirect('/')
        elif category:
            try:
                inventions=db.child("Inventions").child(category).get()
                inventions=[invention.val() for invention in inventions.each()]
                return render_template("searchResults.html",inventions=inventions)
            except:
                return redirect('/')
    return render_template("index.html")

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]
        auth.create_user_with_email_and_password(username,password)
        return redirect('login')
    return render_template("signup.html")

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]
        try:
            auth.sign_in_with_email_and_password(username,password)
            return redirect('dashboard')
        except:
            return render_template("login.html")
    if auth.current_user:
        return redirect('dashboard')
    return render_template("login.html")

@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    user=auth.current_user
    if user:
        if user['email']=='admin@admin.com':
            if request.method=="POST":
                name=request.form["name"]
                inventor=request.form["inventor"]
                year=request.form["year"]
                details1=request.form["details1"]
                details2=request.form["details2"]
                category=request.form.get('category')
                image = request.files['image']
                img_name=name.replace(" ","")
                path=f"{category}/{img_name}.jpg"
                save_path=f"./static/images/{path}"
                image.save(save_path)
                data={"Name":name,"Inventor":inventor,"Year":year,"Details1":details1,
                      "Details2":details2,"Category":category,"Path":path}
                db.child("Inventions").child(category).child(name).set(data)
                return render_template("addInvention.html")
            return render_template("addInvention.html")
        return render_template("dashboard.html",user=user)
    else:
        return redirect('login')

@app.route('/logout')
def logout():
    auth.current_user=None
    return redirect('/')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return "contact"

@app.route('/searchResults')
def searchResults():
    return render_template("searchResults.html")


if __name__ == "__main__":
    app.run(port=8080)