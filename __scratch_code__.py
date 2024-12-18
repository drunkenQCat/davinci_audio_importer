from dftt_timecode import DfttTimecode

from resolve_api_init import RESOLVE


def add_1hour(tc):
    tc = DfttTimecode(tc)
    one = DfttTimecode("01:00:00:00")  # pyright: ignore
    tc = tc + one
    return tc.timecode_output("smpte")


def testcode(pool, project_name: str = "test"):
    project = RESOLVE.GetProjectManager().CreateProject(project_name)
    folder = pool.GetRootFolder().GetSubFolderList()[0]
    clips = folder.GetClipList()
    for clip in clips:
        start = clip.GetClipProperty("Start TC")
        clip.SetClipProperty("Start TC", add_1hour(start))
        end = clip.GetClipProperty("Start TC")
        clip.SetClipProperty("End TC", add_1hour(end))
    audio_sync_settings = {
        RESOLVE.AUDIO_SYNC_MODE: RESOLVE.AUDIO_SYNC_TIMECODE,
        RESOLVE.AUDIO_SYNC_CHANNEL_NUMBER: 1,
        RESOLVE.AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO: True,
        RESOLVE.AUDIO_SYNC_RETAIN_VIDEO_METADATA: False,
    }
    clips_t = pool.AppendToTimeline(clips)
    pool.CreateEmptyTimeline(project_name)
    t = project.GetCurrentTimeline()
    t.AddTrack("audio", "mono")
    t.GetTrackCount("audio")
    t.SetTrackName("audio", 1, "test")
    RESOLVE.AUDIO_SYNC_MODE
    # pool.AppendToTimeline(self, clips)
