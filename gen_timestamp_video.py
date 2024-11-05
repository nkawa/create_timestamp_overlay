import cv2
import numpy as np
import datetime

# タイムスタンプ専用のビデオを作成
# 以下のコマンドでタイムスタンプをオーバーレイするビデオを作成
#ffmpeg -i overlap_0700_2100_2x_nkawa1934.mp4  -i ../timestamp_0700_2100.mp4 -filter_complex "[1:0]colorkey=black:0.01:1[colorkey];[0:0][colorkey]overlay=x=0:y=0" -c:v libx265 -tag:v hvc1 with_timestamp_0700_2100_2x_nkawa1934.mp4

def make_timestamp_video(from_time, to_time, frame_rate, video_rate, shape):


    width,height = (int(x) for x in  shape.split(","))
    print("width",width,"height",height)

    from_time = datetime.datetime.strptime("2024-10-03 "+from_time+":00", "%Y-%m-%d %H:%M:%S")
    to_time = datetime.datetime.strptime("2024-10-03 "+to_time+":00", "%Y-%m-%d %H:%M:%S")
    frame_rate = float(frame_rate)
    video_rate = int(video_rate)

    frame_count =int( (to_time - from_time).seconds * frame_rate)
    print("frame_count", frame_count)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter("timestamp2.mp4", fourcc, video_rate, (width, height))

    for i in range(frame_count):
        img = np.zeros((height, width, 3), np.uint8)
        text = f"{from_time + datetime.timedelta(seconds=i/frame_rate)}"
        if i % 500 == 0:
            print(i,text)

        cv2.putText(img, f"{text}", (1, 1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        out.write(img)

    out.release()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--from_time", required=True, help="start_time")
    parser.add_argument("-t", "--to_time", required=True, help="end_time")
    parser.add_argument("-r", "--frame_rate", required=True, help="stamp fps")
    parser.add_argument("-v", "--video_rate", required=True, help="video fps")
    parser.add_argument("-s", "--shape", required=True, help="video shape")
    args = parser.parse_args()

    make_timestamp_video(args.from_time, args.to_time, args.frame_rate,
                          args.video_rate, args.shape)
