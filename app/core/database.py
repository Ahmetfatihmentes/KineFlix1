"""
SQLite veritabanı adresi — proje ana dizininde kineflix.db.

Dökümanlardaki `sqlite:///./kineflix.db` ifadesi, çalışma dizininden bağımsız
olarak her zaman proje kökündeki dosyaya çözülür.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
# Proje kökü: .../kineflix/kineflix.db (mutlak yol, thread-safe)
DATABASE_URL = f"sqlite:///{(PROJECT_ROOT / 'kineflix.db').resolve().as_posix()}"
