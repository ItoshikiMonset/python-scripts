#!/usr/bin/env python3
# coding: utf-8

"""
Tag a .mkv file or directory of .mkv files
[!] mkvtoolnix must be installed and in your $PATH
ex: mkv_metadata_setter.py -src /path/to/file.mkv -vn "Video track" -an "Audio track" -sn "Sub track"
"""

import os
import argparse
from pathlib import Path
from shlex import quote
from typing import List
from utils import common
from utils import mkvfile

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Path to directory or single MKV file")
    parser.add_argument("-a", "--audio-name", dest="audio_name", type=str, default=None, help="Name of the audio tracks, comma separated")
    parser.add_argument("-b", "--sub-name", dest="sub_name", type=str, default=None, help="Name of the subtitles tracks, comma separated")
    parser.add_argument("-c", "--video-name", dest="video_name", type=str, default=None, help="Name of the video track")
    parser.add_argument("-x", "--audio-lang", dest="audio_lang", type=str, default="und", help="Lang of the audio tracks, comma separated")
    parser.add_argument("-y", "--sub-lang", dest="sub_lang", type=str, default="eng", help="Lang of the subtitles tracks, comma separated")
    parser.add_argument("-z", "--video-lang", dest="video_lang", type=str, default="und", help="Lang of the video track")
    parser.add_argument("-r", "--repl", dest="repl", type=str, default="", help="Pattern to replace for the Title")
    args = parser.parse_args()


    # Get a list of files
    files = common.list_directory(args.input.resolve(), lambda x: x.suffix == ".mkv", True)

    for f in files:
        mkv = mkvfile.MkvFile(f)
        cmd = f'mkvpropedit {quote(str(f))}'

        # Handle subtitles tracks
        stracks = list(filter(lambda x: x.type == "subtitles", mkv.tracks))
        sub_langs = args.sub_lang.split(",")
        sub_names = args.sub_name.split(",") if args.sub_name else []
        tid = 1
        for track in stracks:
            if tid <= len(sub_langs):
                sl = sub_langs[tid - 1]
            else:
                sl = "und"
            sn = f'{sl.upper()}'
            forced = False
            if tid <= len(sub_names):
                s = sub_names[tid - 1]
                forced = "forced" in s.lower()
                sn += f' — {s}'
            cmd += f' --edit track:s2 --set flag-default=0 --edit track:s3 --set flag-default=1'
            tid += 1
        title = f.stem.replace(args.repl, "")
        cmd += f' --edit info --set title={quote(title)}'
        os.system(cmd)
 
