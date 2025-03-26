import os
import json

def save_project_info(project_data, json_path="data/projects.json"):
    projects = []

    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                projects = json.load(f)
            except json.JSONDecodeError:
                projects = []

    # 同名プロジェクトがあれば上書き
    projects = [p for p in projects if p["filename"] != project_data["filename"]]
    projects.append(project_data)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)

def load_projects(json_path="data/projects.json"):
    if not os.path.exists(json_path):
        return []

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def delete_project(filename, json_path="data/projects.json"):
    if not os.path.exists(json_path):
        return

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            projects = json.load(f)
        except json.JSONDecodeError:
            return

    projects = [p for p in projects if p["filename"] != filename]

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
