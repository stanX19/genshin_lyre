try:
    from ... import utils
except ImportError:
    import utils
try:
    import lyre_mp4_to_score
    save_video_as_nightly = lyre_mp4_to_score.save_video_as_nightly
except ImportError as exc:
    def decorator(exc):
        def func(save_dir: str, vid_path: list[str]):
            utils.print_cmd_color("DarkYellow",
                                  f"Failed to import 'lyre_mp4_to_score' module\n    Error: {exc}")
            print()
        return func
    save_video_as_nightly = decorator(exc)
except AttributeError as exc:
    def decorator(exc):
        def func(save_dir: str, vid_path: list[str]):
            utils.print_cmd_color("DarkYellow",
                                  f"Error: 'lyre_mp4_to_score' module is not available")
            print()
        return func
    save_video_as_nightly = decorator(exc)
