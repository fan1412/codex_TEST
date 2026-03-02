# TODO

## 已完成
- [x] 创建 MariaDB 连接工具（`db_utils.py`），默认连接 `172.18.1.65:3306`。
- [x] 支持访问 `ondemand_detail` 与 `set_top_box_boot_status` 两张表，并提供通用查询方法。
- [x] 提供根据表结构动态生成 `select` 函数的脚本（`generate_selects.py`）。
- [x] 新增剧集名称解析工具（`episode_name_parser.py`）。
- [x] 添加解析工具测试用例（`tests/test_episode_name_parser.py`）。

## 待办
- [ ] 在拿到准确数据库名后，补充 `DBConfig.database` 的默认值。
- [ ] 连接可达环境后执行 `python generate_selects.py` 生成并提交 `generated_selects.py`。
- [ ] 按后续需求继续追加任务。

## 备注
- 请把新任务直接追加到「待办」列表，完成后移动到「已完成」。
