# ==========================================
# Buddy AI - System Diagnostics
# ==========================================

import importlib
import os
import socket
import shutil


# ==========================================
# MODULE CHECK
# ==========================================

def check_module(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except Exception as e:
        print(f"[Diagnostics] {module_name} Error:", repr(e))
        return False


# ==========================================
# INTERNET CHECK
# ==========================================

def check_internet():
    try:
        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )
        return True
    except Exception:
        return False


# ==========================================
# STORAGE CHECK
# ==========================================

def check_storage():
    try:
        total, used, free = shutil.disk_usage(
            os.path.abspath(".")
        )

        free_gb = free / (1024 ** 3)

        return round(free_gb, 1)

    except Exception:
        return None


# ==========================================
# MAIN DIAGNOSTIC
# ==========================================

def run_diagnostics():

    results = {}

    # --------------------------------------
    # Core Modules
    # --------------------------------------

    results["Voice"] = check_module("voice")

    results["AI Brain"] = check_module(
        "modules.ai"
    )

    results["AI Manager"] = check_module(
        "modules.ai_manager"
    )

    results["Memory"] = check_module(
        "modules.memory"
    )

    results["Router"] = check_module(
        "modules.router"
    )

    # --------------------------------------
    # Other Buddy Modules
    # --------------------------------------

    results["Notes"] = check_module(
        "modules.notes"
    )

    results["Reminders"] = check_module(
        "modules.reminder"
    )

    results["Weather"] = check_module(
        "modules.weather"
    )

    # --------------------------------------
    # System Module
    # --------------------------------------

    results["System Module"] = check_module(
        "plugins.system"
    )

    # --------------------------------------
    # Internet
    # --------------------------------------

    results["Internet"] = check_internet()

    # --------------------------------------
    # Storage
    # --------------------------------------

    free_storage = check_storage()

    # --------------------------------------
    # Overall Status
    # --------------------------------------

    failed = [
        name
        for name, status in results.items()
        if status is False
    ]

    if not failed:
        overall = "Healthy"
    elif len(failed) <= 2:
        overall = "Minor Issues"
    else:
        overall = "Needs Attention"

    return {
        "results": results,
        "free_storage_gb": free_storage,
        "failed": failed,
        "overall": overall
    }


# ==========================================
# FORMAT DIAGNOSTIC REPORT
# ==========================================

def format_diagnostic_report(data):

    lines = [
        "Buddy System Check.",
        ""
    ]

    for name, status in data["results"].items():

        if status is True:
            icon = "OK"

        elif status is False:
            icon = "ERROR"

        else:
            icon = "UNKNOWN"

        lines.append(
            f"{name}: {icon}"
        )

    lines.append("")

    if data["free_storage_gb"] is not None:

        lines.append(
            f"Free Storage: "
            f"{data['free_storage_gb']} GB"
        )

    lines.append(
        f"Overall Status: {data['overall']}"
    )

    if data["failed"]:

        lines.append("")
        lines.append(
            "Issues Found:"
        )

        for item in data["failed"]:

            lines.append(
                f"- {item}"
            )

    return "\n".join(lines)


# ==========================================
# SIMPLE COMMAND FUNCTION
# ==========================================

def diagnose():

    data = run_diagnostics()

    return format_diagnostic_report(
        data
    )