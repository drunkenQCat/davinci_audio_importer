from typing import Any
from dftt_timecode import DfttTimecode
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DRMediaItem:
    item: Any
    default_offset_smpte: str = "01:00:00:00"

    def __post_init__(self):
        # 从 `item` 中获取起始和结束时间码
        self.default_offset = DfttTimecode(
            self.default_offset_smpte  # pyright: ignore
        )  # 默认时间码偏移 # pyright: ignore
        self.fps = float(self.item.GetClipProperty("FPS"))  # pyright: ignore
        self.start_tc = DfttTimecode(
            self.item.GetClipProperty("Start TC"), fps=self.fps  # pyright: ignore
        )  # pyright: ignore
        self.end_tc = DfttTimecode(
            self.item.GetClipProperty("End TC"), fps=self.fps  # pyright: ignore
        )

        # 获取文件路径和轨道路径
        self._item_path = Path(
            self.item.GetClipProperty("File Path")  # pyright: ignore
        )  # pyright: ignore
        self._track_path = self._item_path.parent

        # 轨道和人物名称
        self.track = self._track_path.name
        self.character = self._track_path.parent.name

        # 获取帧率

        # 计算时间轴中的起始和结束时间码
        self.start_timecode_in_timeline = (
            self.start_tc + self.default_offset
        ).timecode_output("smpte")
        self.end_timecode_in_timeline = (
            self.end_tc + self.default_offset
        ).timecode_output("smpte")
