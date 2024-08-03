from flask import Flask, render_template, request, redirect, url_for

from flask_migrate import Migrate
from models import Post

from config.setting import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SECRET_KEY"] = "123432432432"

db.init_app(app)

Migrate(app, db)

# 點擊 http://127.0.0.1:5000 轉址 找到 main()的endpoint
@app.route("/")
def home():
    return redirect(url_for('main'))


@app.route("/posts", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # 寫入資料庫
        title = request.form.get("title")
        price = request.form.get("price")
        description = request.form.get("description")

        post = Post(title=title, price=price, description=description)
        
        db.session.add(post)
        db.session.commit()

        # flash("新增成功")

        return redirect("/posts")
    
    posts = Post.query.all()
    return render_template("posts/index.jinja", posts=posts)

# 建立
@app.route("/posts/new")
def new():
    return render_template("posts/new.jinja")

# 顯示
@app.route("/posts/<int:id>")
def show(id):
    post = Post.query.get_or_404(id)
    return render_template("posts/show.jinja", post=post)

# 編輯
@app.route("/posts/<int:id>/edit")
def edit(id):
    post = Post.query.get_or_404(id)
    return render_template("posts/edit.jinja", post=post)

# 更新
@app.route("/posts/<int:id>", methods=["POST"])
def update(id):

    post = Post.query.get_or_404(id)

    title = request.form.get("title")
    price = request.form.get("price")
    description = request.form.get("description")

    post.title = title
    post.price = price
    post.description = description

    db.session.add(post)
    db.session.commit()

    return render_template("posts/show.jinja", post=post)

# 刪除
@app.route("/posts/<int:id>/delete", methods=["POST"])
def delete(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/posts")
