import cv2
import sys

import os
import ntpath


class VideoParser:
    def __init__(self, video_path):
        self.pathIn = video_path
        self.pathOut = 'Frames/'
        self.count = 0
        self.vidcap = cv2.VideoCapture(self.pathIn)
        self.success, self.image = self.vidcap.read()  # check if file exists
        self.video_formats = ["mp4", "mov", "wmv", "avi", "mpeg"]
        self.fileName = str(ntpath.basename(video_path))
        self.framesFolder = os.path.join(self.pathOut, self.fileName, "frames")


    def create_directories(self):
        # Creates temporary output directories for audio and frames
        try:
            os.mkdir(os.path.join(self.pathOut, self.fileName))
            os.mkdir(self.framesFolder)
        except FileExistsError:
            print("File with this name has already been parsed.")

    def parse_video(self):
        # Separates video into frames
        while self.success:
            self.vidcap.set(cv2.CAP_PROP_POS_MSEC, (self.count * 1000))
            self.success, self.image = self.vidcap.read()
            if self.success:
                # save frame as JPEG file
                cv2.imwrite(os.path.join(self.framesFolder, "frame%d.jpg" % self.count), self.image)
            # count indicates number of frames per second:
            # count + 1 is 1 frame per second,
            # count + 2 is frame per two seconds
            self.count = self.count + 1



    def parse(self):
        # Checks if the file is a video file and invokes frame and audio extraction
        ext = self.pathIn.split(".")[-1]
        if ext not in self.video_formats:
            print(f"Wrong file extension: {ext}", file=sys.stderr)
        else:
            self.create_directories()
            self.parse_video()



if __name__ == "__main__":
    # python extract_frames.py pathIn
    pathInput = sys.argv[1]

    parser = VideoParser(video_path=pathInput)
    parser.parse()