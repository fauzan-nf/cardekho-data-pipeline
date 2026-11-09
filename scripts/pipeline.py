"""Wrapper fungsi untuk dipanggil DAG Airflow.

Setiap fungsi memanggil main() dari skrip tahap terkait, sehingga logika
pipeline tetap satu sumber (scripts/extract.py, transform.py, dst).
"""
from scripts import extract, transform, load, analytics


def run_extract() -> None:
    extract.main()


def run_transform() -> None:
    transform.main()


def run_load() -> None:
    load.main()


def run_analytics() -> None:
    analytics.main()
