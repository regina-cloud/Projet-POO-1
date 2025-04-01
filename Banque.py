import random
import os

# Classe ClientUtilisateur

class ClientUtilisateur:
    def init(self, nom_complet, adresse, telephone, cnic, login, mot_de_passe, limite_retrait):
        self.nom_complet = nom_complet
        self.adresse = adresse
        self.telephone = telephone
        self.cnic = cnic
        self.login = login
        self.mot_de_passe = mot_de_passe
        self.limite_retrait = limite_retrait
        self.solde = 0
        self.numero_carte = str(random.randint(1000000000000000, 9999999999999999))
        self.type_compte = self.definir_type_compte()

    def definir_type_compte(self):
        if self.limite_retrait <= 500000:
            return "Bronze"
        elif self.limite_retrait <= 1000000:
            return "Or"
        elif self.limite_retrait <= 20000000:
            return "Affaires"
        return "Invalide"

    def deposer(self, montant):
        self.solde += montant
        print(f" Dépôt de {montant} FCFA effectué. Nouveau solde : {self.solde} FCFA.")
        self.enregistrer_transaction("DEPOT", montant)

    def retirer(self, montant):
        if montant > self.solde:
            print(" Fonds insuffisants.")
            return False
        if montant > self.limite_retrait:
            print(f" Montant supérieur à votre limite quotidienne ({self.limite_retrait} FCFA).")
            return False

        self.solde -= montant
        print(f" Retrait de {montant} FCFA effectué. Nouveau solde : {self.solde} FCFA.")
        self.enregistrer_transaction("RETRAIT", montant)
        return True

    def consulter_solde(self):
        return self.solde

    def effectuer_virement(self, destinataire, montant):
        if montant > self.solde:
            print(" Fonds insuffisants pour le virement.")
            return False

        self.solde -= montant
        print(f" Virement de {montant} FCFA effectué vers {destinataire}. Nouveau solde : {self.solde} FCFA.")
        self.enregistrer_transaction("VIREMENT", montant, destinataire)
        return True

    def afficher_historique(self):
        print("\n===  Historique des Transactions ===")
        try:
            with open("transactions.txt", "r") as file:
                transactions = [ligne.strip() for ligne in file.readlines()]
                for transaction in transactions:
                    infos = transaction.split(",")
                    if infos[0] == self.numero_carte:
                        print(f"{infos[1]} | Montant: {infos[2]} FCFA | Destinataire: {infos[3]}")
        except FileNotFoundError:
            print(" Aucun historique disponible.")

    def enregistrer_transaction(self, type_transaction, montant, destinataire=""):
        with open("transactions.txt", "a") as file:
            file.write(f"{self.numero_carte},{type_transaction},{montant},{destinataire}\n")



# Classe EmployeBancaire

class EmployeBancaire:
    def init(self):
        self.nom = "Admin"
        self.identifiant = "admin123"
        self.mot_de_passe = "securepass"

    def approuver_compte(self, client):
        print(f" Vérification des informations pour {client.nom_complet}...")
        if client.cnic and client.numero_carte:
            print(f" Compte de {client.nom_complet} approuvé.")
            self.enregistrer_client(client)
        else:
            print(" Informations invalides. Compte refusé.")

    def enregistrer_client(self, client):
        with open("users.txt", "a") as file:
            file.write(f"{client.numero_carte},{client.nom_complet},{client.adresse},{client.cnic},{client.login},{client.mot_de_passe},{client.solde},{client.type_compte}\n")
        print(f" Compte de {client.nom_complet} enregistré.")

    def authentifier_utilisateur(self, login, mot_de_passe):
        try:
            with open("users.txt", "r") as file:
                for ligne in file:
                    donnees = ligne.strip().split(",")
                    if donnees[4] == login and donnees[5] == mot_de_passe:
                        print(f" Connexion réussie. Bienvenue, {donnees[1]} !")
                        return ClientUtilisateur(donnees[1], donnees[2], "", donnees[3], donnees[4], donnees[5], int(donnees[6]))
            print(" Identifiants incorrects.")
            return None
        except FileNotFoundError:
            print(" Erreur : Fichier users.txt introuvable.")
            return None



#  Menus Interactifs

def menu_principal():
    employe = EmployeBancaire()
    
    while True:
        print("\n===  MENU PRINCIPAL ===")
        print(" Créer un compte")
        print("  Se connecter")
        print("  Quitter")
        choix = input("➡  Choisissez une option : ")

        if choix == "1":
            print("\n=== Création de Compte ===")
            nom = input(" Nom complet : ")
            adresse = input(" Adresse : ")
            telephone = input(" Téléphone : ")
            cnic = input(" CNI ou passeport : ")
            login = input(" Login : ")
            mot_de_passe = input(" Mot de passe : ")
            limite = int(input(" Limite de retrait (500000, 1000000, 20000000) : "))

            client = ClientUtilisateur(nom, adresse, telephone, cnic, login, mot_de_passe, limite)
            print(f" Type de compte attribué : {client.type_compte}")
            employe.approuver_compte(client)

        elif choix == "2":
            login = input(" Entrez votre login : ")
            mot_de_passe = input(" Entrez votre mot de passe : ")

            client = employe.authentifier_utilisateur(login, mot_de_passe)
            if client:
                menu_utilisateur(client)

        elif choix == "3":
            print(" Merci d'avoir utilisé notre banque. À bientôt !")
            break


def menu_utilisateur(client):
    while True:
        print(f"\n===  MENU {client.nom_complet} ===")
        print("1  Déposer des fonds")
        print("2  Retirer des fonds")
        print("3  Consulter le solde")
        print("4  Effectuer un virement")
        print("5  Voir l'historique des transactions")
        print("6  Déconnexion")
        choix = input("➡  Choisissez une option : ")

        if choix == "1":
            montant = float(input(" Montant à déposer : "))
            client.deposer(montant)

        elif choix == "2":
            montant = float(input(" Montant à retirer : "))
            client.retirer(montant)

        elif choix == "3":
            print(f" Solde actuel : {client.consulter_solde()} FCFA")

        elif choix == "4":
            destinataire = input(" Numéro du destinataire : ")
            montant = float(input(" Montant à transférer : "))
            client.effectuer_virement(destinataire, montant)

        elif choix == "5":
            client.afficher_historique()

        elif choix == "6":
            print(" Déconnexion réussie.")
            break



#   Lancer l'application


import random
from datetime import datetime

class ClientUtilisateur:
    def _init_(self, nom, adresse, telephone, cnic, login, mot_de_passe, limite_retrait):
        self.nom = nom
        self.adresse = adresse
        self.telephone = telephone
        self.cnic = cnic
        self.login = login
        self.mot_de_passe = mot_de_passe
        self.limite_retrait = limite_retrait


    def generer_id(self):
        return str(random.randint(100000, 999999))
    
    def enregistrer_utilisateur(self):
        with open("users.txt", "a") as file:
            file.write(f"{self.id},{self.nom},{self.adresse},{self.cnic},{self.login},{self.mot_de_passe},{self.solde}\n")
        print(f"Utilisateur {self.nom} enregistré avec succès (ID : {self.id}).")

    def deposer(self, montant):
        self.solde += montant
        self.enregistrer_transaction(montant, "Dépôt")
        print(f"{montant} FCFA déposés. Solde : {self.solde} FCFA")
    
    def retirer(self, montant):
        if montant > self.solde or montant > self.limite:
            print("Opération refusée : Fonds insuffisants ou dépassement de limite.")
            return
        self.solde -= montant
        self.enregistrer_transaction(montant, "Retrait")
        print(f"{montant} FCFA retirés. Solde : {self.solde} FCFA")
    
    def enregistrer_transaction(self, montant, type_transaction):
        with open("transactions.txt", "a") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{self.id},{montant},{type_transaction}\n")

class ClientEntreprise:
    def _init_(self, nom_entreprise, adresse_entreprise, numero_fiscal, login, mot_de_passe, limite):
        self.nom_entreprise = nom_entreprise
        self.adresse_entreprise = adresse_entreprise
        self.numero_fiscal = numero_fiscal
        self.login = login
        self.mot_de_passe = mot_de_passe
        self.limite = limite
        self.solde = 0
        self.id_entreprise = self.generer_id_entreprise()
    
    def generer_id_entreprise(self):
        return str(random.randint(100000, 999999))
    
    def enregistrer_entreprise(self):
        with open("companies.txt", "a") as file:
            file.write(f"{self.id_entreprise},{self.nom_entreprise},{self.adresse_entreprise},{self.numero_fiscal},{self.login},{self.mot_de_passe},{self.solde}\n")
        print(f"Entreprise {self.nom_entreprise} enregistrée (ID : {self.id_entreprise}).")
    
    def deposer(self, montant):
        self.solde += montant
        self.enregistrer_transaction(montant, "Dépôt")
        print(f"{montant} FCFA déposés. Solde : {self.solde} FCFA")
    
    def retirer(self, montant):
        if montant > self.solde or montant > self.limite:
            print("Opération refusée : Fonds insuffisants ou dépassement de limite.")
            return
        self.solde -= montant
        self.enregistrer_transaction(montant, "Retrait")
        print(f"{montant} FCFA retirés. Solde : {self.solde} FCFA")
    
    def enregistrer_transaction(self, montant, type_transaction):
        with open("transactions.txt", "a") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{self.id_entreprise},{montant},{type_transaction}\n")

def authentifier_entreprise(login, mot_de_passe):
    try:
        with open("companies.txt", "r") as file:
            for ligne in file:
                donnees = ligne.strip().split(",")
                if donnees[4] == login and donnees[5] == mot_de_passe:
                    print(f"Connexion réussie, entreprise {donnees[1]} !")
                    return True, donnees[0]
        print("Échec de connexion : Identifiants incorrects.")
        return False, None
    except FileNotFoundError:
        print("Erreur : Fichier companies.txt introuvable.")
        return False, None

def menu_entreprise(id_entreprise):
    entreprise = ClientEntreprise("", "", "", "", "", 0)
    entreprise.id_entreprise = id_entreprise
    while True:
        print("\n=== Menu Entreprise ===")
        print("1. Déposer des fonds")
        print("2. Retirer des fonds")
        print("3. Se déconnecter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            montant = float(input("Montant à déposer : "))
            entreprise.deposer(montant)
        elif choix == "2":
            montant = float(input("Montant à retirer : "))
            entreprise.retirer(montant)
        elif choix == "3":
            print("Déconnexion réussie.")
            break
        else:
            print("Option invalide.")

def menu_principal():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Créer un compte utilisateur")
        print("2. Créer un compte entreprise")
        print("3. Se connecter (Entreprise)")
        print("4. Quitter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            nom = input("Nom complet : ")
            adresse = input("Adresse : ")
            telephone = input("Téléphone : ")
            cnic = input("CNI ou passeport : ")
            login = input("Login : ")
            mot_de_passe = input("Mot de passe : ")
            limite = int(input("Limite de retrait (500000, 1000000, 20000000) : "))
            client = ClientUtilisateur(nom, adresse, telephone, cnic, login, mot_de_passe, limite)
            client.enregistrer_utilisateur()
        elif choix == "2":
            nom_entreprise = input("Nom de l’entreprise : ")
            adresse_entreprise = input("Adresse : ")
            numero_fiscal = input("Numéro fiscal : ")
            login = input("Login : ")
            mot_de_passe = input("Mot de passe : ")
            limite = int(input("Limite de retrait (1000000, 20000000) : "))
            entreprise = ClientEntreprise(nom_entreprise, adresse_entreprise, numero_fiscal, login, mot_de_passe, limite)
            entreprise.enregistrer_entreprise()
        elif choix == "3":
            login = input("Login : ")
            mot_de_passe = input("Mot de passe : ")
            success, id_entreprise = authentifier_entreprise(login, mot_de_passe)
            if success:
                menu_entreprise(id_entreprise)
        elif choix == "4":
            print("Merci et au revoir !")
            break

menu_principal()
