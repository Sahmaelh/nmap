import nmap
import mysql.connector

# Fonction pour exécuter Nmap sur une adresse IP ou plage d'adresses IP
def run_nmap_scan(target):
    nm = nmap.PortScanner()
    nm.scan(hosts=target, arguments='-F')  # Vous pouvez modifier les arguments Nmap selon vos besoins

    # Retourner les résultats du scan
    return nm.all_hosts(), nm.csv()

# Connexion à la base de données MySQL
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host='Votre_Hôte',
            user='Votre_Utilisateur',
            password='Votre_Mot_de_passe',
            database='Votre_Base_de_données'
        )
        return conn
    except mysql.connector.Error as err:
        print("Erreur lors de la connexion à MySQL :", err)
        return None

# Fonction pour insérer les résultats dans la base de données MySQL
def save_scan_results_to_mysql(conn, hosts, scan_results):
    cursor = conn.cursor()
    for host in hosts:
        try:
            sql = "INSERT INTO scan_results (ip, results) VALUES (%s, %s)"
            val = (host, scan_results)
            cursor.execute(sql, val)
            conn.commit()
        except mysql.connector.Error as err:
            print("Erreur lors de l'insertion des résultats :", err)
            conn.rollback()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    target = "Adresse_IP_ou_Plage_d'adresses_IP"  # Remplacez par l'adresse IP ou la plage d'adresses que vous voulez scanner

    # Exécuter le scan Nmap
    hosts, scan_results = run_nmap_scan(target)

    # Sauvegarder les résultats dans la base de données MySQL
    connection = connect_to_mysql()
    if connection:
        save_scan_results_to_mysql(connection, hosts, scan_results)