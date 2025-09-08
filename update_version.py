import json
import os

# Recupera la versione dalla variabile d'ambiente
version = os.environ.get("VERSION", "0.0.0")

# Path al package.json
package_json_path = "package.json"

# Legge il file
with open(package_json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Aggiorna la versione
data["version"] = version

# Scrive il file aggiornato
with open(package_json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
