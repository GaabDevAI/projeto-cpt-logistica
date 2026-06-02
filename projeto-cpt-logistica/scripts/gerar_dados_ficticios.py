from __future__ import annotations

import csv
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.security import safe_project_path


OUTPUT_PATH = safe_project_path(PROJECT_ROOT, "data/dados_ficticios.csv")
RANDOM_SEED = 42

DESTINATIONS = [
    "Hub_SP_Vila Norte",
    "Hub_SP_Parque Sul",
    "Hub_MG_Centro Oeste",
    "Hub_RJ_Litoral Norte",
    "Hub_SP_Campo Verde",
    "Hub_SP_Metropolitano",
    "Hub_PR_Alto Vale",
    "Hub_SP_Serra Azul",
    "Hub_GO_Planalto",
    "Hub_SC_Baia Sul",
    "Hub_BA_Avenida Mar",
    "Hub_SP_Zona Leste",
    "Hub_SP_Rota Norte",
    "Hub_MG_Sul Minas",
    "Hub_RJ_Serra Azul",
    "Hub_SP_Cidade Nova",
]

CPT_TYPES = ["AM", "PM1", "PM2"]
STATUSES = ["On-Time Arrival", "Waiting", "Delayed Departure"]


def format_dt(value: datetime | None) -> str:
    return value.strftime("%d/%m/%Y %H:%M") if value else ""


def make_plate(index: int) -> str:
    return f"VEICULO_DEMO_{index:03d}"


def main() -> None:
    random.seed(RANDOM_SEED)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    headers = [
        "LH Trip Number",
        "LH Trip Name",
        "Station Number",
        "Station Name",
        "Vehicle Plate Number",
        "Driver",
        "Schedule Arrival Time",
        "Actual Arrival Time",
        "Schedule Departure Time",
        "Actual Departure Time",
        "Outbound(order)",
        "Outbound(weight)(KG)",
        "On Time Indicator ",
        "CPT Type",
        "Occupancy Rate",
    ]

    start = datetime(2026, 6, 2, 5, 30)
    rows: list[dict[str, object]] = []

    for i in range(1, 49):
        departure = start + timedelta(minutes=random.choice([0, 30, 60, 90, 150]) * i)
        destination = random.choice(DESTINATIONS)
        cpt = random.choice(CPT_TYPES)
        lead_hours = random.choice([2, 3, 4, 6, 8, 10, 14, 17])
        arrival_origin = departure - timedelta(minutes=random.choice([20, 30, 45, 60]))
        arrival_dest = departure + timedelta(hours=lead_hours)
        trip_id = f"TRP-20260602-{i:03d}"
        vehicle_count = random.choice([1, 1, 1, 2])
        plates = ",".join(make_plate(i * 2 + n) for n in range(vehicle_count))
        driver = f"Motorista Demo {i:03d}"
        orders = random.randint(60, 340)
        weight = round(random.uniform(800, 4200), 1)
        status = random.choice(STATUSES)
        occupancy = round(random.uniform(0.55, 0.96), 2)

        rows.append(
            {
                "LH Trip Number": trip_id,
                "LH Trip Name": f"20260602_DEMO_{i:03d}_{cpt}",
                "Station Number": 1,
                "Station Name": "CD_SP_Alpha",
                "Vehicle Plate Number": plates,
                "Driver": driver,
                "Schedule Arrival Time": format_dt(arrival_origin),
                "Actual Arrival Time": format_dt(
                    arrival_origin + timedelta(minutes=random.randint(-5, 8))
                ),
                "Schedule Departure Time": format_dt(departure),
                "Actual Departure Time": "",
                "Outbound(order)": orders,
                "Outbound(weight)(KG)": weight,
                "On Time Indicator ": status,
                "CPT Type": cpt,
                "Occupancy Rate": occupancy,
            }
        )
        rows.append(
            {
                "LH Trip Number": trip_id,
                "LH Trip Name": f"20260602_DEMO_{i:03d}_{cpt}",
                "Station Number": 2,
                "Station Name": destination,
                "Vehicle Plate Number": plates,
                "Driver": driver,
                "Schedule Arrival Time": format_dt(arrival_dest),
                "Actual Arrival Time": "",
                "Schedule Departure Time": "",
                "Actual Departure Time": "",
                "Outbound(order)": 0,
                "Outbound(weight)(KG)": 0,
                "On Time Indicator ": "",
                "CPT Type": cpt,
                "Occupancy Rate": 0,
            }
        )

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Arquivo ficticio gerado em: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
