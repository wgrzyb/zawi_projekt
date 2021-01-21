from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect

from flask_app.config import Config

app = Flask(__name__, static_url_path=Config.flask_static_url_path)
app.config.from_object('config.BaseConfig')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Strona główna')


@app.route('/find_species', methods=['GET', 'POST'])
def find_species():
    if request.method == 'POST':
        flash(f"Wiadomość!", 'alert alert-success')
        return redirect(request.url)
    return render_template('find_species.html', title='Znajdź gatunek')


if __name__ == '__main__':
    app.run(port=Config.flask_port)
