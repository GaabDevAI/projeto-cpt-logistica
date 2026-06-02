from __future__ import annotations

from pathlib import Path

import pandas as pd


MAX_CSV_ROWS = 10_000
MAX_TEXT_LENGTH = 300
CSV_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


class SecurityError(ValueError):
    pass


def safe_project_path(project_root: Path, relative_path: str) -> Path:
    root = project_root.resolve()
    target = (root / relative_path).resolve()
    if root != target and root not in target.parents:
        raise SecurityError("Caminho fora da pasta do projeto bloqueado.")
    return target


def validate_required_columns(df: pd.DataFrame, required_columns: set[str]) -> None:
    missing = sorted(required_columns.difference(df.columns))
    if missing:
        raise SecurityError(
            "CSV invalido. Colunas obrigatorias ausentes: " + ", ".join(missing)
        )


def validate_row_limit(df: pd.DataFrame, max_rows: int = MAX_CSV_ROWS) -> None:
    if len(df) > max_rows:
        raise SecurityError(
            f"CSV bloqueado por seguranca: {len(df)} linhas excedem o limite de {max_rows}."
        )


def clamp_text(value: object, max_length: int = MAX_TEXT_LENGTH) -> object:
    if not isinstance(value, str):
        return value
    return value[:max_length]


def escape_spreadsheet_formula(value: object) -> object:
    if not isinstance(value, str):
        return value
    stripped = value.lstrip()
    if stripped.startswith(CSV_FORMULA_PREFIXES):
        return "'" + value
    return value


def sanitize_output_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    safe_df = df.copy()
    for column in safe_df.select_dtypes(include=["object", "string"]).columns:
        safe_df[column] = safe_df[column].map(clamp_text).map(escape_spreadsheet_formula)
    return safe_df
