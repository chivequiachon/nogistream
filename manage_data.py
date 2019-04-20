import sys, os
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nogistream.settings")

import django
django.setup()

from VideoManagement.models import VideoInfo

def update_video_info(video_csv_row):
    video = VideoInfo.objects.get(pk=video_csv_row[0])
    video.real_id = video_csv_row[1]
    video.embed_link = video_csv_row[2]
    video.is_disabled = video_csv_row[3]
    video.save()
    
# the main function for the script, called by the shell    
if __name__ == "__main__":
    ret_flag = 1
    argument_length = len(sys.argv)
    if argument_length > 1:
        if sys.argv[1] == 'GET':
            videos = VideoInfo.objects.filter(is_disabled=True)
            for v in videos:
                print("%s - %s" % (v.id, v.title))
            ret_flag = 0
        elif sys.argv[1] == "UPDATE":
            if argument_length > 2 and sys.argv != "":
                videos_df = pd.read_csv(sys.argv[2])
                print(videos_df)
                videos_df.apply(update_video_info, axis=1)
                ret_flag = 0
            else:
                print("Please provide csv file!")
                ret_flag = 1
        elif sys.argv[1] == 'INSERT':
            pass
    
    sys.exit(ret_flag)

