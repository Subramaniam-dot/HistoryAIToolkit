"""
This takes three args, a filepath to an audio file, audio start and audio end times.

It will sample the file specified for that many minutes and seconds. 

The audio start and end times currently support time in minutes and seconds only.
Example: python interviewkit/slicer.py data/Martine+Barrat_FINAL.mp3 105:40 to 107:40 
means audio will be sliced from 105min 40sec to 107min and 40sec.

`ffmpeg` is a requirement for this to work.

Example usage:
    Format:  python interviewkit/slicer.py path_to_audio_file audio_slice_start_time audio_slice_end_time
    Example: python interviewkit/slicer.py data/Martine+Barrat_FINAL.mp3 2 3
    Example: python interviewkit/slicer.py data/Martine+Barrat_FINAL.mp3 105:40 to 107:40

This generates:

    data/sampled-5-Martine+Barrat_FINAL.mp3

"""
import sys
from pathlib import Path
import shutil

try:
    import pydub
except ImportError:
    print("Please install pydub: pip install pydub")
    exit(1)

if shutil.which("ffmpeg") is None:
    print("Please install ffmpeg: https://ffmpeg.org/download.html")
    print("  On mac you can: brew install ffmpeg")
    exit(1)

def convert_audio_time_to_msec(audio_time_split_list):
    """ Converting mins and secs to msecs for pydub computation """

    if(audio_time_split_list):
        if(len(audio_time_split_list) == 1):
            return int(audio_time_split_list[0]) * 60 * 1000
        elif(len(audio_time_split_list) == 2):
            return int(audio_time_split_list[0]) * 60 * 1000 + int(audio_time_split_list[1]) * 1000
        else:
            print("Error! Audio slice input params invalid. Audio slice supports start/end time in mins or mins:secs format. Please try again with correct input times.")
            print("Error inside convert_audio_time_to_msec(audio_time_split_list) funtion.")
            exit(1)
    else:
        print("Error! Audio slice input params invalid. Please try again with correct parameters.")
        print("Error inside convert_audio_time_to_msec(audio_time_split_list) funtion.")
        exit(1)

def export_filename(audio_time_list):
    """ Filename for exported file """
    
    if audio_time_list and len(audio_time_list) == 2:
        return f"{audio_time_list[0]}m{audio_time_list[1]}s"
    elif audio_time_list and len(audio_time_list) == 1:
        return f"{audio_time_list[0]}m"
    else:
        print("Error! Audio slice input params invalid. Please try again with correct parameters.")
        print("Error inside export_filename(audio_time_list) funtion.")
        exit(1)


def audio_slicing(path, audio_slice_start_time, audio_slice_end_time):
    """ It reads the original audio and uses start and end input time params to generate sliced audio. """
    
    print("Sampling {} from {} to {}".format(path, audio_slice_start_time, audio_slice_end_time))

    # Reading original audio file
    audio = pydub.AudioSegment.from_file(path)
    original_audio_size_ms = audio.duration_seconds * 1000

    # Fetching mins and secs from audio input
    audio_start_time_list = audio_slice_start_time.split(":")
    audio_end_time_list = audio_slice_end_time.split(":")

    # Converting audio start and end times in msecs
    audio_start_time = convert_audio_time_to_msec(audio_start_time_list)
    audio_end_time = convert_audio_time_to_msec(audio_end_time_list)
    
    # Check if audio start and end times are within original audio size limits
    if(audio_start_time > original_audio_size_ms or audio_end_time > original_audio_size_ms):
        print("Error! Audio slice input params cannot be greater than original audio size. Please try again with correct parameters.")
        exit(1)

    # Audio slicing process
    audio = audio[audio_start_time:audio_end_time]

    # Filename for exported file
    audio_start_time_name = export_filename(audio_start_time_list)
    audio_end_time_name = export_filename(audio_end_time_list)
    new_filename =  f"{path.parent}/sampled-{audio_start_time_name}-{audio_end_time_name}-{path.name}"
    audio.export(new_filename, format="mp3")
    print("Created new file: ", new_filename)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 slicer.py <filepath> <audio start time in minutes> <audio end time in minutes>")
        return

    path = Path(sys.argv[1])
    audio_slice_start_time = (sys.argv[2])
    audio_slice_end_time = (sys.argv[3])

    audio_slicing(path, audio_slice_start_time, audio_slice_end_time)

if __name__ == '__main__':
    main()
