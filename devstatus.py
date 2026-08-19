#!/usr/bin/env python3
"""
☕ DevStatus — 程序员每日状态报告
每天生成一份你的精神状态报告
"""

import sys
import random
import hashlib
import argparse
from datetime import datetime, timezone

STATES = [
    ("🟢", "满血复活", "你的大脑 CPU 占用仅 5%，能跑任何复杂任务，趁今天改那个三个月没人敢碰的模块"),
    ("🟡", "亚健康",   "今天你的大脑内存约 3.2GB / 8GB， 能跑些轻量任务，别碰复杂逻辑"),
    ("🟠", "濒临崩溃", "你的状态线已经闪烁红灯了 每写一行代码都像在拆炸弹"),
                    ("🔴", "已宕机",   "建议今天就别写代码了，去看几集番吧 代码不是人写的是神写的但你不是神"),
    ("💀", "已超度",   "你看起来像是一周没睡觉的样子 键盘上可能有脸印 考虑休假"),
]

COFFEE = [
    (0, "☕", "你选择了茶，你是异端"),
    (1, "☕", "一杯续命，及格"),
    (2, "☕☕", "两杯起步，正常操作"),
    (3, "☕☕☕", "三杯还在路上，你是战士"),
    (5, "☕☕☕☕☕", "五杯了，你知道咖啡是有上限的吗"),
    (8, "☕☕☕☕☕☕☕☕", "八杯，说明你今天有 Slayer 级别的故事"),
]

ACTIVITIES_OK = [
    "写单元测试（反正你不会写）",
    "开会讨论需求（不用写代码）",
    "整理桌面图标（假装在整理项目）",
    "看技术博客（摸鱼的高级形式）",
    "写设计文档（拖延编码的合法手段）",
    "review 别人的代码（心情好就用放大镜）",
    "清理 git 分支（至少看起来很忙）",
    "配置环境（一天就过去了）",
]

ACTIVITIES_NO = [
    "重构（你会在第三层缩进时迷失）",
    "写正则表达式（你会陷入疯狂）",
    "处理 merge conflict（你会想离职）",
    "升级依赖版本（有一半概率炸）",
    "碰那段没人懂的代码（那是有原因的）",
    "在周五下午 deploy（老规矩）",
    "跟产品经理争论需求（你赢不了）",
    "优化数据库查询（你只是把慢查询变成了另一种慢）",
]

MOOD_EMOJIS = ["☀️", "🌤️", "⛅", "☁️", "🌧️", "⛈️", "🌪️"]
MOOD_TEXTS = [
    "今天感觉不错，也许能写点好代码",
    "需求又变了，但我已经波澜不惊了",
    "我想回家",
    "为什么又是我来修这个 bug",
    "代码能跑就行，我不挑了",
    "今天的我比昨天多了 3 个 TODO",
    "我已经不记得上次写测试是什么时候了",
    "bug 是特性，feature 是 bug，人生就是这样",
    "别问我，问就是 StackOverflow 说的",
    "今天 Product 来过三次，我感觉不太对",
]

KNOWLEDGE_SOURCES = [
    "StackOverflow 抄的 + ChatGPT 问的",
    "ChatGPT 说的就当他是对的",
    "官方文档 (英文的, 你假装看懂了)",
    "问了同事, 同事说我也不知道",
    "看的 B 站教程 (没有弹幕那种)",
    "GitHub 找的, 但你不知道为什么能跑",
    "灵感来自上个项目的一个函数",
    "纯凭直觉, 跟玄学差不多",
]

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
WEEKDAY_MOOD = {
    0: "又是周一，为什么没有周三的心情",
    1: "已经周二了，周三还远着呢",
    4: "周五了！但是下午三点之前不许高调",
    5: "周六为什么也没有 Electron 桌面通知",
    6: "周日晚上最不适合写代码",
}

CAFFEINE_BARS = ["░░░░░░░░░░", "█░░░░░░░░░", "██░░░░░░░░", "███░░░░░░░",
                 "████░░░░░░", "█████░░░░░", "██████░░░░", "███████░░░",
                 "████████░░", "█████████░", "██████████"]

TOMORROW = [
    ("☀️", "据说明天需求就确定了"),
    ("🌤️", "据说明天没有会议"),
    ("☁️", "据说明天 Product 要来一次新的灵感的雪花"),
    ("🌧️", "据说还有新需求要来"),
    ("🌧️", "带雨伞, 也带耳机"),
    ("⛈️", "据说明天要紧急修复某个生产环境的 issue"),
    ("🌪️", "据说明天要把所有 requirement 换成新的"),
]


def patentRound(num, dig=1):
    return round(num, dig)


def gen_report(name, seed):
    if seed:
        random.seed(seed)
    else:
        today = datetime.now().strftime("%Y%m%d")
        seed_int = hash(f"{name}{today}") & 0xFFFFFFFF
        random.seed(seed_int)
    
    now = datetime.now()
    weekday = now.weekday()
    date_str = now.strftime("%Y-%m-%d")
    weekday_cn = WEEKDAYS[weekday]
    
    state = random.choice(STATES)
    state_emoji, state_name, state_desc = state
    
    coffee_idx = random.choice(range(len(COFFEE)))
    coffee_count, coffee_emoji, coffee_note = COFFEE[coffee_idx]
    
    caffeine_level = min(coffee_count, 10)
    caffeine_bar = CAFFEINE_BARS[caffeine_level]
    
    tabs_ide = random.randint(8, 35)
    tabs_so = random.randint(3, 25)
    terminals = random.randint(1, 15)
    
    effective_lines = random.randint(15, 300)
    new_bugs = random.randint(0, 20)
    new_todos = random.randint(0, 30)
    
    source = random.choice(KNOWLEDGE_SOURCES)
    
    mood_idx = random.randint(0, len(MOOD_EMOJIS) - 1)
    mood_emoji = MOOD_EMOJIS[mood_idx]
    mood_text = random.choice(MOOD_TEXTS)
    
    ok_acts = random.sample(ACTIVITIES_OK, 3)
    no_acts = random.sample(ACTIVITIES_NO, 3)
    
    tm = random.choice(TOMORROW)
    tm_emoji, tm_desc = tm
    
    weekday_mood = WEEKDAY_MOOD.get(weekday, "普普通通的一天")
    
    display_name = name if name and name != "Anonymous Developer" else "Anonymous Developer"
    
    sep = "═" * 51
    
    report = f"""
{sep}
  ☕ DevStatus — 程序员每日状态报告
  📅 {date_str} ({weekday_cn})
  👤 {display_name}
{sep}

精神状态: {state_emoji} {state_name}
  {state_desc}

知识摄入: 📚
  今天读完的文档: {random.randint(0, 5)} 页
  今天 Google 的次数: {random.randint(10, 99)}
  今天的知识来源: {source}

环境状况:
  IDE 打开的标签页: {tabs_ide}
  StackOverflow 打开的页数: {tabs_so}
  终端窗口数: {terminals}
  咖啡消耗: {coffee_count} 杯 {coffee_emoji} ({coffee_note})

代码产出预测:
  能写出的有效代码行数: {effective_lines} 行
  能引入的新 bug 数: {new_bugs} 个
  能产生的 TODO 数: {new_todos} 条

今日建议:
  ✅ 适合: {ok_acts[0]}
  ✅ 适合: {ok_acts[1]}
  ✅ 适合: {ok_acts[2]}
  ❌ 不适合: {no_acts[0]}
  ❌ 不适合: {no_acts[1]}
  ❌ 不适合: {no_acts[2]}

心情指数: {mood_emoji}
  {mood_text}
  咖啡因浓度: {caffeine_bar} {caffeine_level * 10}%

{weekday_mood}

明天预测: {tm_emoji}→{tm_emoji}
  {tm_desc}

{sep}
"""
    print(report)


def main():
    parser = argparse.ArgumentParser(description="☕ DevStatus — 程序员每日状态报告")
    parser.add_argument("--name", type=str, default="Anonymous Developer", help="你的名字")
    parser.add_argument("--seed", type=int, default=None, help="随机种子（同一天同一种子出同样的报告）")
    args = parser.parse_args()
    gen_report(args.name, args.seed)


if __name__ == "__main__":
    main()
