from flask import Flask , render_template ,request ,session, logging,url_for , redirect , flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session , sessionmaker
import pymysql
import requests
from passlib.hash import sha256_crypt

engine = create_engine("mysql+pymysql://root:@localhost/cri")
db=scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)


@app.route("/home")
def home():
    data = requests.get("https://disease.sh/v2/countries/india?yesterday=true&strict=true")
    data_dict = data.json()

    return render_template('home.html' , data=data_dict)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/donate")
def donate():
    return render_template('donate.html')

@app.route("/register" , methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            db.execute("INSERT INTO users(name , email , password) VALUES (:name,:email,:password)",
                                        {"name":name,"email":email,"password":secure_password})
            db.commit()

            return redirect(url_for('login'))
        else:

            return render_template("register.html")

    return render_template("register.html")




@app.route("/plasma" , methods = ["GET","POST"])
def plasma():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        age = request.form.get("age")
        sex = request.form.get("sex")
        bg = request.form.get("bg")
        state = request.form.get("state")

        db.execute("INSERT INTO dplasma(Fname , Lname , age , sex , Blood_group , State) VALUES (:Fname,:Lname,:age , :sex , :Blood_group , :State)",
                                        {"Fname":fname, "Lname":lname,"age":age , "sex":sex , "Blood_group":bg , "State" :state })
        db.commit()

        return redirect(url_for('plasma'))
            #db.execute("INSERT INTO users(Fname , Lname , age , sex , Blood_group , State) VALUES (:Fname,:Lname,:age , :sex , :Blood_group , :State)",
            #                            {"Fname":Fname, "Lname":Lname,"age":age , "sex":sex , "Blood_group":Blood_group , "State" :State })
            #db.commit()

          #  return render_template("register.html")

    return render_template("plasma.html")

headings = ( "Name" , "Age" , "Sex" ,"Blood Group" , "State")
data = (
    ("John" , "35" , "Male" , "A+" , "Delhi" ),
    ("Stephen" , "41" , "Male" , "O+" , "London" ) )

@app.route("/requestplasma" , methods = ["GET","POST"])
def requestplasma():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        age = request.form.get("age")
        sex = request.form.get("sex")
        address = request.form.get("address")
        bg = request.form.get("bg")
        state = request.form.get("state")
        dcp = request.form.get("dcp")

        db.execute("INSERT INTO rplasma(Fname , Lname , age , sex , address ,  bg , state , dcp) VALUES (:fname,:lname,:age , :sex , :address , :bg , :state , :dcp)",
                                        {"fname":fname, "lname":lname,"age":age , "sex":sex, "address": address  , "bg":bg , "state" :state , "dcp":dcp })
        db.commit()

        return redirect(url_for('requestplasma'))
            #db.execute("INSERT INTO users(Fname , Lname , age , sex , Blood_group , State) VALUES (:Fname,:Lname,:age , :sex , :Blood_group , :State)",
            #                            {"Fname":Fname, "Lname":Lname,"age":age , "sex":sex , "Blood_group":Blood_group , "State" :State })
            #db.commit()

          #  return render_template("register.html")

    return render_template("requestplasma.html" , headings=headings , data = data)



@app.route("/updates")
def updates():
    return render_template('updates.html')


@app.route("/map")
def map():
    return render_template('map.html')


@app.route("/login" , methods = ["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        usernamedata = db.execute("SELECT name From users WHERE name=:name",{"name":name}).fetchone()
        passworddata = db.execute("SELECT password From users WHERE name=:name",{"name":name}).fetchone()

        if usernamedata is None:
            flash("No username","danger")
            return render_template("login.html")
        else:
            for passwor_data in passworddata:
                if sha256_crypt.verify(password,passwor_data):
                    session["log"] = True

                    return redirect(url_for('map'))
                else:

                    return render_template("login.html")




    return render_template("login.html")




@app.route("/contact" , methods = ["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")


        db.execute("INSERT INTO Contact(name , email , message ) VALUES (:name,:email,:message )",
                                        {"name":name, "email":email,"message":message })
        db.commit()

        return redirect(url_for('contact'))

    return render_template("contact.html")

#logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.secret_key="mangkeyosharingan"
    app.run(debug=True)
