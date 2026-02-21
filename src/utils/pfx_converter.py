from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12

def convert_pfx_file(file_path: str, password: str, output_status):
    try:
        with open(file_path, "rb") as f:
            pfx_data = f.read()

        private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
            pfx_data, password.encode()
        )

        # --- Key export ---
        key_file = file_path + ".key.pem"
        with open(key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # --- Certificate export ---
        cert_file = file_path + ".cer.pem"
        with open(cert_file, "wb") as f:
            f.write(certificate.public_bytes(serialization.Encoding.PEM))

        output_status.value = f"Konvertierung erfolgreich!\nDateien:\n{key_file}\n{cert_file}"
    except Exception as ex:
        output_status.value = f"Fehler: {ex}"
