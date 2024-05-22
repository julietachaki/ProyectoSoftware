# from cryptography.fernet import Fernet
# import hashlib
import base64

from flask import Blueprint, flash, redirect, render_template, request

from app.models.text import Text
from app.models.user import User
from app.models.user_data import UserData

index = Blueprint("index", __name__)

username_saved = None
password_saved = None
user = None


@index.route("/")
def init():
    if username_saved != None and password_saved != None:
        return redirect("/home")
    else:
        return render_template("init.html")


@index.route("/register", methods=["POST"])
def register():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]
    address = request.form["address"]
    city = request.form["city"]
    country = request.form["country"]
    user_data = UserData()
    user_data.firstname = firstname
    user_data.lastname = lastname
    user_data.phone = phone
    user_data.address = address
    user_data.city = city
    user_data.country = country
    user = User(user_data)
    user.email = request.form["email"]
    user.username = request.form["new_username"]
    user.password = request.form["new_password"]
    try:
        user.save()
    except:
        error = "User or email already exists"
        flash(error)
    return redirect("/")


@index.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    global user
    list_user = User.find_by(username=username, password=password)
    if list_user:
        user = list_user[0]
        if type(request.form.get("remember")) == str:
            global username_saved
            global password_saved
            username_saved = username
            password_saved = password
        return redirect("/home")
    else:
        error = "Invalid credentials"
        flash(error)
        return redirect("/")


@index.route("/encrypt", methods=["POST"])
def encrypt():
    text = Text(content=request.form["content"])
    global user
    print(user)

    if user is not None:
        text.user_id = user.id

    if request.form["key"]:
        key_form = request.form["key"]
        key_form = key_form.encode()
        key_form = base64.urlsafe_b64encode(key_form.ljust(32, b"\0"))
        text.encrypt_content(key_form)
    else:
        text.encrypt_content()
    text.save()

    return redirect("/home")


@index.route("/home")
def home():
    global user
    if user is not None:
        texts = Text.find_by(user_id=user.id)
    for text in texts:
        print(type(text.key))
    return render_template("index.html", texts=texts)


@index.route("/decrypt", methods=["POST"])
def decrypt():
    text_id = int(request.form["text_id"])  # Convert text_id to an integer
    decrypt_key = request.form["decrypt_key"]
    decrypt_key = decrypt_key.encode()
    decrypt_key = base64.urlsafe_b64encode(decrypt_key.ljust(32, b"\0"))

    text = Text.find(text_id)
    if text:
        try:
            text.decrypt_content(decrypt_key)
            text.save()
        except:
            error = "Invalid key"
            flash(error)
        return redirect("/home")
    else:
        return redirect("/home")


@index.route("/delete", methods=["POST"])
def delete():
    text_id = int(request.form["text_id"])
    text = Text.find(text_id)
    if text:
        text.delete()
        return redirect("/home")
    else:
        return redirect("/home")


@index.route("/edit", methods=["POST"])
def edit():
    text_id = int(request.form["text_id"])
    text = Text.find(text_id)
    new_content = request.form["new_content"]
    text.content = new_content
    text.length = len(new_content)
    text.save()
    return redirect("/home")


@index.route("/encrypt-again", methods=["POST"])
def encrypt_again():
    text_id = int(request.form["text_id"])
    text = Text.find(text_id)
    if text:
        key = text.key
        text.encrypt_content(key)
        text.save()
        return redirect("/home")
    else:
        return redirect("/home")


@index.route("/logout")
def logout():
    global username_saved
    global password_saved
    username_saved = None
    password_saved = None
    return redirect("/")