from langflow.custom import Component
from langflow.io import Output, MessageTextInput
from langflow.schema import Data
import requests

class EnvoyerDonneesVerreTableComponent(Component):
    display_name = "Envoyer Données Verre à la Table"
    description = "Envoyer la composition détaillée du verre et les informations de référence du document au serveur Flask."
    icon = "table"

    inputs = [
        MessageTextInput(
            name="texte_extrait",
            display_name="Texte Extrait",
            info=(
                "Texte extrait contenant la référence du document et les informations sur la composition du verre."
            ),
            value=(
                "1. Type du document : Article\n"
                "2. Titre du document : EFFECTS OF COMPOSITION VARIATIONS ON THE ALTERATION KINETICS OF THE UOX1 \"LIGHT WATER\" BOROSILICATE CONTAINMENT GLASS\n"
                "3. Référence : ICEMO01 abs #409 ses 57-4\n"
                "4. Premier Auteur : P. Frugier\n"
                "5. Nombre de types de verres : 1\n"
                "6. SiO₂ : 42.4\n"
                "7. B₂O₃ : 12.4\n"
                "8. Na₂O : 8.1\n"
                "9. Al₂O₃ : 6.6\n"
                "10. Fines : 0.01\n"
                "11. Densité : Non disponible\n"
                "12. Homogénéité : Non disponible\n"
                "13. % B(IV) : Non disponible\n"
                "14. Irradié : Non disponible\n"
                "15. Caractéristiques si irradié : Non disponible\n"
                "16. Température : 100°C\n"
                "17. Statique/dynamique : Non disponible\n"
                "18. Plage granulo si poudre : Non disponible\n"
                "19. Surface spécifique géométrique si poudre : Non disponible\n"
                "20. Surface spécifique BET si poudre : Non disponible\n"
                "21. Qualité polissage si monolithe : Non disponible\n"
                "22. Masse verre : Non disponible\n"
                "23. S(verre) : Non disponible\n"
                "24. V(solution) : Non disponible\n"
                "25. Débit solution : Non disponible\n"
                "26. pH initial (T amb) : Non disponible\n"
                "27. pH initial (T essai) : Non disponible\n"
                "28. Compo solution : Non disponible\n"
                "29. Durée expérience : Non disponible\n"
                "30. pH final (T amb) : Non disponible\n"
                "31. pH final (T essai) : Non disponible\n"
                "32. Normalisation vitesse (Spm ou SBET) : Non disponible\n"
                "33. V₀(Si) : Non disponible\n"
                "34. r²(Si) : Non disponible\n"
                "35. Ordonnée origine : Non disponible\n"
                "36. V₀(B) : Non disponible\n"
                "37. Ordonnée origine : Non disponible\n"
                "38. V₀(Na) : Non disponible\n"
                "39. r²(Na) : Non disponible\n"
                "40. Ordonnée origine : Non disponible\n"
                "41. V₀(ΔM) : Non disponible\n"
                "42. Congruence : Non disponible\n"
            ),
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Réponse", name="sortie", method="construire_sortie"),
    ]

    def construire_sortie(self) -> Data:
        texte_extrait = self.texte_extrait
        print(f"Texte Extrait: {texte_extrait}")

        try:
            # Nettoyer et analyser le texte
            lignes = [ligne.strip() for ligne in texte_extrait.split("\n") if ligne.strip()]

            # Extraction des données
            type_doc = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("1. Type du document :")), None)
            titre = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("2. Titre du document :")), None)
            reference = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("3. Référence :")), None)
            premier_auteur = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("4. Premier Auteur :")), None)
            nombre_types_verres = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("5. Nombre de types de verres :")), None)
            sio2 = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("6. SiO₂ :")), None)
            b2o3 = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("7. B₂O₃ :")), None)
            na2o = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("8. Na₂O :")), None)
            al2o3 = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("9. Al₂O₃ :")), None)
            fines = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("10. Fines :")), None)
            densite = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("11. Densité :")), None)
            homogeneite = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("12. Homogénéité :")), None)
            pourcentage_b_iv = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("13. % B(IV) :")), None)
            irradie = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("14. Irradié :")), None)
            caracteristiques_irradie = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("15. Caractéristiques si irradié :")), None)
            temperature = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("16. Température :")), None)
            statique_dynamique = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("17. Statique/dynamique :")), None)
            plage_granulo = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("18. Plage granulo si poudre :")), None)
            surface_specifique_geometrique = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("19. Surface spécifique géométrique si poudre :")), None)
            surface_specifique_bet = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("20. Surface spécifique BET si poudre :")), None)
            qualite_polissage = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("21. Qualité polissage si monolithe :")), None)
            masse_verre = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("22. Masse verre :")), None)
            s_verre = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("23. S(verre) :")), None)
            v_solution = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("24. V(solution) :")), None)
            debit_solution = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("25. Débit solution :")), None)
            ph_initial = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("26. pH initial (T amb) :")), None)
            ph_final = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("27. pH initial (T essai) :")), None)
            compo_solution = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("28. Compo solution :")), None)
            duree_experience = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("29. Durée expérience :")), None)
            ph_final_amb = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("30. pH final (T amb) :")), None)
            ph_final_test = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("31. pH final (T essai) :")), None)
            normalisation_vitesse = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("32. Normalisation vitesse (Spm ou SBET) :")), None)
            v0_si = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("33. V₀(Si) :")), None)
            r_carre_si = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("34. r²(Si) :")), None)
            ordonnee_origine_si = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("35. Ordonnée origine :")), None)
            v0_b = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("36. V₀(B) :")), None)
            ordonnee_origine_b = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("37. Ordonnée origine :")), None)
            v0_na = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("38. V₀(Na) :")), None)
            r_carre_na = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("39. r²(Na) :")), None)
            ordonnee_origine_na = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("40. Ordonnée origine :")), None)
            v0_dm = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("41. V₀(ΔM) :")), None)
            congruence = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("42. Congruence :")), None)

            # Préparer les données
            url = 'http://127.0.0.1:5001/add_glass_data'
            donnees = {
                "type": type_doc,
                "titre": titre,
                "reference": reference,
                "premier_auteur": premier_auteur,
                "nombre_types_verres": nombre_types_verres,
                "sio2": sio2,
                "b2o3": b2o3,
                "na2o": na2o,
                "al2o3": al2o3,
                "fines": fines,
                "densite": densite,
                "homogeneite": homogeneite,
                "pourcentage_b_iv": pourcentage_b_iv,
                "irradie": irradie,
                "caracteristiques_irradie": caracteristiques_irradie,
                "temperature": temperature,
                "statique_dynamique": statique_dynamique,
                "plage_granulo": plage_granulo,
                "surface_specifique_geometrique": surface_specifique_geometrique,
                "surface_specifique_bet": surface_specifique_bet,
                "qualite_polissage": qualite_polissage,
                "masse_verre": masse_verre,
                "s_verre": s_verre,
                "v_solution": v_solution,
                "debit_solution": debit_solution,
                "ph_initial": ph_initial,
                "ph_final": ph_final,
                "compo_solution": compo_solution,
                "duree_experience": duree_experience,
                "ph_final_amb": ph_final_amb,
                "ph_final_test": ph_final_test,
                "normalisation_vitesse": normalisation_vitesse,
                "v0_si": v0_si,
                "r_carre_si": r_carre_si,
                "ordonnee_origine_si": ordonnee_origine_si,
                "v0_b": v0_b,
                "ordonnee_origine_b": ordonnee_origine_b,
                "v0_na": v0_na,
                "r_carre_na": r_carre_na,
                "ordonnee_origine_na": ordonnee_origine_na,
                "v0_dm": v0_dm,
                "congruence": congruence
            }
            print(f"Envoi des données: {donnees}")

            reponse = requests.post(url, json=donnees)

            if reponse.status_code == 200:
                return Data(value="Données du verre ajoutées avec succès!")
            else:
                return Data(value=f"Erreur lors de l'ajout des données du verre. Code d'état: {reponse.status_code} - {reponse.text}")

        except Exception as e:
            return Data(value=f"Exception survenue: {str(e)}")
