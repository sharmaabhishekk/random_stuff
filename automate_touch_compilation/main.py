import os
import json
import argparse

import cv2
import numpy as np
from PIL import Image
import pytesseract

from pandas import json_normalize
from moviepy.editor import VideoFileClip, concatenate_videoclips

def save_kickoff_time():

    """ Only run when text file not found
    """

    vid.set(cv2.CAP_PROP_POS_MSEC,clip_time_min*60_000) 
    success, image = vid.read()

    ## Select ROI
    r = cv2.selectROI(image, False)
        
    ## Crop image
    cropped_im = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    cropped_im = cv2.medianBlur(cropped_im, 3)
    im_pil = Image.fromarray(cropped_im)
    text = pytesseract.image_to_string(im_pil, config='--psm 6')

    m, s = text.strip().split(':')
    m, s = int(m), int(s)
    print(f'Detected time: {m} mins and {s} secs')

    cv2.imshow('Selected', cropped_im)
    cv2.waitKey(0)

    with open(fr'..\timestamps\{fname}.txt', 'w') as f:
        f.write(str((clip_time_min - (m+s/60))*60_000))

def get_event_data(match_id):
    with open(fr'C:\repository\open-data\data\events\{match_id}.json', 'r') as f:
        md = json.load(f)
    df = json_normalize(md, sep='_')
    df['loc_x'] = df['location'].apply(lambda val: np.nan if val!=val else val[0])
    df['loc_y'] = df['location'].apply(lambda val: np.nan if val!=val else val[1])
    df.drop('location', axis=1, inplace=True)

    return df

def return_events_ts(df, query_str):
    """Takes in the events dataframe, runs the given query and then returns the matching timestamps converted to seconds"""
    pdf = df.query(query_str)
    return (pdf['minute']*60 + pdf['second']).values

def join_and_save_video(timestamps, gap=2.5):
    if len(timestamps)>0:

        ko_sec_ts = ko_millisec_ts/1000
        
        clip = VideoFileClip(fr'..\footage\{filename}')
        clip_list = [clip.subclip(t+ko_sec_ts-gap, t+ko_sec_ts+gap) for n,t in enumerate(timestamps)]    

        video = concatenate_videoclips(clip_list, method='compose')
        video_outname = "".join(i for i in query_str if i not in "\/:*?<>|")
        video.write_videofile(fr'..\out\{video_outname}.mp4', threads=4, audio=False)
        print('All done!')
    else:
        print('There are no events which match your query. Maybe try a different query?') 

#######
if __name__ == '__main__':

    if not os.path.exists(fr'..\timestamps'):
        os.mkdir(fr'..\timestamps')

    if not os.path.exists(fr'..\out'):
        os.mkdir(fr'..\out')

    parser = argparse.ArgumentParser(description='Automate Touch Compilation')
    parser.add_argument('-v', '--video_filename', type=str, help='The name of the match video in the footage directory.', required=True)
    parser.add_argument('-e', '--event_matchid', type=int, help='The name of the match_id/file_name for the Statsbomb JSON file.', required=True)
    parser.add_argument('-q', '--query', type=str, help='The pandas query to run to filter the timestamps', required=True)
    parser.add_argument('-t', '--video_timestamp', type=int, help='The video time to use to infer the match clock. Make sure this frame has the clock prominently displayed', required=True)

    args = parser.parse_args()    

    filename = args.video_filename
    fname, fext = os.path.splitext(filename)

    clip_time_min = args.video_timestamp ##ensure this time is at least some frame of the game where the timestamp is visible
    vid = cv2.VideoCapture(fr'..\footage\{filename}')

    if not os.path.exists(fr'..\timestamps\{fname}.txt'):
        save_kickoff_time()

    with open(fr'..\timestamps\{fname}.txt', 'r') as f:
        ko_millisec_ts = float(f.read())

    df = get_event_data(args.event_matchid)
    query_str = args.query ##f""
    timestamps = return_events_ts(df, query_str)
    print(len(timestamps))
    join_and_save_video(timestamps)

##python main.py -v '2018_Francia_-_Croacia_-_1.mp4' -e 8658 -t 20 -q "player_name == 'Paul Pogba' & type_name == 'Pass' & period == 1"   
##python main.py -v '2018_Francia_-_Croacia_-_1.mp4' -e 8658 -t 20 -q "team_name == 'Croatia' & type_name == 'Pressure' & loc_x>= 60 & period == 1"   
