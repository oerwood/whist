from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def beregn_overførsler(point_dict, kr_per_point):
    spillere = point_dict
    sorteret_spillere = sorted(spillere.items(), key=lambda x: x[1])

    betaling_samlet = {spiller: 0 for spiller in spillere}

    for i, (skyldner, skyldner_point) in enumerate(sorteret_spillere):
        for modtager, modtager_point in sorteret_spillere[i+1:]:
            beløb = (modtager_point - skyldner_point) * kr_per_point
            betaling_samlet[skyldner] -= beløb
            betaling_samlet[modtager] += beløb

    skyldnere = {k: -v for k, v in betaling_samlet.items() if v < 0}
    modtagere = {k: v for k, v in betaling_samlet.items() if v > 0}

    skyldnere_liste = sorted(skyldnere.items(), key=lambda x: x[1], reverse=True)
    modtagere_liste = sorted(modtagere.items(), key=lambda x: x[1], reverse=True)

    betalinger = []
    i, j = 0, 0
    while i < len(skyldnere_liste) and j < len(modtagere_liste):
        skyldner, skyld_beløb = skyldnere_liste[i]
        modtager, modtag_beløb = modtagere_liste[j]

        beløb = min(skyld_beløb, modtag_beløb)
        betalinger.append({"Fra": skyldner, "Til": modtager, "Beløb": round(beløb, 2)})

        skyldnere_liste[i] = (skyldner, skyld_beløb - beløb)
        modtagere_liste[j] = (modtager, modtag_beløb - beløb)

        if skyldnere_liste[i][1] == 0:
            i += 1
        if modtagere_liste[j][1] == 0:
            j += 1

    return betalinger

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/beregn', methods=['POST'])
def beregn():
    data = request.json
    kr_per_point = float(data["kr_per_point"])
    del data["kr_per_point"]
    
    resultater = beregn_overførsler(data, kr_per_point)
    return jsonify(resultater)

if __name__ == '__main__':
    app.run(debug=True)