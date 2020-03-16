from flask import Flask,render_template,request,redirect,url_for
import pymysql


app = Flask(__name__)
conn = pymysql.connect('localhost','root','29062542','contentdb')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/post")
def post():
    with conn:
        cur = conn.cursor() #ชี้ข้อมูล
        cur.execute("SELECT * FROM content") #ระบุตาราง
        rows = cur.fetchall() #ดึงข้อมูลมาทั้งหมด
        return render_template('post.html',datas=rows) #โยนข้อมูลไปทำงาน

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/form")
def addData():
    return render_template('form.html')

@app.route("/delete/<string:id_data>",methods=['GET'])
def delete(id_data):
    with conn:
        cur = conn.cursor() #ชี้ข้อมูล
        cur.execute("delete from content where id=%s",(id_data)) #ระบุตาราง
        conn.commit()
    return redirect(url_for('post'))

@app.route("/insert",methods=['POST'])
def insert():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        msg=request.form['message']
        with conn.cursor() as cursor:
            sql="INSERT INTO `content`(`name`, `email`, `msg`) values(%s,%s,%s)"
            cursor.execute(sql,(name,email,msg))
            conn.commit() #สั่งเปลี่ยนแปลงข้อมูลด้านในฐานข้อมูล
        return redirect(url_for('post'))

@app.route("/update",methods=['POST'])
def update():
    if request.method=="POST":
        id_update=request.form['id']
        name=request.form['name']
        email=request.form['email']
        msg=request.form['message']
        with conn.cursor() as cursor:
            sql="update content set name=%s, email=%s,msg=%s where id=%s"
            cursor.execute(sql,(name,email,msg,id_update))
            conn.commit() #สั่งเปลี่ยนแปลงข้อมูลด้านในฐานข้อมูล
        return redirect(url_for('post'))

if __name__ == '__main__':
    app.run(debug=True)