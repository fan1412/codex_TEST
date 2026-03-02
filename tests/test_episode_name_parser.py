from episode_name_parser import parse_series_name


def test_parse_series_name_cases():
    assert parse_series_name("汪汪队立大功 第十一季_6") == "汪汪队立大功"
    assert parse_series_name("太平年_25") == "太平年"
    assert parse_series_name("布莱泽奥特曼（普通话版）_25") == "布莱泽奥特曼"
    assert parse_series_name("啦咘啦哆警长之小哆哆守护计划_5") == "啦咘啦哆警长之小哆哆守护计划"
