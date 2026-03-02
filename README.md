# 项目说明

## 1) MariaDB 连接
默认使用以下连接参数（见 `db_utils.py`）：

- Host: `172.18.1.65`
- Port: `3306`
- User: `zxfc_admin`
- Password: `WGZXwgzx669992`

> 数据库名（schema）需要通过 `MARIADB_SCHEMA` 提供。

## 2) 访问表
目标表：

- `ondemand_detail`
- `set_top_box_boot_status`

`MariaDBClient` 提供：

- `select_all(table_name, limit=None)`
- `select_by_filters(table_name, filters)`

## 3) 根据表结构生成 select 函数
执行：

```bash
MARIADB_SCHEMA=你的库名 python generate_selects.py
```

生成文件：`generated_selects.py`（包含两张表的按字段筛选函数）。

## 4) 剧集名解析工具
文件：`episode_name_parser.py`

函数：`parse_series_name(episode_title: str) -> str`

示例：

- `汪汪队立大功 第十一季_6` -> `汪汪队立大功`
- `太平年_25` -> `太平年`
- `布莱泽奥特曼（普通话版）_25` -> `布莱泽奥特曼`
- `啦咘啦哆警长之小哆哆守护计划_5` -> `啦咘啦哆警长之小哆哆守护计划`

## 5) TODO 管理
见 `TODO.md`，后续可持续追加任务。
