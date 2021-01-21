from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect

from flask_app.config import Config

app = Flask(__name__, static_url_path=Config.flask_static_url_path)
app.config.from_object('config.BaseConfig')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Strona główna')


def get_features():
    features = {"Środowisko życia": {"id": "living_environment",
                                     "type": "str"},
                "Liczba nóg": {"id": "n_legs",
                               "type": "int"},
                "Czy posiada skrzydła?": {"id": "has_wing",
                                          "type": "bool"},
                "Czy potrafi pływać?": {"id": "can_swim",
                                        "type": "bool"}
                }
    return features


@app.route('/find_species', methods=['GET', 'POST'])
def find_species():
    if request.method == 'POST':
        for feature in request.form:
            print(f"{feature}={request.form.get(feature)}")
        flash(f"Wiadomość!", 'alert alert-success')
        return redirect(request.url)
    return render_template('find_species.html', title='Znajdź gatunek', features=get_features())


if __name__ == '__main__':
    app.run(port=Config.flask_port)
