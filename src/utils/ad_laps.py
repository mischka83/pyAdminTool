from ldap3 import Server, Connection, ALL, SUBTREE, BASE
from utils.config import load_config
from datetime import datetime, timedelta
from ldap3.utils.dn import escape_rdn, parse_dn

def get_laps_group_members(group_name):
    """
    Gibt Mitglieder der AD-Gruppe inkl. TTL zurück.
    Struktur: [{name, display_name, ttl_expiry}, ...]
    """

    config = load_config()
    server = Server(config["ldaps_url"], get_info=ALL)
    conn = Connection(server, user=config["username"], password=config["password"], auto_bind=True)

    results = []

    try:
        # DEBUG
        print(f"[DEBUG] LDAP Filter = (&(objectClass=group)(cn={group_name}))")
        print(f"[DEBUG] group_name = '{group_name}'")

        # --- Gruppensuche ---
        conn.search(
            search_base=config["base_dn"],
            search_filter=f"(&(objectClass=group)(cn={group_name}))",
            search_scope=SUBTREE,
            attributes=["distinguishedName"]
        )

        if not conn.entries:
            return [{"name": f"Gruppe '{group_name}' nicht gefunden", "display_name": "", "ttl_expiry": ""}]

        group_dn = conn.entries[0].distinguishedName.value

        # --- Mitglieder mit TTL laden ---
        ttl_control = ('1.2.840.113556.1.4.2309', True, None)

        conn.search(
            search_base=group_dn,
            search_filter="(objectClass=group)",
            search_scope=BASE,
            attributes=["member"],
            controls=[ttl_control]
        )

        if not conn.entries or "member" not in conn.entries[0]:
            return [{"name": "Keine Mitglieder gefunden", "display_name": "", "ttl_expiry": ""}]

        members = conn.entries[0].member.values

        # --- Mitglieder durchlaufen ---
        for entry in members:

            print(f"[DEBUG] Raw member value: {entry}")

            raw = entry
            ttl_expiry = "N/A"
            dn = raw

            # --------------------------------------------------------------------
            # 1) Microsoft TTL-Format: <TTL=6748509>,CN=....
            # --------------------------------------------------------------------
            if raw.startswith("<TTL="):
                try:
                    ttl_str = raw.split(">")[0]  # "<TTL=12345>"
                    seconds = int(ttl_str.replace("<TTL=", "").replace(">", ""))

                    # DN nach dem ">,"
                    dn = raw.split(">,", 1)[1]

                    expiry_time = datetime.now() + timedelta(seconds=seconds)
                    ttl_expiry = expiry_time.strftime("%d.%m.%Y %H:%M:%S")
                except Exception as ex:
                    print(f"[DEBUG] TTL-Parsing-Fehler (<TTL>): {ex}")

            # --------------------------------------------------------------------
            # 2) Klassisches Format: DN;ttl=12345
            # --------------------------------------------------------------------
            elif ";ttl=" in raw.lower():
                try:
                    dn, ttl_part = raw.split(";ttl=")
                    seconds = int(ttl_part)

                    expiry_time = datetime.now() + timedelta(seconds=seconds)
                    ttl_expiry = expiry_time.strftime("%Y-%m-%d %H:%M:%S")
                except Exception as ex:
                    print(f"[DEBUG] TTL-Parsing-Fehler (;ttl=): {ex}")

            # --------------------------------------------------------------------
            # 3) DN korrekt escapen für LDAP
            # --------------------------------------------------------------------
            try:
                escaped_rdn_parts = []

                # parse_dn liefert Liste von RDNs, jede RDN ist eine Liste von Tupeln
                for rdn_group in parse_dn(dn):
                    escaped_parts = []
                    for attr_val in rdn_group:  # attr_val = (attr, value)
                        attr, val = attr_val
                        escaped_parts.append(escape_rdn(f"{attr}={val}"))
                    # mehrere Attribute in einem RDN mit '+' verbinden
                    escaped_rdn_parts.append("+".join(escaped_parts))

                safe_dn = ",".join(escaped_rdn_parts)

            except Exception as ex:
                print(f"[DEBUG] DN-Parsing-Fehler bei DN={dn}: {ex}")
                # Wir gehen weiter, versuchen den unbereinigten DN direkt:
                safe_dn = dn

            # --------------------------------------------------------------------
            # 4) LDAP-Lookup des Mitglieds (Name + DisplayName)
            # --------------------------------------------------------------------
            display_name = ""
            cn_value = ""

            conn.search(
                search_base=safe_dn,
                search_filter="(objectClass=*)",
                search_scope=BASE,
                attributes=["displayName", "cn"]
            )

            if conn.entries:
                e = conn.entries[0]
                display_name = e.displayName.value if "displayName" in e else None
                cn_value = e.cn.value if "cn" in e else None

            # Fallback, falls kein LDAP Lookup möglich
            if not cn_value:
                cn_value = dn.split(",")[0].replace("CN=", "")

            if not display_name:
                display_name = cn_value

            results.append({
                "name": cn_value,
                "display_name": display_name,
                "ttl_expiry": ttl_expiry
            })

    except Exception as ex:
        results.append({"name": f"Fehler: {ex}", "display_name": "", "ttl_expiry": ""})

    return results
