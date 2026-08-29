"""
data_manager.py - Gestor de persistencia y cálculos para Operación Bikini 🌴👙☀️
Maneja el almacenamiento en JSON con auto-sincronización en la nube (GitHub API),
registro de participantes, pesajes históricos, métricas y estado de la competencia.
"""

import json
import os
import base64
from datetime import datetime, date
from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
import requests

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "operacion_bikini.json")
BACKUPS_DIR = os.path.join(DATA_DIR, "backups")

# Fecha de cierre de la competencia (17 de Noviembre del año en curso)
DEADLINE_MONTH = 11
DEADLINE_DAY = 17


def _get_github_config() -> Optional[Dict[str, str]]:
    """Obtiene la configuración de GitHub desde st.secrets si está disponible."""
    try:
        import streamlit as st
        if "github" in st.secrets:
            cfg = st.secrets["github"]
            token = cfg.get("token", "").strip()
            repo = cfg.get("repo", "").strip()
            if token and repo:
                return {
                    "token": token,
                    "repo": repo,
                    "branch": cfg.get("branch", "main").strip(),
                    "file_path": cfg.get("file_path", "data/operacion_bikini.json").strip()
                }
    except Exception:
        pass
    return None


def is_github_sync_active() -> bool:
    """Verifica si la sincronización con GitHub está configurada en secrets."""
    return _get_github_config() is not None


def get_github_repo_name() -> str:
    """Retorna el nombre del repositorio configurado o vacío."""
    cfg = _get_github_config()
    return cfg.get("repo", "") if cfg else ""


def test_github_connection() -> Tuple[bool, str]:
    """Prueba la conexión con la API de GitHub usando los secrets configurados."""
    config = _get_github_config()
    if not config:
        return False, "No se encontró la configuración [github] en Streamlit Secrets. Sigue los pasos de configuración abajo."
    
    token = config.get("token", "")
    repo = config.get("repo", "")
    if not token or not repo:
        return False, "Falta 'token' o 'repo' en la configuración de [github]."
        
    try:
        url = f"https://api.github.com/repos/{repo}/contents/{config['file_path']}?ref={config['branch']}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code == 200:
            return True, f"¡Conexión exitosa con el repositorio '{repo}'! El archivo '{config['file_path']}' se lee y sincroniza correctamente."
        elif res.status_code == 401:
            return False, "Error de autenticación (401): El Token de GitHub es inválido o expiró."
        elif res.status_code == 404:
            return False, f"No se encontró el repositorio '{repo}' o el archivo '{config['file_path']}' (404). Verifica que el nombre del repositorio sea exacto (ej: 'tu-usuario/nombre-repo')."
        else:
            return False, f"GitHub respondió con código {res.status_code}: {res.text}"
    except Exception as e:
        return False, f"Error de conexión con GitHub: {e}"


def _fetch_from_github(config: Dict[str, str]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Obtiene los datos más recientes directamente desde GitHub API."""
    try:
        url = f"https://api.github.com/repos/{config['repo']}/contents/{config['file_path']}?ref={config['branch']}"
        headers = {
            "Authorization": f"Bearer {config['token']}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code == 200:
            json_resp = res.json()
            content_b64 = json_resp.get("content", "")
            sha = json_resp.get("sha")
            raw_bytes = base64.b64decode(content_b64)
            data = json.loads(raw_bytes.decode("utf-8"))
            if "users" not in data:
                data["users"] = {}
            # Actualizar copia local en caché de disco
            _ensure_data_file()
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return data, sha
    except Exception as e:
        print(f"[GitHub Sync] Error al leer de GitHub: {e}")
    return None, None


def _push_to_github(
    config: Dict[str, str],
    data_dict: Dict[str, Any],
    target_file_path: Optional[str] = None,
    commit_msg: Optional[str] = None
) -> bool:
    """Sube una versión del JSON a GitHub haciendo un commit automático."""
    try:
        f_path = target_file_path or config["file_path"]
        url = f"https://api.github.com/repos/{config['repo']}/contents/{f_path}"
        headers = {
            "Authorization": f"Bearer {config['token']}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        # Obtener el SHA actual del archivo remoto si ya existe
        get_res = requests.get(f"{url}?ref={config['branch']}", headers=headers, timeout=6)
        sha = None
        if get_res.status_code == 200:
            sha = get_res.json().get("sha")
            
        json_str = json.dumps(data_dict, ensure_ascii=False, indent=2)
        content_b64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
        
        msg = commit_msg or f"📊 Auto-guardado pesajes [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [skip ci]"
        payload = {
            "message": msg,
            "content": content_b64,
            "branch": config["branch"]
        }
        if sha:
            payload["sha"] = sha
            
        put_res = requests.put(url, headers=headers, json=payload, timeout=8)
        if put_res.status_code in [200, 201]:
            return True
        else:
            print(f"[GitHub Sync] Error al guardar en GitHub ({f_path}): Status {put_res.status_code} - {put_res.text}")
            return False
    except Exception as e:
        print(f"[GitHub Sync] Excepción al guardar en GitHub ({f_path}): {e}")
        return False


def _ensure_data_file() -> None:
    """Asegura que los directorios data/, data/backups/ y el archivo principal existan."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(BACKUPS_DIR):
        os.makedirs(BACKUPS_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"users": {}}, f, ensure_ascii=False, indent=2)


def load_data() -> Dict[str, Any]:
    """
    Carga los datos del archivo JSON. Si hay conexión configurada con GitHub,
    descarga la versión más actualizada de la nube.
    """
    config = _get_github_config()
    if config:
        cloud_data, _ = _fetch_from_github(config)
        if cloud_data is not None:
            return cloud_data

    _ensure_data_file()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "users" not in data:
                data["users"] = {}
            return data
    except (json.JSONDecodeError, OSError):
        return {"users": {}}

# Variable global para rastrear el estado de la última sincronización
_last_sync_result = {"success": None, "message": "", "timestamp": ""}


def get_last_sync_status() -> Dict[str, Any]:
    """Retorna el estado de la última sincronización con GitHub."""
    return _last_sync_result.copy()


def save_data(data: Dict[str, Any]) -> None:
    """
    Guarda los datos en el archivo principal Y en una copia con fecha diaria
    (tanto en disco local como en GitHub).
    """
    global _last_sync_result
    
    _ensure_data_file()
    
    # 1. Guardar archivo principal local
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 2. Guardar copia histórica local con fecha del día
    today_str = date.today().strftime("%Y-%m-%d")
    backup_file_local = os.path.join(BACKUPS_DIR, f"operacion_bikini_{today_str}.json")
    with open(backup_file_local, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 3. Sincronizar en GitHub (archivo principal + copia fechada)
    config = _get_github_config()
    if config:
        # Subir archivo principal
        ok_main = _push_to_github(config, data)
        # Subir copia con fecha a la carpeta backups/ de GitHub
        backup_git_path = f"data/backups/operacion_bikini_{today_str}.json"
        _push_to_github(
            config,
            data,
            target_file_path=backup_git_path,
            commit_msg=f"💾 Respaldo diario [{today_str}] [skip ci]"
        )
        
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if ok_main:
            _last_sync_result = {
                "success": True,
                "message": f"Datos guardados y respaldados con fecha {today_str} en GitHub.",
                "timestamp": ts
            }
        else:
            _last_sync_result = {
                "success": False,
                "message": f"Error al sincronizar con GitHub. Los datos se guardaron localmente.",
                "timestamp": ts
            }
    else:
        _last_sync_result = {
            "success": None,
            "message": f"GitHub no configurado. Respaldo guardado localmente ({today_str}).",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }


def list_available_backups() -> List[str]:
    """Retorna la lista de fechas disponibles de copias de seguridad (ej: ['2026-08-29'])."""
    _ensure_data_file()
    dates_found = set()
    
    # 1. Buscar en backups locales
    if os.path.exists(BACKUPS_DIR):
        for f in os.listdir(BACKUPS_DIR):
            if f.startswith("operacion_bikini_") and f.endswith(".json"):
                d_str = f.replace("operacion_bikini_", "").replace(".json", "")
                dates_found.add(d_str)

    # 2. Si hay conexión con GitHub, consultar lista de backups remotos
    config = _get_github_config()
    if config:
        try:
            url = f"https://api.github.com/repos/{config['repo']}/contents/data/backups?ref={config['branch']}"
            headers = {
                "Authorization": f"Bearer {config['token']}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                for item in res.json():
                    name = item.get("name", "")
                    if name.startswith("operacion_bikini_") and name.endswith(".json"):
                        d_str = name.replace("operacion_bikini_", "").replace(".json", "")
                        dates_found.add(d_str)
        except Exception:
            pass

    return sorted(list(dates_found), reverse=True)


def restore_backup_by_date(date_str: str) -> Tuple[bool, str]:
    """
    Restaura la base de datos a partir de una copia de seguridad con fecha dada.
    """
    date_str = date_str.strip()
    data_to_restore = None
    
    # 1. Intentar leer de local
    local_path = os.path.join(BACKUPS_DIR, f"operacion_bikini_{date_str}.json")
    if os.path.exists(local_path):
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                data_to_restore = json.load(f)
        except Exception:
            pass
            
    # 2. Si no está en local, intentar descargar de GitHub
    if not data_to_restore:
        config = _get_github_config()
        if config:
            try:
                url = f"https://api.github.com/repos/{config['repo']}/contents/data/backups/operacion_bikini_{date_str}.json?ref={config['branch']}"
                headers = {
                    "Authorization": f"Bearer {config['token']}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
                res = requests.get(url, headers=headers, timeout=6)
                if res.status_code == 200:
                    raw_bytes = base64.b64decode(res.json().get("content", ""))
                    data_to_restore = json.loads(raw_bytes.decode("utf-8"))
            except Exception as e:
                return False, f"Error al descargar copia de GitHub: {e}"
                
    if not data_to_restore or "users" not in data_to_restore:
        return False, f"No se pudo encontrar o leer la copia del {date_str}."
        
    # Guardar como base de datos activa y sincronizar
    save_data(data_to_restore)
    user_count = len(data_to_restore.get("users", {}))
    return True, f"¡Copia del {date_str} restaurada con éxito! ({user_count} participantes recuperadas)"


def restore_from_json_dict(data_dict: Dict[str, Any]) -> Tuple[bool, str]:
    """Valida y restaura una base de datos desde un diccionario JSON cargado manualmente."""
    if not isinstance(data_dict, dict) or "users" not in data_dict:
        return False, "El archivo JSON no tiene un formato válido (debe contener la clave 'users')."
        
    save_data(data_dict)
    user_count = len(data_dict.get("users", {}))
    return True, f"¡Archivo restaurado con éxito! ({user_count} participantes activadas)"



def get_deadline(year: Optional[int] = None) -> datetime:
    """Obtiene el objeto datetime de la fecha límite (17 de Noviembre a las 23:59:59)."""
    current_year = year or datetime.now().year
    return datetime(current_year, DEADLINE_MONTH, DEADLINE_DAY, 23, 59, 59)


def get_competition_status(year: Optional[int] = None) -> Tuple[bool, int, str]:
    """
    Calcula si la competencia está cerrada y cuántos días faltan.
    Retorna: (is_closed, days_left, deadline_formatted_str)
    """
    deadline = get_deadline(year)
    now = datetime.now()
    diff = deadline - now
    
    is_closed = now > deadline
    days_left = max(0, diff.days) if not is_closed else 0
    deadline_str = deadline.strftime("%d/%m/%Y")
    
    return is_closed, days_left, deadline_str


def get_all_users() -> List[str]:
    """Retorna la lista de apodos de todas las usuarias registradas."""
    data = load_data()
    return sorted(list(data["users"].keys()))


def add_user(nickname: str, start_weight: float, target_weight: float, entry_date: Optional[str] = None) -> Tuple[bool, str]:
    """
    Registra una nueva participante y añade su peso inicial con la fecha indicada.
    """
    nickname = nickname.strip()
    if not nickname:
        return False, "El apodo no puede estar vacío."
    
    data = load_data()
    if nickname.lower() in [u.lower() for u in data["users"].keys()]:
        return False, f"Ya existe una participante con el apodo '{nickname}'."
    
    if start_weight <= 0 or target_weight <= 0:
        return False, "Los pesos deben ser mayores a 0 kg."

    today_str = entry_date or date.today().strftime("%Y-%m-%d")
    
    data["users"][nickname] = {
        "start_weight": round(float(start_weight), 1),
        "target_weight": round(float(target_weight), 1),
        "created_at": today_str,
        "weights": [
            {
                "date": today_str,
                "weight": round(float(start_weight), 1)
            }
        ]
    }
    
    save_data(data)
    return True, f"¡Bienvenida {nickname} a Operación Bikini! 🏖️💃"


def log_weight(nickname: str, weight: float, entry_date: Optional[str] = None) -> Tuple[bool, str]:
    """
    Registra o actualiza el peso de una usuaria para una fecha dada.
    """
    is_closed, _, deadline_str = get_competition_status()
    if is_closed:
        return False, f"La competencia finalizó el {deadline_str}. Ya no se pueden cargar nuevos pesos."

    nickname = nickname.strip()
    data = load_data()
    if nickname not in data["users"]:
        return False, f"La participante '{nickname}' no está registrada."
    
    if weight <= 0:
        return False, "El peso debe ser mayor a 0 kg."
    
    weight = round(float(weight), 1)
    target_date = entry_date or date.today().strftime("%Y-%m-%d")
    
    weights = data["users"][nickname]["weights"]
    
    # Verificar si ya existe pesaje en esa fecha para actualizarlo
    found = False
    for item in weights:
        if item["date"] == target_date:
            item["weight"] = weight
            found = True
            break
            
    if not found:
        weights.append({"date": target_date, "weight": weight})
        
    # Ordenar por fecha cronológica
    weights.sort(key=lambda x: x["date"])
    data["users"][nickname]["weights"] = weights
    
    # Si la fecha cargada es anterior a la fecha inicial registrada, actualizar el peso inicial
    if len(weights) > 0:
        data["users"][nickname]["start_weight"] = weights[0]["weight"]
        data["users"][nickname]["created_at"] = weights[0]["date"]
    
    save_data(data)
    action_text = "actualizado" if found else "registrado"
    return True, f"¡Pesaje de {weight} kg {action_text} con éxito para {nickname} ({target_date})! 👙✨"


def update_weight_entry(nickname: str, date_str: str, new_weight: float) -> Tuple[bool, str]:
    """Modifica el peso de una fecha específica."""
    data = load_data()
    if nickname not in data["users"]:
        return False, "Participante no encontrada."
    
    if new_weight <= 0:
        return False, "El peso debe ser mayor a 0 kg."
    
    weights = data["users"][nickname]["weights"]
    found = False
    for item in weights:
        if item["date"] == date_str:
            item["weight"] = round(float(new_weight), 1)
            found = True
            break
            
    if not found:
        return False, f"No se encontró un registro para la fecha {date_str}."
        
    # Re-sincronizar peso inicial si se modificó el primer registro
    if weights and weights[0]["date"] == date_str:
        data["users"][nickname]["start_weight"] = round(float(new_weight), 1)

    save_data(data)
    return True, f"Registro del {date_str} modificado correctamente a {new_weight} kg."


def delete_weight_entry(nickname: str, date_str: str) -> Tuple[bool, str]:
    """Elimina un registro de pesaje específico (mínimo debe quedar 1 registro)."""
    data = load_data()
    if nickname not in data["users"]:
        return False, "Participante no encontrada."
        
    weights = data["users"][nickname]["weights"]
    if len(weights) <= 1:
        return False, "No puedes eliminar el único pesaje registrado de la participante."
        
    new_weights = [item for item in weights if item["date"] != date_str]
    if len(new_weights) == len(weights):
        return False, f"No se encontró registro para la fecha {date_str}."
        
    data["users"][nickname]["weights"] = new_weights
    
    # Re-sincronizar peso inicial
    if new_weights:
        data["users"][nickname]["start_weight"] = new_weights[0]["weight"]
        data["users"][nickname]["created_at"] = new_weights[0]["date"]

    save_data(data)
    return True, f"Registro del {date_str} eliminado exitosamente."


def delete_user(nickname: str) -> Tuple[bool, str]:
    """Elimina una participante por completo."""
    data = load_data()
    if nickname in data["users"]:
        del data["users"][nickname]
        save_data(data)
        return True, f"Participante '{nickname}' eliminada del sistema."
    return False, "Participante no encontrada."


def get_user_stats(nickname: str) -> Optional[Dict[str, Any]]:
    """
    Calcula todas las métricas de progreso de una participante.
    """
    data = load_data()
    if nickname not in data["users"]:
        return None
        
    user = data["users"][nickname]
    start_weight = user["start_weight"]
    target_weight = user["target_weight"]
    weights = user.get("weights", [])
    
    if not weights:
        return None
        
    weights_sorted = sorted(weights, key=lambda x: x["date"])
    current_entry = weights_sorted[-1]
    current_weight = current_entry["weight"]
    latest_date = current_entry["date"]
    
    # Variación vs último pesaje anterior
    if len(weights_sorted) > 1:
        prev_weight = weights_sorted[-2]["weight"]
        last_delta = round(current_weight - prev_weight, 1)
        prev_date = weights_sorted[-2]["date"]
    else:
        last_delta = 0.0
        prev_date = latest_date
        
    # Variación total acumulada
    total_delta = round(current_weight - start_weight, 1)
    total_lost = round(start_weight - current_weight, 1)
    
    # Distancia a la meta
    remaining_to_goal = round(current_weight - target_weight, 1)
    total_target_loss = round(start_weight - target_weight, 1)
    
    if total_target_loss > 0:
        progress_pct = round((total_lost / total_target_loss) * 100, 1)
    else:
        progress_pct = 100.0 if current_weight <= target_weight else 0.0
        
    goal_achieved = current_weight <= target_weight
    
    return {
        "nickname": nickname,
        "start_weight": start_weight,
        "target_weight": target_weight,
        "current_weight": current_weight,
        "latest_date": latest_date,
        "prev_date": prev_date,
        "last_delta": last_delta,
        "total_delta": total_delta,
        "total_lost": total_lost,
        "remaining_to_goal": remaining_to_goal,
        "total_target_loss": total_target_loss,
        "progress_pct": progress_pct,
        "goal_achieved": goal_achieved,
        "history": weights_sorted
    }


def get_all_stats() -> List[Dict[str, Any]]:
    """Retorna las estadísticas de todas las participantes."""
    users = get_all_users()
    stats_list = []
    for u in users:
        st = get_user_stats(u)
        if st:
            stats_list.append(st)
    return stats_list


def get_hall_of_fame() -> List[Dict[str, Any]]:
    """Retorna las participantes que alcanzaron su objetivo."""
    all_stats = get_all_stats()
    achieved = [st for st in all_stats if st["goal_achieved"]]
    achieved.sort(key=lambda x: x["total_lost"], reverse=True)
    return achieved


def get_all_weights_dataframe() -> pd.DataFrame:
    """
    Retorna un DataFrame consolidado con el historial de todas las usuarias para graficar.
    """
    data = load_data()
    rows = []
    for nick, user_info in data.get("users", {}).items():
        start_w = user_info["start_weight"]
        target_w = user_info["target_weight"]
        for entry in user_info.get("weights", []):
            rows.append({
                "Fecha": entry["date"],
                "Participante": nick,
                "Peso (kg)": entry["weight"],
                "Peso Inicial": start_w,
                "Objetivo (kg)": target_w,
                "Kilos Bajados": round(start_w - entry["weight"], 1)
            })
            
    if not rows:
        return pd.DataFrame(columns=["Fecha", "Participante", "Peso (kg)", "Peso Inicial", "Objetivo (kg)", "Kilos Bajados"])
        
    df = pd.DataFrame(rows)
    df["Fecha_dt"] = pd.to_datetime(df["Fecha"])
    df = df.sort_values(by=["Fecha_dt", "Participante"]).reset_index(drop=True)
    return df


def export_data_csv() -> str:
    """Exporta todos los registros a formato CSV."""
    df = get_all_weights_dataframe()
    if df.empty:
        return "Fecha,Participante,Peso,Peso_Inicial,Objetivo\n"
    export_df = df[["Fecha", "Participante", "Peso (kg)", "Peso Inicial", "Objetivo (kg)"]]
    return export_df.to_csv(index=False, encoding="utf-8")
