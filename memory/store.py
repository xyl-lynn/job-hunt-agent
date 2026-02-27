import json
import os
from datetime import datetime
from typing import Optional

STORE_PATH = "memory/applications.json"


def load_applications() -> list:
    if not os.path.exists(STORE_PATH):
        return []
    with open(STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_application(company: str, position: str, jd_summary: str, remind_days: int = 7) -> dict:
    applications = load_applications()
    record = {
        "id": len(applications) + 1,
        "company": company,
        "position": position,
        "jd_summary": jd_summary,
        "status": "已投递",
        "applied_date": datetime.now().strftime("%Y-%m-%d"),
        "last_update": datetime.now().strftime("%Y-%m-%d"),
        "remind_days": remind_days,
        "notes": ""
    }
    applications.append(record)
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(applications, f, ensure_ascii=False, indent=2)
    return record


def update_status(record_id: int, status: str, notes: str = "") -> Optional[dict]:
    applications = load_applications()
    for app in applications:
        if app["id"] == record_id:
            app["status"] = status
            if notes:
                app["notes"] = notes
            app["last_update"] = datetime.now().strftime("%Y-%m-%d")
            with open(STORE_PATH, "w", encoding="utf-8") as f:
                json.dump(applications, f, ensure_ascii=False, indent=2)
            return app
    return None


def delete_application(record_id: int):
    applications = load_applications()
    applications = [a for a in applications if a["id"] != record_id]
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(applications, f, ensure_ascii=False, indent=2)


def edit_application(record_id: int, company: str, position: str) -> Optional[dict]:
    applications = load_applications()
    for app in applications:
        if app["id"] == record_id:
            app["company"] = company
            app["position"] = position
            app["last_update"] = datetime.now().strftime("%Y-%m-%d")
            with open(STORE_PATH, "w", encoding="utf-8") as f:
                json.dump(applications, f, ensure_ascii=False, indent=2)
            return app
    return None


def check_followups() -> list:
    applications = load_applications()
    today = datetime.now()
    need_followup = []
    final_statuses = ("已拒绝", "已offer", "已放弃")
    for app in applications:
        if app["status"] in final_statuses:
            continue
        last = datetime.strptime(app["last_update"], "%Y-%m-%d")
        days_passed = (today - last).days
        remind_days = app.get("remind_days", 7)
        if days_passed >= remind_days:
            app["days_passed"] = days_passed
            need_followup.append(app)
    return need_followup


def list_all() -> list:
    return load_applications()