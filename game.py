import random
import tkinter as tk

# try:
#     from .constants import CELL, COLORS, COLS, EMPTY, HEIGHT, ROWS, SHAPES, WIDTH, GAME_TITLE
#     from .piece import Tetromino
#     from .ranking import load_rankings, record_score
#     from .texts import LANGUAGE_NAMES, TEXTS_BY_LANGUAGE
# except ImportError:
from constants import CELL, COLORS, COLS, EMPTY, HEIGHT, ROWS, SHAPES, WIDTH, GAME_TITLE
from piece import Tetromino
from ranking import load_rankings, record_score
from texts import LANGUAGE_NAMES, TEXTS_BY_LANGUAGE


class TetrisGame:
    def __init__(self):
        # ウィンドウとゲーム状態を初期化
        self.root = tk.Tk()
        self.root.title(TEXTS_BY_LANGUAGE["en"]["window_title"])
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH,
            height=HEIGHT,
            bg="#151820",
            highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.on_key)

        self.state = "menu"
        self.after_id = None
        self.selected = 0
        self.ranking_recorded = False

        self.config = {
            "language": "en",
            "preview_count": 1,
            "fall_speed": 650,
            "rotate_direction": 1,
            "button_layout": "Shift",
        }

        self.menu_items = ["play", "config", "help", "ranking", "exit"]
        self.pause_items = ["resume", "retire"]
        self.confirm_items = ["no", "yes"]
        self.config_items = [
            "language",
            "preview_count",
            "fall_speed",
            "rotate_direction",
            "hold_key",
            "back",
        ]

        self.board = []
        self.current = None
        self.hold_piece = None
        self.hold_used = False
        self.queue = []
        self.score = 0
        self.lines = 0

        self.draw_menu()

    @property
    def texts(self):
        # 現在の言語設定に合った表示テキストを返す
        return TEXTS_BY_LANGUAGE[self.config["language"]]

    def ui_font(self, size, weight=None):
        # 日本語表示では読みやすい日本語フォントを優先する
        family = "Mintyo" if self.config["language"] == "ja" else "Consolas"
        if weight:
            return (family, size, weight)
        return (family, size)

    def run(self):
        # Tkinterのメインループを開始
        self.root.mainloop()

    def random_piece(self):
        # ランダムなテトリミノを生成
        return Tetromino(random.choice(list(SHAPES)))

    def ensure_queue(self):
        # 次のテトリミノを必要数だけ補充
        needed = max(1, self.config["preview_count"] + 1)
        while len(self.queue) < needed:
            self.queue.append(self.random_piece())

    def next_from_queue(self):
        # キューから次に落とすテトリミノを取り出す
        self.ensure_queue()
        piece = self.queue.pop(0)
        piece.reset_position()
        self.ensure_queue()
        return piece

    def start_game(self):
        # 新しいゲームを開始
        self.cancel_tick()
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current = None
        self.hold_piece = None
        self.hold_used = False
        self.queue = []
        self.score = 0
        self.lines = 0
        self.ranking_recorded = False
        self.state = "playing"
        self.spawn_piece()
        self.draw_game()
        self.schedule_tick()

    def spawn_piece(self):
        # 操作するテトリミノを出現させる
        self.current = self.next_from_queue()
        self.hold_used = False
        if self.collides(self.current.cells()):
            self.game_over()

    def cancel_tick(self):
        # 予約済みの自動落下タイマーを停止
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def schedule_tick(self):
        # 次の自動落下を予約
        self.cancel_tick()
        self.after_id = self.root.after(self.config["fall_speed"], self.tick)

    def tick(self):
        # 自動落下を1段進める
        self.after_id = None
        if self.state != "playing":
            return
        if not self.move(0, 1):
            self.lock_piece()
        if self.state == "playing":
            self.draw_game()
            self.schedule_tick()

    def collides(self, cells):
        # 壁や床や固定ブロックとの衝突を判定
        for x, y in cells:
            if x < 0 or x >= COLS or y >= ROWS:
                return True
            if y >= 0 and self.board[y][x] != EMPTY:
                return True
        return False

    def move(self, dx, dy):
        # 移動先が空いていればテトリミノを動かす
        cells = self.current.cells(x=self.current.x + dx, y=self.current.y + dy)
        if self.collides(cells):
            return False
        self.current.x += dx
        self.current.y += dy
        return True

    def rotate_current(self):
        # 設定された方向にテトリミノを回転
        direction = self.config["rotate_direction"]
        blocks = self.current.rotated(direction)
        for kick in (0, -1, 1, -2, 2):
            cells = self.current.cells(blocks=blocks, x=self.current.x + kick)
            if not self.collides(cells):
                self.current.blocks = blocks
                self.current.x += kick
                return

    def soft_drop(self):
        # 1段落として少し加点
        if self.move(0, 1):
            self.score += 1
        else:
            self.lock_piece()

    def hard_drop(self):
        # 一気に落として落下距離に応じて加点
        dropped = 0
        while self.move(0, 1):
            dropped += 1
        self.score += dropped * 2
        self.lock_piece()

    def hold_current(self):
        # 操作中のテトリミノをホールドと交換
        if self.hold_used:
            return

        outgoing = Tetromino(self.current.kind)
        if self.hold_piece is None:
            self.hold_piece = outgoing
            self.current = self.next_from_queue()
        else:
            incoming = self.hold_piece
            self.hold_piece = outgoing
            incoming.reset_position()
            self.current = incoming

        self.hold_used = True
        if self.collides(self.current.cells()):
            self.game_over()

    def lock_piece(self):
        # テトリミノを盤面に固定
        for x, y in self.current.cells():
            if y < 0:
                self.game_over()
                return
            self.board[y][x] = self.current.kind

        cleared = self.clear_lines()
        if cleared:
            self.lines += cleared
            self.score += [0, 100, 300, 500, 800][cleared]
        self.spawn_piece()

    def clear_lines(self):
        # そろった行を消して上に空行を追加
        kept = [row for row in self.board if EMPTY in row]
        cleared = ROWS - len(kept)
        new_rows = [[EMPTY for _ in range(COLS)] for _ in range(cleared)]
        self.board = new_rows + kept
        return cleared

    def pause_game(self):
        # プレイ中のゲームを一時停止
        self.cancel_tick()
        self.state = "paused"
        self.selected = 0
        self.draw_pause()

    def resume_game(self):
        # 一時停止メニューからゲームを再開
        self.state = "playing"
        self.draw_game()
        self.schedule_tick()

    def retire_game(self):
        # スコアを記録せずにメニューへ戻る
        self.cancel_tick()
        self.state = "menu"
        self.selected = 0
        self.draw_menu()

    def game_over(self):
        # ゲームを終了してスコアを記録
        texts = self.texts
        self.cancel_tick()
        self.state = "gameover"
        self.record_ranking()
        self.draw_game()
        self.canvas.create_rectangle(
            45, 210, COLS * CELL - 45, 375, fill="#10131a", outline="#f2d94e", width=2
        )
        self.canvas.create_text(
            COLS * CELL // 2,
            255,
            text=texts["game_over"]["title"],
            fill="#ffffff",
            font=self.ui_font(24, "bold"),
        )
        self.canvas.create_text(
            COLS * CELL // 2,
            305,
            text=texts["game_over"]["score"].format(score=self.score),
            fill="#cfd6e6",
            font=self.ui_font(15, "bold"),
        )
        self.canvas.create_text(
            COLS * CELL // 2,
            340,
            text=texts["game_over"]["footer"],
            fill="#cfd6e6",
            font=self.ui_font(14),
        )

    def record_ranking(self):
        # 現在のスコアを1回だけランキングに追加
        if self.ranking_recorded:
            return
        self.ranking_recorded = True
        record_score(self.score)

    def on_key(self, event):
        # 現在の画面状態に応じてキー入力を振り分け
        key = event.keysym

        if self.state == "menu":
            self.handle_menu_key(key)
        elif self.state == "config":
            self.handle_config_key(key)
        elif self.state in ("help", "ranking"):
            if key in ("Return", "Escape"):
                self.state = "menu"
                self.selected = 0
                self.draw_menu()
        elif self.state == "playing":
            self.handle_play_key(key)
        elif self.state == "paused":
            self.handle_pause_key(key)
        elif self.state == "retire_confirm":
            self.handle_confirm_key(key)
        elif self.state == "gameover" and key == "Return":
            self.state = "menu"
            self.selected = 0
            self.draw_menu()

    def handle_menu_key(self, key):
        # スタートメニューのキー操作を処理
        if key == "Up":
            self.selected = (self.selected - 1) % len(self.menu_items)
            self.draw_menu()
        elif key == "Down":
            self.selected = (self.selected + 1) % len(self.menu_items)
            self.draw_menu()
        elif key == "Return":
            item = self.menu_items[self.selected]
            if item == "play":
                self.start_game()
            elif item == "config":
                self.state = "config"
                self.selected = 0
                self.draw_config()
            elif item == "help":
                self.state = "help"
                self.draw_help()
            elif item == "ranking":
                self.state = "ranking"
                self.draw_ranking()
            elif item == "exit":
                self.root.destroy()

    def handle_config_key(self, key):
        # 設定画面のキー操作を処理
        if key == "Up":
            self.selected = (self.selected - 1) % len(self.config_items)
            self.draw_config()
        elif key == "Down":
            self.selected = (self.selected + 1) % len(self.config_items)
            self.draw_config()
        elif key in ("Left", "Right"):
            self.change_config(-1 if key == "Left" else 1)
            self.draw_config()
        elif key == "Return":
            if self.config_items[self.selected] == "back":
                self.state = "menu"
                self.selected = 0
                self.draw_menu()
            else:
                self.change_config(1)
                self.draw_config()
        elif key == "Escape":
            self.state = "menu"
            self.selected = 0
            self.draw_menu()

    def change_config(self, step):
        # 選択中の設定項目を変更
        item = self.config_items[self.selected]
        if item == "language":
            languages = list(TEXTS_BY_LANGUAGE)
            index = languages.index(self.config["language"])
            self.config["language"] = languages[(index + step) % len(languages)]
            self.root.title(self.texts["window_title"])
        elif item == "preview_count":
            self.config["preview_count"] = (self.config["preview_count"] + step) % 3
        elif item == "fall_speed":
            speeds = [900, 650, 400, 220]
            index = speeds.index(self.config["fall_speed"])
            self.config["fall_speed"] = speeds[(index + step) % len(speeds)]
        elif item == "rotate_direction":
            self.config["rotate_direction"] *= -1
        elif item == "hold_key":
            layouts = ["Shift", "Tab", "C"]
            index = layouts.index(self.config["button_layout"])
            self.config["button_layout"] = layouts[(index + step) % len(layouts)]

    def handle_play_key(self, key):
        # プレイ中のキー操作を処理
        if key == "Return":
            self.pause_game()
            return

        if key == "Left":
            self.move(-1, 0)
        elif key == "Right":
            self.move(1, 0)
        elif key == "Down":
            self.soft_drop()
        elif key == "Up":
            self.hard_drop()
        elif key == "space":
            self.rotate_current()
        elif self.is_hold_key(key):
            self.hold_current()

        if self.state == "playing":
            self.draw_game()

    def is_hold_key(self, key):
        # キーが設定中のホールドキーか判定
        layout = self.config["button_layout"]
        if layout == "Shift":
            return key in ("Shift_L", "Shift_R")
        if layout == "Tab":
            return key == "Tab"
        if layout == "C":
            return key.lower() == "c"
        return False

    def handle_pause_key(self, key):
        # 一時停止メニューのキー操作を処理
        if key == "Up":
            self.selected = (self.selected - 1) % len(self.pause_items)
            self.draw_pause()
        elif key == "Down":
            self.selected = (self.selected + 1) % len(self.pause_items)
            self.draw_pause()
        elif key == "Return":
            if self.pause_items[self.selected] == "resume":
                self.resume_game()
            else:
                self.state = "retire_confirm"
                self.selected = 0
                self.draw_retire_confirm()
        elif key == "Escape":
            self.resume_game()

    def handle_confirm_key(self, key):
        # リタイア確認画面のキー操作を処理
        if key in ("Left", "Right", "Up", "Down"):
            self.selected = (self.selected + 1) % len(self.confirm_items)
            self.draw_retire_confirm()
        elif key == "Return":
            if self.confirm_items[self.selected] == "yes":
                self.retire_game()
            else:
                self.state = "paused"
                self.selected = 0
                self.draw_pause()
        elif key == "Escape":
            self.state = "paused"
            self.selected = 0
            self.draw_pause()

    def draw_menu(self):
        # スタートメニューを描画
        texts = self.texts
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#151820", outline="")
        self.canvas.create_text(
            WIDTH // 2,
            105,
            text=GAME_TITLE,
            fill="#ffffff",
            font=("Arial Black", 38, "bold"),
        )
        self.draw_vertical_menu(
            [texts["menu"][item] for item in self.menu_items], 215, 45
        )

    def draw_config(self):
        # 設定画面を描画
        texts = self.texts
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#151820", outline="")
        self.canvas.create_text(
            WIDTH // 2,
            70,
            text=texts["config"]["title"],
            fill="#ffffff",
            font=self.ui_font(30, "bold"),
        )

        values = {
            "language": LANGUAGE_NAMES[self.config["language"]],
            "preview_count": str(self.config["preview_count"]),
            "fall_speed": texts["speed_names"].get(
                self.config["fall_speed"], str(self.config["fall_speed"])
            ),
            "rotate_direction": (
                texts["config"]["clockwise"]
                if self.config["rotate_direction"] > 0
                else texts["config"]["counter"]
            ),
            "hold_key": self.config["button_layout"],
            "back": "",
        }
        items = [
            (
                f"{texts['config'][item]}: {values[item]}"
                if values[item]
                else texts["config"][item]
            )
            for item in self.config_items
        ]
        self.draw_vertical_menu(items, 155, 45)
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT - 55,
            text=texts["config"]["footer"],
            fill="#8f9bb3",
            font=self.ui_font(11),
        )

    def draw_help(self):
        # 遊び方画面を描画
        texts = self.texts
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#151820", outline="")
        self.canvas.create_text(
            WIDTH // 2,
            55,
            text=texts["help"]["title"],
            fill="#ffffff",
            font=self.ui_font(28, "bold"),
        )
        lines = [
            line.format(hold_key=self.config["button_layout"])
            for line in texts["help"]["lines"]
        ]
        for i, text in enumerate(lines):
            self.canvas.create_text(
                75,
                120 + i * 32,
                anchor="w",
                text=text,
                fill="#cfd6e6",
                font=self.ui_font(14),
            )

    def draw_ranking(self):
        # ランキング画面を描画
        texts = self.texts
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#151820", outline="")
        self.canvas.create_text(
            WIDTH // 2,
            65,
            text=texts["ranking"]["title"],
            fill="#ffffff",
            font=self.ui_font(30, "bold"),
        )
        rankings = load_rankings()
        if not rankings:
            self.canvas.create_text(
                WIDTH // 2,
                220,
                text=texts["ranking"]["empty"],
                fill="#cfd6e6",
                font=self.ui_font(18),
            )
        else:
            for i, row in enumerate(rankings[:5], start=1):
                line = f"{i}: {row.get('score', 0)}: {row.get('date', '----/--/--')}"
                self.canvas.create_text(
                    WIDTH // 2,
                    140 + i * 48,
                    text=line,
                    fill="#cfd6e6",
                    font=self.ui_font(18, "bold"),
                )
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT - 55,
            text=texts["ranking"]["footer"],
            fill="#8f9bb3",
            font=self.ui_font(12),
        )

    def draw_pause(self):
        # ゲーム画面の上に一時停止表示を描画
        texts = self.texts
        self.draw_game()
        self.canvas.create_rectangle(
            60, 165, COLS * CELL - 60, 385, fill="#10131a", outline="#f2d94e", width=2
        )
        self.canvas.create_text(
            COLS * CELL // 2,
            210,
            text=texts["pause"]["title"],
            fill="#ffffff",
            font=self.ui_font(25, "bold"),
        )
        self.draw_vertical_menu(
            [texts["pause"][item] for item in self.pause_items],
            275,
            48,
            center_x=COLS * CELL // 2,
        )

    def draw_retire_confirm(self):
        # リタイア確認表示を描画
        texts = self.texts
        self.draw_game()
        self.canvas.create_rectangle(
            25, 150, COLS * CELL - 25, 405, fill="#10131a", outline="#ef5a68", width=2
        )
        self.canvas.create_text(
            COLS * CELL // 2,
            195,
            text=texts["retire"]["title"],
            fill="#ffffff",
            font=self.ui_font(15, "bold"),
        )
        self.canvas.create_text(
            COLS * CELL // 2,
            240,
            text=texts["retire"]["message"],
            fill="#cfd6e6",
            font=self.ui_font(11),
        )
        self.draw_vertical_menu(
            [texts["retire"][item] for item in self.confirm_items],
            305,
            42,
            center_x=COLS * CELL // 2,
        )

    def draw_vertical_menu(self, items, start_y, gap, center_x=None):
        # 共通の縦メニューを描画
        center_x = WIDTH // 2 if center_x is None else center_x
        for i, item in enumerate(items):
            y = start_y + i * gap
            fill = "#f2d94e" if i == self.selected else "#cfd6e6"
            prefix = "> " if i == self.selected else "  "
            self.canvas.create_text(
                center_x,
                y,
                text=prefix + item,
                fill=fill,
                font=self.ui_font(18, "bold"),
            )

    def draw_game(self):
        # 盤面とサイドパネルと操作中テトリミノを描画
        self.canvas.delete("all")
        self.draw_board()
        self.draw_side_panel()

        if self.current and self.state in ("playing", "paused", "retire_confirm"):
            for x, y in self.current.cells():
                if y >= 0:
                    self.draw_cell(x, y, COLORS[self.current.kind])

    def draw_board(self):
        # 固定ブロックと盤面グリッドを描画
        self.canvas.create_rectangle(
            0, 0, COLS * CELL, HEIGHT, fill="#10131a", outline="#343b4c"
        )
        for y in range(ROWS):
            for x in range(COLS):
                kind = self.board[y][x]
                if kind:
                    self.draw_cell(x, y, COLORS[kind])
                else:
                    x1 = x * CELL
                    y1 = y * CELL
                    self.canvas.create_rectangle(
                        x1, y1, x1 + CELL, y1 + CELL, outline="#202633", width=1
                    )
        self.canvas.create_line(0, 0, COLS * CELL, 0, fill="#ef5a68", width=3)

    def draw_cell(self, x, y, color):
        # 盤面の1マスを描画
        x1 = x * CELL
        y1 = y * CELL
        self.canvas.create_rectangle(
            x1 + 2,
            y1 + 2,
            x1 + CELL - 2,
            y1 + CELL - 2,
            fill=color,
            outline="#e9edf5",
            width=1,
        )
        self.canvas.create_rectangle(
            x1 + 5, y1 + 5, x1 + CELL - 5, y1 + CELL - 5, outline="#ffffff", width=1
        )

    def draw_side_panel(self):
        # ホールドや次ピースやスコアを描画
        texts = self.texts
        x0 = COLS * CELL
        self.canvas.create_rectangle(x0, 0, WIDTH, HEIGHT, fill="#1d2230", outline="")
        self.canvas.create_text(
            x0 + 22,
            30,
            anchor="w",
            text=texts["side_panel"]["hold"],
            fill="#ffffff",
            font=self.ui_font(15, "bold"),
        )
        if self.hold_piece:
            self.draw_preview(self.hold_piece, x0 + 45, 54)

        self.canvas.create_text(
            x0 + 22,
            165,
            anchor="w",
            text=texts["side_panel"]["next"],
            fill="#ffffff",
            font=self.ui_font(15, "bold"),
        )
        for i, piece in enumerate(self.queue[: self.config["preview_count"]]):
            self.draw_preview(piece, x0 + 45, 190 + i * 95, scale=20)

        self.canvas.create_text(
            x0 + 22,
            410,
            anchor="w",
            text=texts["side_panel"]["score"].format(score=self.score),
            fill="#cfd6e6",
            font=self.ui_font(14, "bold"),
        )
        self.canvas.create_text(
            x0 + 22,
            490,
            anchor="w",
            text=texts["side_panel"]["lines"].format(lines=self.lines),
            fill="#cfd6e6",
            font=self.ui_font(14, "bold"),
        )

    def draw_preview(self, piece, px, py, scale=22):
        # 小さなテトリミノのプレビューを描画
        blocks = piece.blocks
        min_x = min(x for x, _ in blocks)
        max_x = max(x for x, _ in blocks)
        min_y = min(y for _, y in blocks)
        max_y = max(y for _, y in blocks)
        offset_x = (4 - (max_x - min_x + 1)) * scale // 2
        offset_y = (3 - (max_y - min_y + 1)) * scale // 2

        for bx, by in blocks:
            x1 = px + (bx - min_x) * scale + offset_x
            y1 = py + (by - min_y) * scale + offset_y
            self.canvas.create_rectangle(
                x1 + 2,
                y1 + 2,
                x1 + scale - 2,
                y1 + scale - 2,
                fill=COLORS[piece.kind],
                outline="#e9edf5",
            )
