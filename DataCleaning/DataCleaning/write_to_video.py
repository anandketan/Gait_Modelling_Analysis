import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2
import numpy as np

# Use Agg backend for canvas
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def vid_maker(cycles, data):
    # create OpenCV video writer
    video = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc('A','V','C','1'), 1, (mat.shape[0],mat.shape[1]))


    # loop over your images
    for i in range(len(img)):

        fig = plt.figure()
        plt.imshow(img[i], cmap=cm.Greys_r)

        # put pixel buffer in numpy array
        canvas = FigureCanvas(fig)
        canvas.draw()
        mat = np.array(canvas.renderer._renderer)
        mat = cv2.cvtColor(mat, cv2.COLOR_RGB2BGR)

        # write frame to video
        video.write(mat)

    # close video writer
    cv2.destroyAllWindows()
    video.release()