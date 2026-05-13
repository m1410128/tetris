# tetris/texts.py
# 画面に表示する文章をまとめたファイルです。
# キー名は変更せず、右側の文字だけ編集すると安全です。

LANGUAGE_NAMES = {
    "en": "English",
    "ja": "日本語",
}

TEXTS_EN = {
    "window_title": "Tetris",
    "title": "TETRIS",
    "menu": {
        "play": "Play Start",
        "config": "Config",
        "help": "How To Play",
        "ranking": "Ranking",
        "exit": "Exit",
    },
    "config": {
        "title": "CONFIG",
        "language": "Language",
        "preview_count": "Preview Count",
        "fall_speed": "Fall Speed",
        "rotate_direction": "Space Rotate",
        "hold_key": "Reserve Key",
        "back": "Back",
        "clockwise": "Clockwise",
        "counter": "Counter",
        "footer": "Left/Right or Enter: Change    Esc: Back",
    },
    "speed_names": {
        900: "eazy",
        650: "normal",
        400: "hard",
        220: "very hard",
    },
    "help": {
        "title": "HOW TO PLAY",
        "lines": [
            "Left / Right : Move",
            "Down         : Soft drop (+1)",
            "Up           : Hard drop (+2 per cell)",
            "Space        : Rotate",
            "{hold_key:<12} : Reserve / Swap",
            "Enter        : Pause",
            "",
            "Fill a horizontal line to clear it.",
            "Cross the top deadline and the game ends.",
            "",
            "Enter / Esc  : Back",
        ],
    },
    "ranking": {
        "title": "RANKING",
        "empty": "No records yet",
        "footer": "Enter / Esc: Back",
    },
    "pause": {
        "title": "PAUSE",
        "resume": "Resume",
        "retire": "Retire",
    },
    "retire": {
        "title": "Retire this game?",
        "message": "This result will not be recorded.",
        "no": "No",
        "yes": "Yes",
    },
    "game_over": {
        "title": "GAME OVER",
        "score": "Score: {score}",
        "footer": "Enter: Menu",
    },
    "side_panel": {
        "hold": "HOLD",
        "next": "NEXT",
        "score": "SCORE\n{score}",
        "lines": "LINES\n{lines}",
    },
}

TEXTS_JA = {
    "window_title": "テトリス",
    "title": "テトリス",
    "menu": {
        "play": "ゲーム開始",
        "config": "設定",
        "help": "遊び方",
        "ranking": "ランキング",
        "exit": "終了",
    },
    "config": {
        "title": "設定",
        "language": "言語",
        "preview_count": "次ブロック表示数",
        "fall_speed": "落下速度",
        "rotate_direction": "回転方向",
        "hold_key": "ホールドキー",
        "back": "戻る",
        "clockwise": "時計回り",
        "counter": "反時計回り",
        "footer": "左右キーまたはEnter: 変更    Esc: 戻る",
    },
    "speed_names": {
        900: "おそい",
        650: "ふつう",
        400: "ややはやい",
        220: "かなりはやい",
    },
    "help": {
        "title": "遊び方",
        "lines": [
            "Left / Right : 左右に移動",
            "Down         : 1マス落下 (+1)",
            "Up           : 一気に落下 (+2/マス)",
            "Space        : 回転",
            "{hold_key:<12} : ホールド / 交換",
            "Enter        : 一時停止",
            "",
            "横一列をそろえるとラインが消えます。",
            "上の赤いラインを超えるとゲームオーバーです。",
            "",
            "Enter / Esc  : 戻る",
        ],
    },
    "ranking": {
        "title": "ランキング",
        "empty": "まだ記録がありません",
        "footer": "Enter / Esc: 戻る",
    },
    "pause": {
        "title": "一時停止",
        "resume": "再開",
        "retire": "リタイア",
    },
    "retire": {
        "title": "リタイアしますか？",
        "message": "このスコアは記録されません。",
        "no": "いいえ",
        "yes": "はい",
    },
    "game_over": {
        "title": "ゲームオーバー",
        "score": "スコア: {score}",
        "footer": "Enter: メニューへ",
    },
    "side_panel": {
        "hold": "ホールド",
        "next": "次",
        "score": "スコア\n{score}",
        "lines": "ライン\n{lines}",
    },
}

TEXTS_BY_LANGUAGE = {
    "en": TEXTS_EN,
    "ja": TEXTS_JA,
}
