from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.security import SecurityError, validate_required_columns, validate_row_limit


REQUIRED_COLUMNS = {
    "LH Trip Number",
    "LH Trip Name",
    "Station Number",
    "Station Name",
    "Vehicle Plate Number",
    "Driver",
    "Schedule Arrival Time",
    "Schedule Departure Time",
    "Outbound(order)",
    "Outbound(weight)(KG)",
    "On Time Indicator ",
    "CPT Type",
}


@dataclass(frozen=True)
class ShiftDefinition:
    name: str
    start_minute: int
    end_minute: int


SHIFT_DEFINITIONS = (
    ShiftDefinition("T1", 5 * 60 + 20, 13 * 60 + 40),
    ShiftDefinition("T2", 13 * 60 + 20, 21 * 60 + 40),
    ShiftDefinition("T3", 22 * 60, 5 * 60 + 40),
)


def parse_datetime(series: pd.Series | None, index: pd.Index | None = None) -> pd.Series:
    if series is None:
        return pd.Series(pd.NaT, index=index, dtype="datetime64[ns]")
    return pd.to_datetime(series, errors="coerce", dayfirst=True)


def minute_of_day(value: pd.Timestamp) -> int | None:
    if pd.isna(value):
        return None
    return int(value.hour * 60 + value.minute)


def is_inside_shift(minute: int, shift: ShiftDefinition) -> bool:
    if shift.start_minute <= shift.end_minute:
        return shift.start_minute <= minute <= shift.end_minute
    return minute >= shift.start_minute or minute <= shift.end_minute


def matching_shifts(value: pd.Timestamp) -> list[str]:
    minute = minute_of_day(value)
    if minute is None:
        return []
    return [
        shift.name
        for shift in SHIFT_DEFINITIONS
        if is_inside_shift(minute, shift)
    ]


def shift_window(value: pd.Timestamp) -> str:
    shifts = matching_shifts(value)
    return " / ".join(shifts) if shifts else "Fora do turno"


def primary_shift(value: pd.Timestamp) -> str:
    shifts = matching_shifts(value)
    if not shifts:
        return "Fora do turno"
    if "T1" in shifts and "T3" in shifts:
        return "T1"
    if "T1" in shifts and "T2" in shifts:
        return "T2"
    return shifts[0]


def numeric_column(df: pd.DataFrame, column: str, default: float = 0) -> pd.Series:
    if column not in df.columns:
        return pd.Series(default, index=df.index)
    return pd.to_numeric(df[column], errors="coerce").fillna(default)


def text_column(row: pd.Series, column: str, default: str = "") -> str:
    value = row.get(column, default)
    if pd.isna(value):
        return default
    return str(value)


def consolidate_trips(raw_df: pd.DataFrame) -> pd.DataFrame:
    validate_row_limit(raw_df)
    validate_required_columns(raw_df, REQUIRED_COLUMNS)

    df = raw_df.copy()
    df["Station Number"] = numeric_column(df, "Station Number")
    df["Schedule Departure Time"] = parse_datetime(df["Schedule Departure Time"])
    df["Actual Departure Time"] = parse_datetime(
        df.get("Actual Departure Time"),
        index=df.index,
    )
    df["Schedule Arrival Time"] = parse_datetime(df["Schedule Arrival Time"])
    df["Actual Arrival Time"] = parse_datetime(
        df.get("Actual Arrival Time"),
        index=df.index,
    )
    df["Outbound(order)"] = numeric_column(df, "Outbound(order)")
    df["Outbound(weight)(KG)"] = numeric_column(df, "Outbound(weight)(KG)")

    records: list[dict[str, object]] = []

    for trip_id, group in df.groupby("LH Trip Number", dropna=False):
        ordered = group.sort_values("Station Number")
        origin = ordered.iloc[0]
        destination = ordered.iloc[-1]

        departure = origin["Schedule Departure Time"]
        if pd.isna(departure):
            departure = origin["Actual Departure Time"]

        if pd.isna(departure):
            raise SecurityError(f"Viagem sem horario de saida valido: {trip_id}")

        arrival = destination["Schedule Arrival Time"]
        plate = text_column(origin, "Vehicle Plate Number")
        vehicle_count = max(1, len([item for item in plate.split(",") if item.strip()]))

        records.append(
            {
                "Viagem": trip_id,
                "Nome Viagem": text_column(origin, "LH Trip Name"),
                "Data Saida": departure.date() if not pd.isna(departure) else None,
                "Hora Saida": departure.strftime("%H:%M") if not pd.isna(departure) else "",
                "Saida Prevista": departure,
                "Turno": primary_shift(departure),
                "Janela Turno": shift_window(departure),
                "Placa": plate,
                "Qtd Veiculos": vehicle_count,
                "Motorista": text_column(origin, "Driver"),
                "Origem": text_column(origin, "Station Name"),
                "Destino": text_column(destination, "Station Name"),
                "Chegada Prevista": arrival,
                "Lead Time h": round((arrival - departure).total_seconds() / 3600, 1)
                if not pd.isna(arrival) and not pd.isna(departure)
                else None,
                "Pedidos": float(origin["Outbound(order)"]),
                "Peso KG": float(origin["Outbound(weight)(KG)"]),
                "CPT": text_column(destination, "CPT Type")
                or text_column(origin, "CPT Type"),
                "Status": text_column(origin, "On Time Indicator ").strip(),
            }
        )

    return pd.DataFrame.from_records(records)
