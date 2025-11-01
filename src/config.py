"""Configuration management for Samarth application."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Streamlit secrets fallback (for cloud deployment)
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        DATA_GOV_API_KEY = st.secrets.get("DATA_GOV_API_KEY", DATA_GOV_API_KEY)
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", GEMINI_API_KEY)
except:
    pass

# Database Configuration
DB_PATH = os.getenv("DB_PATH", "./data/samarth.duckdb")

# Cache Configuration
CACHE_DIR = Path(os.getenv("CACHE_DIR", "./cache"))
PARQUET_CACHE_DIR = Path(os.getenv("PARQUET_CACHE_DIR", "./cache/parquet"))

# Data.gov.in API Configuration
DATA_GOV_BASE_URL = "https://api.data.gov.in/resource"

# Ensure directories exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)
PARQUET_CACHE_DIR.mkdir(parents=True, exist_ok=True)
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
