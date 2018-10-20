# Analiza podatkov

Trenutno vključuje samo skripto za zajem podatkov s strani [findagrave.com](http://findagrave.com/), ki pridobi podatke grobov z 80 najbolj popisanih pokopališč. Z vsakega groba se pridobita samo podatka ime osebe ter datuma rojstva in smrti.

## Priprava okolja

```
python3 -m venv venv3

source venv3/bin/activate  # bash
. venv3/bin/activate.fish  # fish
```

Namestitev potrebnih knjižnic
```
pip3 install -r requirements.txt
```

Stran [findagrave.com](http://findagrave.com/) na žalost ni prijazna do programov, ki avtomatizirano prenašajo podatke z njihove spletne strani, zato s preprosto `GET` zahtevo ni mogoče pridobiti podatkov. Tudi sprememba `user-agent`-a v glavi zahteve ne zadostuje. Zato je potrebna uporaba "nadziranega brskalnika". Možnost za prenos Mozillinega Geckodriverja je na voljo [tukaj](https://github.com/mozilla/geckodriver/releases)