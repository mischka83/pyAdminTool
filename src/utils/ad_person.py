# utils/ad_person.py
from ldap3 import Server, Connection, ALL
from utils.config import load_config
import csv
from pathlib import Path

EXPORT_FILE = Path("person_details_export.csv")

def escape_ldap_filter(value):
    return value.replace("\\", "\\5c").replace("*", "\\2a").replace("(", "\\28").replace(")", "\\29").replace("\x00", "\\00")

def search_persons(query):
    config = load_config()
    server = Server(config["ldaps_url"], get_info=ALL)
    conn = Connection(server, user=config["username"], password=config["password"], auto_bind=True)
    ldap_filter = f"(&(objectClass=user)(|(displayName=*{query}*)(cn=*{query}*)(givenName=*{query}*)(sn=*{query}*)))"
    conn.search(config["base_dn"], ldap_filter, attributes=["displayName"], size_limit=50)
    return [entry.displayName.value for entry in conn.entries if entry.displayName.value]

def get_person_details(person_name):
    config = load_config()
    server = Server(config["ldaps_url"], get_info=ALL)
    conn = Connection(server, user=config["username"], password=config["password"], auto_bind=True)

    safe_name = escape_ldap_filter(person_name)
    ldap_filter = f"(&(objectClass=user)(|(displayName={safe_name})(cn={safe_name})))"

    conn.search(config["base_dn"], ldap_filter,
                attributes=["givenName", "sn", "displayName", "mail", "department", "title", "telephoneNumber", "memberOf", "samAccountName"],)

    if not conn.entries:
        return None

    entry = conn.entries[0]
    details = {
        "Name": getattr(entry, "samAccountName", None) and entry.samAccountName.value or "",
        "Vorname": getattr(entry, "givenName", None) and entry.givenName.value or "",
        "Nachname": getattr(entry, "sn", None) and entry.sn.value or "",
        "DisplayName": getattr(entry, "displayName", None) and entry.displayName.value or "",
        "E-Mail": getattr(entry, "mail", None) and entry.mail.value or "",
        "Abteilung": getattr(entry, "department", None) and entry.department.value or "",
        "Titel": getattr(entry, "title", None) and entry.title.value or "",
        "Telefon": getattr(entry, "telephoneNumber", None) and entry.telephoneNumber.value or "",
        "Gruppen": [dn.split(",")[0].replace("CN=", "") for dn in entry.memberOf.values] if getattr(entry, "memberOf", None) else []
    }
    return details

def export_person_details(details):
    with open(EXPORT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Attribut", "Wert"])
        for key, value in details.items():
            if key == "Gruppen":
                writer.writerow([key, ", ".join(value)])
            else:
                writer.writerow([key, value])
    return EXPORT_FILE
