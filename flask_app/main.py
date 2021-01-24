from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect
from owlready2 import *
from flask_app.config import Config

app = Flask(__name__, static_url_path=Config.flask_static_url_path)
app.config.from_object('config.BaseConfig')


def reason(onto):
    with onto:
        Imp().set_as_rule("Gatunek(?G), posiada_umiejetnosc(?G, Latanie) -> posiada_ceche(?G, Skrzydla)")
        Imp().set_as_rule("Gatunek(?G) , Rodzaj(?R) , nalezy_do_rodzaju(?G, ?R) , nalezy_do_gromady(?R, Ptaki) -> posiada_liczbe_odnozy(?G, 2)")
        Imp().set_as_rule("Gatunek(?G) , posiada_ceche(?G, Traba) -> posiada_liczbe_odnozy(?G, 4)")
        Imp().set_as_rule("Gatunek(?G) , posiada_ceche(?G, Traba) -> ma_sposob_odzywiania(?G, Roslinozernosc)")
        Imp().set_as_rule("Gatunek(?G) , nalezy_do_rodzaju(?G, ?R) , posiada_ceche(?G, Traba) -> nalezy_do_gromady(?R, Ssaki)")
        Imp().set_as_rule("Gatunek(?G) , nalezy_do_rodziny(?G, kotowate) -> posiada_liczbe_odnozy(?G, 4)")
        sync_reasoner_pellet(infer_data_property_values=True, infer_property_values=True)
    return onto

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Strona główna')


def get_features():
    features = {"Środowisko życia": {"id": "wystepuje_na_obszarze",
                                     "type": "str"},
                "Liczba nóg": {"id": "posiada_liczbe_odnozy",
                               "type": "int"},
                "Czy posiada skrzydła?": {"id": "skrzydla",
                                          "type": "bool"},
                "Czy posiada trąbę?": {"id": "traba",
                                        "type": "bool"}
                }
    return features


@app.route('/find_species', methods=['GET', 'POST'])
def find_species():
    if request.method == 'POST':
        if len(request.form) == 0:
            flash(f"Nie podano cech!", 'alert alert-danger')
            return redirect(request.url)

        # cechy:
        # Gdy użytkownik nie sprecyzuje pola - brane są wszystkie rekordy z ontologii
        liczba_nog = 'all'
        obszar = 'all'
        cechy = []

        # onto
        onto = get_ontology("Atlas_Zwierzat.owl").load()
        onto = reason(onto)
        for feature in request.form:
            if feature == 'wystepuje_na_obszarze':
                obszar = request.form.get(feature)
            if feature == 'posiada_liczbe_odnozy':
                liczba_nog = int(request.form.get(feature))
            if feature == 'skrzydla':
                if request.form.get(feature) == 'on':
                    cechy.append(onto['Skrzydla'])
            if feature == 'traba':
                if request.form.get(feature) == 'on':
                    cechy.append(onto['Traba'])

        result = onto.search(posiada_liczbe_odnozy='*' if liczba_nog == 'all' else liczba_nog,
                             wystepuje_na_obszarze='*' if obszar == 'all' else onto[obszar],
                             posiada_ceche='*' if not cechy else cechy)
        print(result)

        flash(f"Znaleziono!", 'alert alert-success')
        return redirect(request.url)
    return render_template('find_species.html', title='Znajdź gatunek', features=get_features())


@app.route('/add_species', methods=['GET', 'POST'])
def add_species():
    if request.method == 'POST':
        if len(request.form) == 0:
            flash(f"Nie podano cech!", 'alert alert-danger')
            return redirect(request.url)
    #flash(f"Dodano!", 'alert alert-success')
    return render_template('add_species.html', title='Dodaj gatunek')

if __name__ == '__main__':
    app.run(port=Config.flask_port)
