# テトリスゲーム Tetris Game

アプリの配布練習のために、Codexに頼みPython(Tkinter)で作成したテトリスゲームです。
Releasesからzipを解凍、main.exeダブルクリックで遊べます、多分。
<br>
Dr.Stone劇中セリフの「簡単な落ち物パズルは1行で作れる」を信じて作りました。全く1行では収まりませんでした。

<br>

A Python implementation of the classic Tetris game using tkinter.

## 概要 Features

- テトリスの基本プレイ
- コンフィグ(次のブロック表示数の変更・落下速度の設定・回転方向の設定・日本語⇔英語の切り替え)
- ランキング（スコア保存 tetris_rankings.jsonに格納）
- 遊び方説明
- 一時停止機能

<br>

- Classic Tetris gameplay
- Configurable settings (preview count, fall speed, rotation direction, Japanese/English language switching)
- Ranking/Score system(Save tetris_rankings.json)
- Menu system with How To Play guide
- Pause functionality

## 動作環境 Requirements

- Python 3.7以上
- tkinter（通常はPythonに含まれています）

<br>

- Python 3.7 or higher
- tkinter (included with Python standard library)

## 導入 Installation

```bash
python main.py
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
├── texts.py             # 画面表示テキスト
├── ranking.py           # ランキング処理
├── tetris_rankings.json # スコア保存
├── setup.py             # パッケージ設定
├── requirements.txt     # 必要ライブラリ
└── README.md            # この説明書
```
<br>

```txt
tetris/
├── main.py              # Entry point
├── game.py              # Main game logic
├── piece.py             # Tetromino piece definitions
├── constants.py         # Game constants and colors
├── texts.py             # UI text
├── ranking.py           # Score/ranking system
├── tetris_rankings.json # Saved rankings data
├── setup.py             # Package configuration
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## ライセンス License

MIT License - see LICENSE file for details

## 作成者 Author

m1410128
