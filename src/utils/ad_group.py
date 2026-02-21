# utils/ad_group.py
from ldap3 import Server, Connection, ALL
from utils.config import load_config
import csv
from pathlib import Path

EXPORT_FILE = Path("members_export.csv")

def search_groups(query):
    """Sucht Gruppen im AD und gibt eine Liste von Gruppennamen zurück."""
    config = load_config()
    server = Server(config["ldaps_url"], get_info=ALL)
    conn = Connection(server, user=config["username"], password=config["password"], auto_bind=True)
    conn.search(config["base_dn"], f"(cn={query}*)", attributes=["cn"])
    return [entry.cn.value for entry in conn.entries]

def get_group_members(group_name):
    """Lädt Mitglieder einer Gruppe und gibt eine Liste von Dicts zurück."""
    config = load_config()
    server = Server(config["ldaps_url"], get_info=ALL)
    conn = Connection(server, user=config["username"], password=config["password"], auto_bind=True)
    conn.search(config["base_dn"], f"(cn={group_name})", attributes=["member"])
    members = []
    if conn.entries and "member" in conn.entries[0]:
        for m in conn.entries[0].member.values:
            cn = m.split(",")[0].replace("CN=", "")
            conn.search(config["base_dn"], f"(distinguishedName={m})", attributes=["displayName", "name"])
            display_name = conn.entries[0].displayName.value if conn.entries else "Unbekannt"
            if conn.entries and hasattr(conn.entries[0], "name"):
                cn = conn.entries[0].name.value
            members.append({"name": cn, "display_name": display_name})
    return members

def export_members_to_csv(members):
    """Exportiert Mitgliederliste als CSV."""
    with open(EXPORT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Display Name"])
        for m in members:
            writer.writerow([m["name"], m["display_name"]])
