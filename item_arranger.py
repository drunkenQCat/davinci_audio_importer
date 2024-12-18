from collections import defaultdict
from pprint import pp
from davinci_media_item import DRMediaItem


def _get_item_start_in_frame(item: DRMediaItem):
    """
    获取媒体项的起始帧数。

    参数:
        item (DRMediaItem): 需要获取起始帧数的媒体项。

    返回:
        int: 媒体项的起始帧数。
    """
    return item.start_tc.timecode_output("frame")


def group_items_by_character_and_track(
    media_items: list[DRMediaItem],
) -> defaultdict[str, defaultdict[str, list[DRMediaItem]]]:
    """
    根据角色（character）和轨道（track）对 media_items 进行分组。
    
    参数:
        media_items (list[DRMediaItem]): 需要分组的媒体项列表。
    
    返回:
        defaultdict[str, defaultdict[str, list[DRMediaItem]]]: 一个嵌套的defaultdict，结构为 {character: {track: [items]}}。
    """
    characters = defaultdict(lambda: defaultdict(list))  # {character: {track: [items]}}
    for item in media_items:
        characters[item.character][item.track].append(item)
    return characters


def _sort_items_by_start_tc(items: list[DRMediaItem]):
    """
    按照 `start_tc` 排序 `items`。
    """
    items.sort(key=_get_item_start_in_frame)


def _handle_overlapping_items(
    current_item: DRMediaItem, next_item: DRMediaItem, characters: defaultdict
):
    """
    检查当前 item 是否盖住下一个 item，如果盖住，则将下一个 item 移动到下一个轨道。
    """
    if current_item.end_tc > next_item.start_tc:
        # 如果当前项盖住了下一个项
        pp(
            f"overlap: current_item.end_tc: {current_item.end_tc}, next_item.start_tc: {next_item.start_tc}"
        )
        pp(
            f"current_item: {current_item.character}, {current_item.track}, {current_item.start_tc}, {current_item.end_tc}"
        )
        current_item.track = str(
            int(current_item.track) + 1
        )  # 假设轨道编号是整数并按顺序命名
        pp(f"try to move next_item to next track: {next_item.track}")

        # 递归检查下一个轨道是否也有重叠
        _resolve_item_overlap(current_item, characters)


def _resolve_item_overlap(current_item: DRMediaItem, characters: defaultdict):
    """
    递归检查并解决轨道之间的重叠。
    如果重叠，则将 item 移动到下一个轨道，直到没有重叠为止。
    """
    while True:
        next_track_items = characters[current_item.character].get(
            current_item.track, []
        )
        _sort_items_by_start_tc(next_track_items)

        # 检查该轨道上的最后一个 item 是否与 next_item 有重叠
        if next_track_items and next_track_items[-1].end_tc > current_item.start_tc:
            # 如果重叠，继续移动到下一个轨道
            current_item.track = str(int(current_item.track) + 1)
        else:
            # 如果没有重叠，退出循环
            characters[current_item.character][current_item.track].append(current_item)
            break


def _process_track(items: list[DRMediaItem], characters: defaultdict):
    """
    处理每个轨道，检查并处理轨道上的 item 是否有重叠。
    """
    _sort_items_by_start_tc(items)  # 排序轨道上的 items

    # 遍历每个轨道，检查是否有重叠
    for i in range(len(items) - 1):
        current_item = items[i]
        next_item = items[i + 1]

        # 检查并处理重叠
        _handle_overlapping_items(current_item, next_item, characters)

    # 重新排序当前轨道上的 item
    _sort_items_by_start_tc(items)


def get_character_track_dict(
    media_items: list[DRMediaItem],
) -> dict[str, list[DRMediaItem]]:
    """
    统计 `media_items` 中所有的 `character` 和 `track` 组合，
    并返回一个字典，键是 "character-track" 形式的字符串，值是该组合下的 DRMediaItem 列表。
    """
    character_track_dict = defaultdict(list)  # 使用 defaultdict 方便地添加元素

    for item in media_items:
        # 获取每个 item 的 character 和 track
        combination = f"{item.character}-{item.track}"
        character_track_dict[combination].append(item)

    return dict(character_track_dict)  # 转换为常规字典并返回


def rearrange_items(media_items: list[DRMediaItem]):
    """
    检查每个 `character` 的每条 `track`，确保没有时间码重叠的情况。
    如果发生重叠，移动被覆盖的 `item` 到下一个轨道，直到没有重叠，或者创建新轨道。
    """
    # 将 `media_items` 按 `character` 和 `track` 分组
    characters = group_items_by_character_and_track(media_items)

    # 遍历每个 character 和它的轨道
    for character, tracks in characters.items():
        # 避免在遍历时修改字典，可以先将轨道和 items 提取到一个列表中
        track_items = list(tracks.items())

        for track, items in track_items:
            _process_track(items, characters)

    # 收集所有最终结果
    rearranged_items = []
    for character, tracks in characters.items():
        for track, items in tracks.items():
            rearranged_items.extend(items)

    return get_character_track_dict(rearranged_items)  # 返回重新排序的 item 列表
