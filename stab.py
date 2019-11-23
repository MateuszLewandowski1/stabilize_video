from vidgear.gears import VideoGear
import numpy as np
import cv2
import argparse

path_to_video = '/home/mateusz/Downloads/COMPONEER-Direct-Composite-Veneering-System---long-version-BMwoJ_G1Eu4.mp4'
path_to_tsunami = '/home/mateusz/5BiggestTsunamiCaughtOnCamera-Z-2khcTHIgs.mkv'


class Stabilize:

    """
    The following class stabilizes the video provided in the path parameter, possible to use a youtube URL
    """

    def __init__(self, path, watch_only_stabilized, y_tube=False):
        self.path = path
        self.watch_only_stabilized = watch_only_stabilized
        self.y_tube = y_tube

    def use_vidgear(self):

        stream_stab = VideoGear(source=self.path,
                                stabilize=True, y_tube=self.y_tube).start()  # To open any valid video stream with `stabilize` flag set to True.
        stream_org = VideoGear(source=self.path, y_tube=self.y_tube).start()  # open same stream without stabilization for comparison

        # infinite loop
        while True:

            frame_stab = stream_stab.read()
            # read stabilized frames
            # check if frame is None
            if frame_stab is None:
                # if True break the infinite loop
                break
            # read original frame
            frame_org = stream_org.read()

            # concatenate both frames
            output_frame = np.concatenate((frame_org, frame_stab), axis=1)

            # put text
            cv2.putText(output_frame, "Before", (10, output_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(output_frame, "After", (output_frame.shape[1] // 2 + 10, output_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

            if self.watch_only_stabilized:
                cv2.imshow("Stabilized Frame", frame_stab)
            # choose to see both original and stabilized frame
            else:
                cv2.imshow("output Frame", output_frame)
            # Show output window

            key = cv2.waitKey(1) & 0xFF
            # check for 'q' key-press
            if key == ord("q"):
                # if 'q' key-pressed break out
                break

        cv2.destroyAllWindows()
        # close output window
        stream_org.stop()
        stream_stab.stop()

    def __call__(self):
        self.use_vidgear()


if __name__ == '__main__':
    path_to_tsunami = '/home/mateusz/5BiggestTsunamiCaughtOnCamera-Z-2khcTHIgs.mkv'
    parser = argparse.ArgumentParser(description="watch only stabilised video or both primary and stabilized video")
    parser.add_argument('one_video', type=int, help='watch only stabilised or both')
    args = parser.parse_args()
    stab = Stabilize(path_to_tsunami, args.one_video)
    stab()
