from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': 'Bradley Cooper',
        'title': 'Opening night',
        'content': 'The best night of our lives',
        'date_posted': 'January 1, 2019'
    },
    {
        'author': 'Pierre du Toit',
        'title': 'A New World',
        'content': 'The world is an amazing place, full of amazing people and amazing things to see',
        'date_posted': 'October 19, 2019'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)