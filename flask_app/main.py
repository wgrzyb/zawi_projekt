import json
import unicodedata

from flask import Flask, render_template, request, flash, url_for, session
from werkzeug.utils import redirect
from owlready2 import *
from flask_app.config import Config

app = Flask(__name__, static_url_path=Config.flask_static_url_path)
app.config.from_object('config.BaseConfig')


def reason(onto):
    with onto:
        Imp().set_as_rule("Gatunek(?G), posiada_umiejetnosc(?G, Latanie) -> posiada_ceche(?G, Skrzydla)")
        Imp().set_as_rule(
            "Gatunek(?G) , Rodzaj(?R) , nalezy_do_rodzaju(?G, ?R) , nalezy_do_gromady(?R, Ptaki) -> posiada_liczbe_odnozy(?G, 2)")
        Imp().set_as_rule("Gatunek(?G) , posiada_ceche(?G, Traba) -> posiada_liczbe_odnozy(?G, 4)")
        Imp().set_as_rule("Gatunek(?G) , posiada_ceche(?G, Traba) -> ma_sposob_odzywiania(?G, Roslinozernosc)")
        Imp().set_as_rule(
            "Gatunek(?G) , nalezy_do_rodzaju(?G, ?R) , posiada_ceche(?G, Traba) -> nalezy_do_gromady(?R, Ssaki)")
        Imp().set_as_rule("Gatunek(?G) , nalezy_do_rodziny(?G, Kotowate) -> posiada_liczbe_odnozy(?G, 4)")
        sync_reasoner_pellet(infer_data_property_values=True, infer_property_values=True)
    return onto


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Strona glowna')


def get_features():
    features = {"Srodowisko zycia": {"id": "wystepuje_na_obszarze",
                                     "type": "select",
                                     "values": ["Afryka", "Ameryka Polnocna", "Ameryka Poludniowa", "Ameryka srodkowa",
                                                "Australia", "Azja", "Europa", "Morza", "Oceany"]},
                "Rodzaj": {"id": "rodzaj",
                           "type": "str"},
                "Liczba nog": {"id": "posiada_liczbe_odnozy",
                               "type": "int"},
                "Czy posiada skrzydla?": {"id": "skrzydla",
                                          "type": "bool"},
                "Czy posiada trabe?": {"id": "traba",
                                       "type": "bool"}
                }
    return features


@app.route('/find_species', methods=['GET', 'POST'])
def find_species():
    if request.method == 'POST':
        if len(request.form) == 0:
            flash(f"Nie podano cech!", 'alert alert-danger')
            return redirect(request.url)

        # Cechy:
        # Gdy uzytkownik nie sprecyzuje pola - brane sa wszystkie rekordy z ontologii

        nogi = []
        obszar = []
        cechy = []

        # onto warunki
        onto = get_ontology("Atlas.owl").load()

        for feature in request.form:
            if feature == 'wystepuje_na_obszarze':
                obszar.append(request.form['wystepuje_na_obszarze'].replace(' ', '_'))
            if feature == 'posiada_liczbe_odnozy':
                nogi.append(request.form.get(int(request.form['posiada_liczbe_odnozy'])))
            if feature == 'skrzydla':
                if request.form.get(feature) == 'on':
                    cechy.append(onto['Skrzydla'])
            if feature == 'traba':
                if request.form.get(feature) == 'on':
                    cechy.append(onto['Traba'])
        print(obszar, nogi)
        # result = {}
        # result['nogi'] = onto.search(posiada_liczbe_odnozy='*' if liczba_nog == 'all' else liczba_nog),
        # result['obszar'] = onto.search(wystepuje_na_obszarze='*' if obszar == 'all' else onto[obszar]),
        # result['cechy'] = onto.search(posiada_ceche='*' if not cechy else onto[cechy])
        # print(liczba_nog, obszar)
        # if not liczba_nog and not obszar:
        onto = reason(onto)
        result = onto.search(is_a=onto['Gatunek'], posiada_ceche=cechy)
        print(result)
        # result = onto.search(posiada_liczbe_odnozy='' if liczba_nog == 'all' else liczba_nog,
        #                       wystepuje_na_obszarze='' if obszar == 'all' else onto[obszar],
        #                       posiada_ceche=onto[cechy])

        species = [species.get_name().replace("_", " ") for species in result]
        return redirect(url_for('show_result', species=json.dumps(species)))
    return render_template('find_species.html', title='Znajdz gatunek', features=get_features())


@app.route('/result', methods=['GET', 'POST'])
def show_result():
    species = json.loads(request.args['species'])
    return render_template('result.html', title='Wyniki', species=species)


def get_form_fields():
    features = {"Gatunek": {"id": "gatunek",
                            "type": "str",
                            "required": True},
                "Gromada": {"id": "gromada",
                            "type": "select",
                            "values": ["Gady", "Krazkoplawy", "Owady", "Pajeczaki", "Paprotniki", "Plazy", "Ptaki",
                                       "Ssaki", "Watrobowce"],
                            "required": True},
                "Rodzaj": {"id": "rodzaj",
                           "type": "str",
                           "required": True},
                "Rodzina": {"id": "rodzina",
                            "type": "str",
                            "required": True},
                "Obszar": {"id": "obszar",
                           "type": "select",
                           "values": ["Afryka", "Ameryka Polnocna", "Ameryka Poludniowa", "Ameryka srodkowa",
                                      "Australia", "Azja", "Europa", "Morza", "Oceany"],
                           "required": True},
                "Sposob odzywiania": {"id": "sposob_odzywiania",
                                      "type": "select",
                                      "values": ["Miesozernosc", "Roslinozernosc", "Wszystkozernosc"],
                                      "required": True},
                "Kategoria zagrozenia wyginieciem": {"id": "kategoria_zagrozenia",
                                                     "type": "select",
                                                     "values": ["Najmniejszej troski", "Nierozpoznane", "Wymarle",
                                                                "Zagrozone"],
                                                     "required": True},
                "Posiada ogon?": {"id": "czy_ogon",
                                  "type": "bool",
                                  "required": False},
                "Posiada pletwy?": {"id": "czy_pletwy",
                                    "type": "bool",
                                    "required": False},
                "Posiada skrzydla?": {"id": "czy_skrzydla",
                                      "type": "bool",
                                      "required": False},
                "Posiada trabe?": {"id": "czy_traba",
                                   "type": "bool",
                                   "required": False},
                "Umie latac?": {"id": "czy_lata",
                                "type": "bool",
                                "required": False},
                "Umie plywac?": {"id": "czy_plywa",
                                 "type": "bool",
                                 "required": False},
                "Liczba odnozy": {"id": "ile_odnozy",
                                  "type": "int",
                                  "required": False},
                "Masa ciala": {"id": "masa_ciala",
                               "type": "int",
                               "required": False}
                }
    return features


@app.route('/add_species', methods=['GET', 'POST'])
def add_species():
    if request.method == 'POST':
        print(request.form)  # Wypisanie parametrow z formularza
        gatunek = request.form['gatunek'].replace(' ', '_')
        gromada = request.form['gromada'].replace(' ', '_')
        rodzaj = request.form['rodzaj'].replace(' ', '_')
        rodzina = request.form['rodzina'].replace(' ', '_')
        obszar = request.form['obszar'].replace(' ', '_')
        sposob_odz = request.form['sposob_odzywiania']
        kategoria = request.form['kategoria_zagrozenia'].replace(' ', '_')
        ile_odnozy = request.form['ile_odnozy']
        masa_ciala = request.form['masa_ciala']

        onto = get_ontology("Atlas.owl").load()  # Załadowanie onto

        cechy = []
        umiejetnosci = []
        nogi = []
        masa = []
        re_dig = re.compile(r'^[1-9]+$')

        for feature in request.form:
            if feature == 'czy_ogon':
                cechy.append(onto['Ogon'])
            if feature == 'czy_pletwy':
                cechy.append(onto['Pletwy'])
            if feature == 'czy_skrzydla':
                cechy.append(onto['Skrzydla'])
            if feature == 'czy_traba':
                cechy.append(onto['Traba'])
            if feature == 'czy_plywa':
                umiejetnosci.append(onto['Plywanie'])
            if feature == 'czy_lata':
                umiejetnosci.append(onto['Latanie'])
            if feature == 'ile_odnozy' and re_dig.match(ile_odnozy):
                nogi.append(int(ile_odnozy))
            if feature == 'masa_ciala' and re_dig.match(masa_ciala):
                nogi.append(int(masa_ciala))

        if any(map(str.isdigit, gatunek)) or any(map(str.isdigit, gromada)) or any(map(str.isdigit, rodzina)) or any(
                map(str.isdigit, obszar)):
            flash(f"Pola nie moga zawierac liczb!", 'alert alert-danger')
            return redirect(request.url)

        if not onto[rodzina]:
            onto.Rodzina(rodzina)

        if not onto[rodzaj]:
            onto.Rodzaj(rodzaj)

        onto.Gatunek(gatunek, nalezy_do_gromady=[onto[gromada]],
                     wystepuje_na_obszarze=[onto[obszar]],
                     nalezy_do_rodziny=[onto[rodzina]],
                     nalezy_rodzaju=[onto[rodzaj]],
                     ma_sposob_odzywiania=[onto[sposob_odz]],
                     znajduje_sie_w_kategorii_zagrozenia=[onto[kategoria]],
                     posiada_ceche=cechy,
                     posiada_umiejetnosc=umiejetnosci,
                     posiada_liczbe_odnozy=nogi,
                     posiada_mase_ciala=masa)

        flash(f"Indywiduum dodane do ontologii!", 'alert alert-success')
        onto.save(file='Atlas.owl')

    return render_template('add_species.html', title='Dodaj gatunek', form_fields=get_form_fields())


if __name__ == '__main__':
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=Config.flask_port)
