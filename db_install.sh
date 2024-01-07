#!/bin/bash
sqlite3 moneyflow_manager.db < schema.sql
python3 db_fill.py
