from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3 as sql
app=Flask(__name__)

app.secret_key="key123"

@app.route('/')
def home():
    conn=sql.connect("video_details.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("select * from youtube_details")
    data=cur.fetchall()
    return render_template("home.html",data=data)

@app.route('/video<id>')
def video(id):
     conn=sql.connect("video_details.db")
     conn.row_factory=sql.Row
     cur=conn.cursor()
     cur.execute("select * from youtube_details where id=?",(id,))
     data=cur.fetchone()
    
     return render_template("videoplayer.html", data=data)

@app.route('/login',methods=["POST","GET"])
def login():
      if request.method=="POST":
        Name=request.form.get("Name")
        Email_ID=request.form.get("Email_ID")
        Password=request.form.get("Password")
        conn=sql.connect("video_details.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("select * from user_details where Name=?",(Name,))
        data=cur.fetchone()
        print(data)
        if data:
             if Email_ID==data["Email_ID"] and Password==data["Password"]:
                  session["username"]=Name
                  return redirect(url_for("home"))
             else:
                  return "user doesn't exist"
         
         #return redirect(url_for('home'))
      return render_template("login.html")

@app.route('/logout')
def logout():
   session.pop("Name",None)
   return redirect(url_for("login"))

@app.route("/new_user",methods=["POST","GET"])
def new_user():
   if request.method=="POST":
      Name=request.form.get("Name")
      Email_ID=request.form.get("Email_ID")
      Password=request.form.get("Password")
      conn=sql.connect("video_details.db")
      conn.row_factory=sql.Row
      cur=conn.cursor()
      cur.execute("insert into user_details (Name,Email_ID,Password) values(?,?,?)",(Name,Email_ID,Password))
      conn.commit()
      return redirect(url_for('home'))
   return render_template("new_user.html")

if __name__=="__main__":
        app.run(debug=True)