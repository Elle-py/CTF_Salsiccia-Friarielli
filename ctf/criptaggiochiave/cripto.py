import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# Messaggio da criptare
message = b"netsec{m4ng14t1_5t4_p1z24}"

# Generazione della chiave e del vettore di inizializzazione (IV)
key = os.urandom(32)  # 256-bit key
iv = os.urandom(16)   # 128-bit IV

# Creazione del cifrario AES
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()

# Aggiungere padding al messaggio (AES richiede blocchi di lunghezza fissa)
padder = padding.PKCS7(algorithms.AES.block_size).padder()
padded_message = padder.update(message) + padder.finalize()

# Crittografare il messaggio
ciphertext = encryptor.update(padded_message) + encryptor.finalize()

# Salvare il messaggio criptato in un file
with open("encrypted_message.txt", "wb") as file:
    # Salva l'IV e il messaggio crittografato
    file.write(iv + b"  " + ciphertext)

# Salva la chiave in un file separato (da mantenere segreto!)
with open("key.txt", "wb") as key_file:
    key_file.write(key)
