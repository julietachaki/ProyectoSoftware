from app import create_app

app = create_app()

#https://flask.palletsprojects.com/en/3.0.x/appcontext/
app.app_context().push()

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)