from pathlib import Path
from time import sleep
from typing import Any

from davinci_media_item import DRMediaItem
from hello import resolve


def add_wav_files_with_structure(pool: Any, path_of_folder: str) -> list[DRMediaItem]:
    """
    递归遍历文件夹，将 WAV 文件添加到 DaVinci Resolve 媒体池，并保留文件夹结构，同时封装成 DRMediaItem 对象。

    ms: MediaStorage 对象
    root_folder: 媒体池中的根文件夹, 实际为 Folder 类型
    path_of_folder: 需要扫描并添加文件的文件夹路径
    """
    root_folder = pool.GetRootFolder()
    pool.SetCurrentFolder(root_folder)
    sleep(0.1)
    ms = resolve.GetMediaStorage()

    def create_media_item(current_path: Path):
        # 添加 WAV 文件到媒体池
        dr_items = ms.AddItemListToMediaPool(str(current_path))

        # 对于每个 WAV 文件，封装成 DRMediaItem 并添加到列表中
        for item in dr_items:
            # 获取 MediaPoolItem 对象
            dr_item = DRMediaItem(item=item)  # 创建 DRMediaItem 实例
            media_items.append(dr_item)  # 将 DRMediaItem 添

    root_path = Path(path_of_folder)
    media_items = []  # 存储所有的 DRMediaItem 实例

    def add_files_to_pool(current_folder: Any, current_path: Path):
        # 获取当前文件夹下所有的 WAV 文件
        pool.SetCurrentFolder(current_folder)
        sleep(0.1)
        wav_files = list(current_path.glob("*.wav"))

        if wav_files:
            create_media_item(current_path)

        # 递归处理子文件夹
        for subfolder in current_path.iterdir():
            if not subfolder.is_dir():
                continue
            # 创建对应的子文件夹
            new_folder = pool.AddSubFolder(current_folder, subfolder.name)
            # 递归调用处理子文件夹
            add_files_to_pool(new_folder, subfolder)
        pool.SetCurrentFolder(current_folder)
        sleep(0.1)

    # 从根文件夹开始递归处理
    add_files_to_pool(root_folder, root_path)
    pool.SetCurrentFolder(root_folder)
    sleep(0.1)

    return media_items  # 返回所有创建的 DRMediaItem 实例
