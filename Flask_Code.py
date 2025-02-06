from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import os
import subprocess
import requests
import pandas as pd
from io import BytesIO
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app)

# Initialiser SQLAlchemy
db = SQLAlchemy(app)

# Modèle de base de données
class GlassData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_document = db.Column(db.String(100), nullable=True)
    titre = db.Column(db.String(200), nullable=True)
    reference = db.Column(db.String(200), nullable=True)
    premier_auteur = db.Column(db.String(100), nullable=True)
    nombre_types_verres = db.Column(db.Integer, nullable=True)
    sio2 = db.Column(db.String(100), nullable=True)
    b2o3 = db.Column(db.String(100), nullable=True)
    na2o = db.Column(db.String(100), nullable=True)
    al2o3 = db.Column(db.String(100), nullable=True)
    fines = db.Column(db.String(100), nullable=True)
    densite = db.Column(db.String(100), nullable=True)
    homogeneite = db.Column(db.String(100), nullable=True)
    b_iv_pourcent = db.Column(db.String(100), nullable=True)
    irradie = db.Column(db.String(100), nullable=True)
    caracteristiques_irradie = db.Column(db.String(100), nullable=True)
    temperature = db.Column(db.String(100), nullable=True)
    statique_dynamique = db.Column(db.String(100), nullable=True)
    plage_granulo = db.Column(db.String(100), nullable=True)
    surface_specifique_geometrique = db.Column(db.String(100), nullable=True)
    surface_specifique_bet = db.Column(db.String(100), nullable=True)
    qualite_polissage = db.Column(db.String(100), nullable=True)
    masse_verre = db.Column(db.String(100), nullable=True)
    s_verre = db.Column(db.String(100), nullable=True)
    v_solution = db.Column(db.String(100), nullable=True)
    debit_solution = db.Column(db.String(100), nullable=True)
    ph_initial = db.Column(db.String(100), nullable=True)
    ph_final = db.Column(db.String(100), nullable=True)
    composition_solution = db.Column(db.String(100), nullable=True)
    duree_experience = db.Column(db.String(100), nullable=True)
    ph_final_amb = db.Column(db.String(100), nullable=True)
    ph_final_test = db.Column(db.String(100), nullable=True)
    normalisation_vitesse = db.Column(db.String(100), nullable=True)
    v0_si = db.Column(db.String(100), nullable=True)
    r_carre_si = db.Column(db.String(100), nullable=True)
    ordonnee_origine_si = db.Column(db.String(100), nullable=True)
    v0_b = db.Column(db.String(100), nullable=True)
    ordonnee_origine_b = db.Column(db.String(100), nullable=True)
    v0_na = db.Column(db.String(100), nullable=True)
    r_carre_na = db.Column(db.String(100), nullable=True)
    ordonnee_origine_na = db.Column(db.String(100), nullable=True)
    v0_dm = db.Column(db.String(100), nullable=True)
    congruence = db.Column(db.String(100), nullable=True)

# Créer la base de données si elle n'existe pas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    glass_data = GlassData.query.all()
    return render_template('index.html', glass_data=glass_data)

@app.route('/add_glass_data', methods=['POST'])
def add_glass_data():
    data = request.get_json()
    nombre_types_verres=data.get('nombre_types_verres')
    try:
        # Créer l'entrée principale
        new_entry = GlassData(
            type_document=data.get('type'),
            titre=data.get('titre'),
            reference=data.get('reference'),
            premier_auteur=data.get('premier_auteur'),
            nombre_types_verres=nombre_types_verres,
            sio2=data.get('sio2'),
            b2o3=data.get('b2o3'),
            na2o=data.get('na2o'),
            al2o3=data.get('al2o3'),
            fines=data.get('fines'),
            densite=data.get('densite'),
            homogeneite=data.get('homogeneite'),
            b_iv_pourcent=data.get('b_iv_pourcent'),
            irradie=data.get('irradie'),
            caracteristiques_irradie=data.get('caracteristiques_irradie'),
            temperature=data.get('temperature'),
            statique_dynamique=data.get('statique_dynamique'),
            plage_granulo=data.get('plage_granulo'),
            surface_specifique_geometrique=data.get('surface_specifique_geometrique'),
            surface_specifique_bet=data.get('surface_specifique_bet'),
            qualite_polissage=data.get('qualite_polissage'),
            masse_verre=data.get('masse_verre'),
            s_verre=data.get('s_verre'),
            v_solution=data.get('v_solution'),
            debit_solution=data.get('debit_solution'),
            ph_initial=data.get('ph_initial'),
            ph_final=data.get('ph_final'),
            composition_solution=data.get('composition_solution'),
            duree_experience=data.get('duree_experience'),
            ph_final_amb=data.get('ph_final_amb'),
            ph_final_test=data.get('ph_final_test'),
            normalisation_vitesse=data.get('normalisation_vitesse'),
            v0_si=data.get('v0_si'),
            r_carre_si=data.get('r_carre_si'),
            ordonnee_origine_si=data.get('ordonnee_origine_si'),
            v0_b=data.get('v0_b'),
            ordonnee_origine_b=data.get('ordonnee_origine_b'),
            v0_na=data.get('v0_na'),
            r_carre_na=data.get('r_carre_na'),
            ordonnee_origine_na=data.get('ordonnee_origine_na'),
            v0_dm=data.get('v0_dm'),
            congruence=data.get('congruence')
        )
        db.session.add(new_entry)
        db.session.commit()

        # Créer des entrées supplémentaires avec "Non" pour les champs de composition
        for _ in range(int(nombre_types_verres) - 1):
            additional_entry = GlassData(
                type_document=data.get('type_document'),
                titre=data.get('titre'),
                reference=data.get('reference'),
                premier_auteur=data.get('premier_auteur'),
                nombre_types_verres=nombre_types_verres,
                sio2="Non",
                b2o3="Non",
                na2o="Non",
                al2o3="Non",
                fines="Non",
                densite="Non",
                homogeneite=data.get('homogeneite'),
                b_iv_pourcent=data.get('b_iv_pourcent'),
                irradie=data.get('irradie'),
                caracteristiques_irradie=data.get('caracteristiques_irradie'),
                temperature=data.get('temperature'),
                statique_dynamique=data.get('statique_dynamique'),
                plage_granulo=data.get('plage_granulo'),
                surface_specifique_geometrique=data.get('surface_specifique_geometrique'),
                surface_specifique_bet=data.get('surface_specifique_bet'),
                qualite_polissage=data.get('qualite_polissage'),
                masse_verre=data.get('masse_verre'),
                s_verre=data.get('s_verre'),
                v_solution=data.get('v_solution'),
                debit_solution=data.get('debit_solution'),
                ph_initial=data.get('ph_initial'),
                ph_final=data.get('ph_final'),
                composition_solution=data.get('composition_solution'),
                duree_experience=data.get('duree_experience'),
                ph_final_amb=data.get('ph_final_amb'),
                ph_final_test=data.get('ph_final_test'),
                normalisation_vitesse=data.get('normalisation_vitesse'),
                v0_si="Non",
                r_carre_si="Non",
                ordonnee_origine_si="Non",
                v0_b="Non",
                ordonnee_origine_b="Non",
                v0_na="Non",
                r_carre_na="Non",
                ordonnee_origine_na="Non",
                v0_dm="Non",
                congruence="Non"
            )
            db.session.add(additional_entry)
            db.session.commit()

        return "Données sur le verre ajoutées avec succès !", 200

    except Exception as e:
        return f"Erreur : {str(e)}", 500

@app.route('/delete_document_reference/<int:id>', methods=['POST'])
def delete_document_reference(id):
    glass_data = GlassData.query.get(id)
    db.session.delete(glass_data)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Call Docling script
        docling_script_path = '/home/intra.cea.fr/ao280403/DOCLING_LANGFLOW_FLASK_v2/DLF/docling_script.py'
        if not os.path.exists(docling_script_path):
            return f"Docling script not found at: {docling_script_path}", 500

        process = subprocess.Popen(
            ["python", docling_script_path, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Read the output and send progress updates
        total_pages = 0
        for line in process.stdout:
            logging.info(line.strip())
            if "Page" in line and "/" in line:
                parts = line.split(" ")
                current_page = int(parts[1].split("/")[0])
                total_pages = int(parts[1].split("/")[1])
                percent_complete = (current_page / total_pages) * 100
                socketio.emit('progress', {'percent_complete': percent_complete})
            elif "Table" in line or "Picture" in line:
                socketio.emit('progress', {'message': line.strip()})

        process.wait()

        # Construct the expected Markdown file path
        doc_filename = os.path.splitext(os.path.basename(filepath))[0]
        md_filepath = os.path.join('scratch', f"{doc_filename}-md", f"{doc_filename}-plain.md")

        # Verify the Markdown file exists
        if not os.path.exists(md_filepath):
            return f"Markdown file not found at: {md_filepath}", 500

        # Read the Markdown file
        with open(md_filepath, 'r') as md_file:
            md_content = md_file.read()

        # Call Langflow API
        response = requests.post(
            "http://127.0.0.1:7860/api/v1/run/a7e4b6a1-d444-487c-bec7-a954e6d42725?stream=false",
            json={
                "input_value": md_content,
                "output_type": "chat",
                "input_type": "text",
                "tweaks": {
                    "MistralModel-X63zd": {},
                    "File-yvKBt": {},
                    "Prompt-F8PHW": {},
                    "ParseData-ggwft": {},
                    "TextInput-4LsXJ": {},
                    "ChatOutput-Uou7S": {},
                    "CustomComponent-OsOFR": {}
                }
            }
        )

        # Return a JSON response to update the frontend
        return jsonify({"message": "File processed successfully", "data": response.json()})

@app.route('/download_excel', methods=['GET'])
def download_excel():
    glass_data = GlassData.query.all()
    data = []
    for entry in glass_data:
        data.append({
            "Type": entry.type_document,
            "Titre": entry.titre,
            "Référence": entry.reference,
            "Premier Auteur": entry.premier_auteur,
            "Nombre de types de verres": entry.nombre_types_verres,
            "SiO₂": entry.sio2,
            "B₂O₃": entry.b2o3,
            "Na₂O": entry.na2o,
            "Al₂O₃": entry.al2o3,
            "Fines": entry.fines,
            "Densité": entry.densite,
            "Homogénéité": entry.homogeneite,
            "% B(IV)": entry.b_iv_pourcent,
            "Irradié": entry.irradie,
            "Caractéristiques si irradié": entry.caracteristiques_irradie,
            "Température": entry.temperature,
            "Statique/dynamique": entry.statique_dynamique,
            "Plage granulo si poudre": entry.plage_granulo,
            "Surface spécifique géométrique si poudre": entry.surface_specifique_geometrique,
            "Surface spécifique BET si poudre": entry.surface_specifique_bet,
            "Qualité polissage si monolithe": entry.qualite_polissage,
            "Masse verre": entry.masse_verre,
            "S(verre)": entry.s_verre,
            "V(solution)": entry.v_solution,
            "Débit solution": entry.debit_solution,
            "pH initial (T amb)": entry.ph_initial,
            "pH final (T essai)": entry.ph_final,
            "Compo solution": entry.composition_solution,
            "Durée expérience": entry.duree_experience,
            "pH final (T amb)": entry.ph_final_amb,
            "pH final (T essai)": entry.ph_final_test,
            "Normalisation vitesse (Spm ou SBET)": entry.normalisation_vitesse,
            "V₀(Si)": entry.v0_si,
            "r²": entry.r_carre_si,
            "Ordonnée origine": entry.ordonnee_origine_si,
            "V₀(B)": entry.v0_b,
            "Ordonnée origine": entry.ordonnee_origine_b,
            "V₀(Na)": entry.v0_na,
            "r²": entry.r_carre_na,
            "Ordonnée origine": entry.ordonnee_origine_na,
            "V₀(ΔM)": entry.v0_dm,
            "Congruence": entry.congruence
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Glass Data')
    output.seek(0)

    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='glass_data.xlsx')

@socketio.on('connect')
def handle_connect():
    emit('status', {'msg': 'Connecté'})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    socketio.run(app, debug=True, port=5001)
