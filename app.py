import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from  blog import blog

app = Flask(__name__)
app.register_blueprint(blog)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

# model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post')

    def __repr__(self):
        return f'<Post "{self.title}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'


class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))


    def __init__(self, name, city, addr,pin):
        self.name = name
        self.city=city
        self.addr=addr
        self.pin=pin

# post - insert
@app.route('/students',methods=["post"])
def add_student():
    data= request.json
    print(data["city"])
    newStudent= students(data["name"],data["city"],data["addr"],data["pin"])
    db.session.add (newStudent)
    db.session.commit()

    return {'add':"true"}

# get - select
@app.route('/students',methods=["get"])
def get_students():
    res=[]
    for stu in students.query.all():
         res.append({"id":stu.id,"name":stu.name,"city":stu.city})
    return json.dumps( res)


@app.route('/students/<id>',methods=["delete"])
def del_students(id):
    stu= students.query.filter_by(id=id).first()
    db.session.delete(stu)
    db.session.commit()
    return {'del':"true"}

# get - select
@app.route('/posts',methods=["get"])
def get_posts():
    res=[]
    for stu in Post.query.all():
         res.append({"id":stu.id,"content":stu.content})
    return json.dumps( res)

@app.route('/posts/<id>',methods=["delete"])
def del_post(id):
    stu= Post.query.filter_by(id=id).first()
    db.session.delete(stu)
    db.session.commit()
    return {'del':"true"}


@app.route('/students/<id>',methods=["put"])
def upd_students(id):
    data= request.json
    stu= students.query.filter_by(id=id).first()
    stu.name=data["name"]
    db.session.commit()
    return {'upd':"true"}

def init_data():
    post1 = Post(title='Post The First', content='Content for the first post')
    post2 = Post(title='Post The Second', content='Content for the Second post')
    post3 = Post(title='Post The Third', content='Content for the third post')

    comment1 = Comment(content='Comment for the first post', post=post1)
    comment2 = Comment(content='Comment for the second post', post=post2)
    comment3 = Comment(content='Another comment for the second post', post_id=2)
    comment4 = Comment(content='Another comment for the first post', post_id=1)


    db.session.add_all([post1, post2, post3])
    db.session.add_all([comment1, comment2, comment3, comment4])

    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
            db.create_all()
                # init_data()
    app.run(debug = True)
