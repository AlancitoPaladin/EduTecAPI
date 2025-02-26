from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/courses')
def courses():
    Courses = [
        {"Course": "Ingeniería de Software", "Duration": "Feb-Junio 2025", "Teacher": "Alan Carlos Hernández",
         "Image": "https://miro.medium.com/v2/resize:fit:4800/format:webp/1*gQzkQ3uJ0SwJL51t16bivw.jpeg"}
    ]
    return Courses


if __name__ == '__main__':
    app.run()
