import os
import sys

from dftt_timecode import DfttTimecode

from item_creator import add_wav_files_with_structure

# 设置 DaVinci Resolve 的 API 路径和库路径
resolve_script_api = (
    r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
)
resolve_script_lib = (
    r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
)
python_path = os.path.join(resolve_script_api, "Modules")

# 动态设置环境变量
os.environ["RESOLVE_SCRIPT_API"] = resolve_script_api
os.environ["RESOLVE_SCRIPT_LIB"] = resolve_script_lib
os.environ["PYTHONPATH"] = f"{os.environ.get('PYTHONPATH', '')};{python_path}"

# 添加库路径到系统路径（如果需要导入模块）
if python_path not in sys.path:
    sys.path.append(python_path)

# 检查是否成功加载环境变量
print("RESOLVE_SCRIPT_API:", os.environ["RESOLVE_SCRIPT_API"])
print("RESOLVE_SCRIPT_LIB:", os.environ["RESOLVE_SCRIPT_LIB"])
print("PYTHONPATH:", os.environ["PYTHONPATH"])

import DaVinciResolveScript  # noqa: E402

resolve = DaVinciResolveScript.scriptapp("Resolve")


def add_1hour(tc):
    tc = DfttTimecode(tc)
    one = DfttTimecode("01:00:00:00")  # pyright: ignore
    tc = tc + one
    return tc.timecode_output("smpte")


def main(folder_path: str, project_name: str = "test"):
    project = resolve.GetProjectManager().CreateProject(project_name)
    if project is None:
        print("The input Project Name is not unique, try another")
        return
    pool = project.GetMediaPool()
    folder = pool.GetRootFolder().GetSubFolderList()[0]
    clips = folder.GetClipList()
    for clip in clips:
        start = clip.GetClipProperty("Start TC")
        clip.SetClipProperty("Start TC", add_1hour(start))
        end = clip.GetClipProperty("Start TC")
        clip.SetClipProperty("End TC", add_1hour(end))
    audio_sync_settings = {
        resolve.AUDIO_SYNC_MODE: resolve.AUDIO_SYNC_TIMECODE,
        resolve.AUDIO_SYNC_CHANNEL_NUMBER: 1,
        resolve.AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO: True,
        resolve.AUDIO_SYNC_RETAIN_VIDEO_METADATA: False,
    }
    clips_t = pool.AppendToTimeline(clips)
    pool.CreateEmptyTimeline(project_name)
    t = project.GetCurrentTimeline()
    t.AddTrack("audio", "mono")
    t.GetTrackCount("audio")
    t.SetTrackName("audio", 1, "test")
    resolve.AUDIO_SYNC_MODE
    # pool.AppendToTimeline(self, clips)
    return add_wav_files_with_structure(pool, folder_path)


if __name__ == "__main__":
    main(r"C:\CreativeProjects\长安-2min预告\Audio Files\OrganizedFiles")
