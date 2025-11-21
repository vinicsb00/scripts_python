import os
import json
import shutil
from datetime import datetime

def consulta_config():
    with open("config.json", "r") as f:
        return json.load(f)

def destino_check(destino):
    if not os.path.exists(destino):
        return None

    backups = [
        os.path.join(destino, pasta)
        for pasta in os.listdir(destino)
        if pasta.startswith("backup_")
    ]

    if not backups:
        return None

    return max(backups, key=os.path.getmtime)

def backup_incremental():
    config = consulta_config()
    source = config["source"]
    destination = config["destination"]

    # criar pasta de backup
    os.makedirs(destination, exist_ok=True)

    # veriificar ult backup
    ultimo_backup = destino_check(destination)

    # Criar novo com data e hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    novo_backup = os.path.join(destination, f"backup_{timestamp}")
    os.makedirs(novo_backup)

    # pasta de log
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "backup.log")
    log = open(log_path, "a", encoding="utf-8")

    print("Fazendo Backup Incrimental")

    for arquivo in os.listdir(source):
        caminho_original = os.path.join(source, arquivo)
        caminho_novo = os.path.join(novo_backup, arquivo)

        if not os.path.isfile(caminho_original):
            continue

        copiar = False

        # se não teve backup anterior, faça
        if not ultimo_backup:
            copiar = True
        else:
            caminho_antigo = os.path.join(ultimo_backup, arquivo)

            # se o arquivo não tem no ultimo backup faz
            if not os.path.exists(caminho_antigo):
                copiar = True
            else:
                # verifica as datas
                mod_src = os.path.getmtime(caminho_original)
                mod_old = os.path.getmtime(caminho_antigo)

                if mod_src > mod_old: 
                    copiar = True

        if copiar:
            shutil.copy2(caminho_original, caminho_novo)
            log.write(f"{datetime.now()} - Copiado: {arquivo}\n")
            print(f"✔ Arquivo novo/modificado: {arquivo}")
        else:
            # não copia
            print(f"- Arquivo sem alterações: {arquivo}")

    log.close()
    print("Backup incremental concluído!")

if __name__ == "__main__":
    backup_incremental()
