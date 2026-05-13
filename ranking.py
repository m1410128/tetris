import json
from datetime import datetime
from pathlib import Path


RANKING_FILE = Path(__file__).with_name("tetris_rankings.json")


def load_rankings():
    # 保存済みランキングを読み込む
    try:
        with RANKING_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def save_rankings(rankings):
    # 上位5件だけランキングに保存
    with RANKING_FILE.open("w", encoding="utf-8") as file:
        json.dump(rankings[:5], file, ensure_ascii=False, indent=2)


def record_score(score):
    # 現在のスコアをランキングに追加
    rankings = load_rankings()
    rankings.append(
        {
            "score": score,
            "date": datetime.now().strftime("%Y/%m/%d"),
        }
    )
    rankings.sort(key=lambda row: row.get("score", 0), reverse=True)
    save_rankings(rankings)
