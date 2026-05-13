try:
    from .constants import COLS, SHAPES
except ImportError:
    from constants import COLS, SHAPES


class Tetromino:
    def __init__(self, kind):
        # テトリミノの種類と出現位置を設定
        self.kind = kind
        self.blocks = list(SHAPES[kind])
        self.x = COLS // 2 - 2
        self.y = -1

    def cells(self, blocks=None, x=None, y=None):
        # 相対座標を盤面上の座標に変換
        blocks = self.blocks if blocks is None else blocks
        x = self.x if x is None else x
        y = self.y if y is None else y
        return [(x + bx, y + by) for bx, by in blocks]

    def reset_position(self):
        # 元の形と出現位置に戻す
        self.blocks = list(SHAPES[self.kind])
        self.x = COLS // 2 - 2
        self.y = -1

    def rotated(self, direction):
        # 回転後のブロック配置を返す
        if self.kind == "O":
            return self.blocks

        if direction < 0:
            blocks = [(by, 3 - bx) for bx, by in self.blocks]
        else:
            blocks = [(3 - by, bx) for bx, by in self.blocks]

        min_x = min(x for x, _ in blocks)
        min_y = min(y for _, y in blocks)
        return [(x - min_x, y - min_y) for x, y in blocks]
