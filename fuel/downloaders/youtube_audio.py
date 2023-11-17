import os

try:
    import pafy
    PAFY_AVAILABLE = True
except ImportError:
    PAFY_AVAILABLE = False


def download(directory, youtube_id, clear=False):
    """Download the audio of a YouTube video.

    The audio is downloaded in the highest available quality. Progress is
    printed to `stdout`. The file is named `youtube_id.m4a`, where
    `youtube_id` is the 11-character code identifiying the YouTube video
    (can be determined from the URL).

    Parameters
    ----------
    directory : str
        The directory in which to save the downloaded audio file.
    youtube_id : str
        11-character video ID (taken from YouTube URL)
    clear : bool
        If `True`, it deletes the downloaded video. Otherwise it downloads
        it. Defaults to `False`.

    """
    filepath = os.path.join(directory, f'{youtube_id}.m4a')
    if clear:
        os.remove(filepath)
        return
    if not PAFY_AVAILABLE:
        raise ImportError("pafy is required to download YouTube videos")
    url = f'https://www.youtube.com/watch?v={youtube_id}'
    video = pafy.new(url)
    audio = video.getbestaudio()
    audio.download(quiet=False, filepath=filepath)


def fill_subparser(subparser):
    """Sets up a subparser to download audio of YouTube videos.

    Adds the compulsory `--youtube-id` flag.

    Parameters
    ----------
    subparser : :class:`argparse.ArgumentParser`
        Subparser handling the `youtube_audio` command.

    """
    subparser.add_argument(
        '--youtube-id', type=str, required=True,
        help=("The YouTube ID of the video from which to extract audio, "
              "usually an 11-character string.")
    )
    return download
