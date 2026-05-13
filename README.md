# テトリスゲーム Tetris Game

アプリ配布練習のために、Codexに頼みPython(Tkinter)で作成したテトリスゲームです。
Dr.Stone劇中セリフの「簡単な落ち物パズルは1行で作れる」を信じて作りました。全く1行では収まりませんでした。

A Python implementation of the classic Tetris game using tkinter.

## 概要 Features

- テトリスの基本プレイ
- (※未実装)次のブロック表示数の変更(コンフィグ)
- (※未実装)落下速度の設定
- (※未実装)回転方向の設定
- ランキング（スコア保存 tetris_ranking.jsonに格納）
- 遊び方説明
- 一時停止機能
- (※出来たらいいな) 日本語⇔英語の切り替えなど

- Classic Tetris gameplay
- (※Not yet)Configurable settings (preview count, fall speed, rotation direction)
- Ranking/Score system(Save tetris_ranking.json)
- Menu system with How To Play guide
- Pause functionality
- (※I'll try) Change language Japanese⇔English

## 動作環境 Requirements

- Python 3.7以上
- tkinter（通常はPythonに含まれています）

- Python 3.7 or higher
- tkinter (included with Python standard library)

## 導入 Installation

### Option 1: Direct Run

```bash
python main.py
```

### Option 2: Install as Package

```bash
pip install -e .
tetris
```

## Usage

Run the game:
```bash
python main.py
```

## ファイル構成 File Structure

```txt
tetris/
├── main.py              # 起動用
├── game.py              # ゲーム本体
├── piece.py             # テトロミノ定義
├── constants.py         # 定数・色設定
├── ranking.py           # ランキング処理
├── tetris_rankings.json # スコア保存
├── setup.py             # パッケージ設定
├── requirements.txt     # 必要ライブラリ
└── README.md            # この説明書
```

```
tetris/
├── main.py              # Entry point
├── game.py              # Main game logic
├── piece.py             # Tetromino piece definitions
├── constants.py         # Game constants and colors
├── ranking.py           # Score/ranking system
├── tetris_rankings.json # Saved rankings data
├── setup.py             # Package configuration
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## ライセンス License

よくわかっていない

MIT License - see LICENSE file for details

## 作成者 Author

わし m1410128
