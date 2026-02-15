"""Скрипт проверки установки всех зависимостей."""


def check_imports():
    """Проверяем, что все пакеты импортируются без ошибок."""
    packages = {}

    try:
        import fastapi
        packages["fastapi"] = fastapi.__version__
    except ImportError as e:
        packages["fastapi"] = f"ОШИБКА: {e}"

    try:
        import sqlalchemy
        packages["sqlalchemy"] = sqlalchemy.__version__
    except ImportError as e:
        packages["sqlalchemy"] = f"ОШИБКА: {e}"

    try:
        import alembic
        packages["alembic"] = alembic.__version__
    except ImportError as e:
        packages["alembic"] = f"ОШИБКА: {e}"

    try:
        import asyncpg
        packages["asyncpg"] = asyncpg.__version__
    except ImportError as e:
        packages["asyncpg"] = f"ОШИБКА: {e}"

    try:
        import pydantic
        packages["pydantic"] = pydantic.__version__
    except ImportError as e:
        packages["pydantic"] = f"ОШИБКА: {e}"

    try:
        import jose
        packages["python-jose"] = "OK"
    except ImportError as e:
        packages["python-jose"] = f"ОШИБКА: {e}"

    try:
        import passlib
        packages["passlib"] = "OK"
    except ImportError as e:
        packages["passlib"] = f"ОШИБКА: {e}"

    print("=" * 50)
    print("  ПРОВЕРКА УСТАНОВКИ ЗАВИСИМОСТЕЙ")
    print("=" * 50)

    all_ok = True
    for name, version in packages.items():
        status = "✅" if "ОШИБКА" not in str(version) else "❌"
        if "ОШИБКА" in str(version):
            all_ok = False
        print(f"  {status} {name:.<30} {version}")

    print("=" * 50)
    if all_ok:
        print("  ✅ Все зависимости установлены корректно!")
    else:
        print("  ❌ Есть проблемы. Переустанови пакеты.")
    print("=" * 50)


if __name__ == "__main__":
    check_imports()