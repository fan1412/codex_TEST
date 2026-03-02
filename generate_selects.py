"""Generate select helper functions for required tables."""
from __future__ import annotations

import os
from pathlib import Path

from db_utils import DBConfig, MariaDBClient, SelectFunctionGenerator

TARGET_TABLES = ["ondemand_detail", "set_top_box_boot_status"]
OUTPUT_FILE = Path(__file__).with_name("generated_selects.py")


def main() -> None:
    schema_name = os.getenv("MARIADB_SCHEMA", "").strip()
    if not schema_name:
        raise ValueError("请先设置环境变量 MARIADB_SCHEMA，再执行生成脚本。")

    config = DBConfig(database=schema_name)
    client = MariaDBClient(config)
    generator = SelectFunctionGenerator(client)
    content = generator.generate(schema_name=schema_name, table_names=TARGET_TABLES)
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
