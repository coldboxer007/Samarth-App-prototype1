"""Script to verify the Samarth setup is correct."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
from dotenv import load_dotenv


def check_environment():
    """Check environment variables."""
    print("🔍 Checking environment variables...")

    load_dotenv()

    checks = {
        "DATA_GOV_API_KEY": os.getenv("DATA_GOV_API_KEY", ""),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", "")
    }

    all_good = True
    for key, value in checks.items():
        if value and value != "your_api_key_here" and value != "your_anthropic_api_key_here":
            print(f"  ✓ {key} is set")
        else:
            print(f"  ✗ {key} is NOT set or still has default value")
            all_good = False

    return all_good


def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")

    required_packages = [
        "streamlit",
        "duckdb",
        "pandas",
        "requests",
        "anthropic",
        "openpyxl",
        "pyarrow",
        "tenacity",
        "pydantic"
    ]

    all_good = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package} is installed")
        except ImportError:
            print(f"  ✗ {package} is NOT installed")
            all_good = False

    return all_good


def check_directories():
    """Check if required directories exist."""
    print("\n📁 Checking directories...")

    required_dirs = [
        Path("data"),
        Path("cache"),
        Path("cache/parquet"),
        Path("src"),
        Path("scripts")
    ]

    all_good = True
    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"  ✓ {dir_path} exists")
        else:
            print(f"  ✗ {dir_path} does NOT exist")
            all_good = False

    return all_good


def check_imports():
    """Check if core modules can be imported."""
    print("\n🔧 Checking core modules...")

    modules_to_check = [
        ("src.config", "Configuration"),
        ("src.catalog", "Catalog Layer"),
        ("src.adapters", "Adapter Layer"),
        ("src.database", "Database Layer"),
        ("src.query", "Query Layer"),
        ("src.llm", "LLM Layer"),
        ("src.app", "Application Layer")
    ]

    all_good = True
    for module_name, description in modules_to_check:
        try:
            __import__(module_name)
            print(f"  ✓ {description} ({module_name})")
        except Exception as e:
            print(f"  ✗ {description} ({module_name}): {str(e)[:50]}")
            all_good = False

    return all_good


def check_database():
    """Check if database can be initialized."""
    print("\n💾 Checking database...")

    try:
        from src.database import CanonicalDatabase
        db = CanonicalDatabase()
        print(f"  ✓ Database initialized at {db.db_path}")
        return True
    except Exception as e:
        print(f"  ✗ Database initialization failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Samarth Setup Verification")
    print("=" * 60)
    print()

    checks = [
        ("Environment Variables", check_environment),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
        ("Module Imports", check_imports),
        ("Database", check_database)
    ]

    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)

    if all_passed:
        print("✅ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Update scripts/ingest_sample_data.py with real resource IDs")
        print("2. Run: python scripts/test_system.py")
        print("3. Or run: streamlit run streamlit_app.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Missing dependencies: pip install -r requirements.txt")
        print("- Missing API keys: Copy .env.example to .env and add your keys")
        print("- Missing directories: They should be created automatically")

    print("=" * 60)


if __name__ == "__main__":
    main()
