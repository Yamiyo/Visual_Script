import cv2
import math
import numpy as np
import base64
from GeometrA.src.finder.rectangle import Rectangle

class CV2Img:
    def __init__(self, source=None):
        self._source = source
        self._roi = None

        if source is not None:
            self._update_source_info()

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
        self._update_source_info()

    @property
    def shape(self):
        return self.source.shape

    def _update_source_info(self):
        self.rows, self.cols = self.source.shape[:2]
        self._roi = Rectangle(0, 0, self.rows, self.cols)

        self.mean, self.stddev = cv2.meanStdDev(self.source)

    def load_file(self, file_path, way = None):
        # The 1 means return 3-channel color image (without alpha channel)
        #  1 : cv2.IMREAD_COLOR: Loads a color image.Any transparency of image will be neglected.It is the default flag.
        #  0 : cv2.IMREAD_GRAYSCALE: Loads image in grayscale mode
        # -1 : cv2.IMREAD_UNCHANGED: Loads image as such including alpha channel
        img = cv2.imread(file_path, way)

        if img is None:
            raise Exception("Can't load image from {}".format(file_path))
        else:
            self.source = img

        return self

    def load_binary(self, binary):
        buf = np.fromstring(binary, dtype='uint8')

        # The 1 means return 3-channel color image (without alpha channel)
        self.source = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)

        return self

    def load_base64(self, encoded_string):
        self.load_binary(base64.b64decode(encoded_string))
        return self

    def load_PILimage(self, image):
        #self.source = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
        self.source = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2GRAY)
        return self

    def is_same_color(self):
        return np.sum(self.stddev[0:4]) <= 1e-5

    def is_black(self):
        return (np.sum(self.mean[0:4]) <= 1e-5) and self.is_same_color()

    def gray(self):
        new_img = CV2Img()
        new_img.source = cv2.cvtColor(self.source, cv2.COLOR_RGB2GRAY)

        return new_img

    def invert(self):
        return CV2Img(cv2.bitwise_not(self.source))

    def crop(self, roi):
        new_img = CV2Img()
        new_img.source = self.source[roi.y:roi.y + roi.h, roi.x:roi.x + roi.w]

        return new_img

    def resize(self, factor):
        h, w = self.source.shape[:2]
        new_size = (int(w * factor), int(h * factor))
        new_img = CV2Img()
        new_img.source = cv2.resize(self.source, new_size, interpolation=cv2.INTER_NEAREST)

        return new_img

    def copy(self):
        new_img = CV2Img()
        new_img.source = np.copy(self.source)

        return new_img

    def show(self, title=None):
        if not title:
            title = "Show Image"
        cv2.imshow(title, self.source)
        cv2.waitKey(0)

    def canny(self, threshold1=50, threshold2=200):
        return CV2Img(cv2.Canny(self.source, threshold1, threshold2))


    def draw_result_range(self, find_result, color=(0, 0, 255)):
        cv2.rectangle(self.source,
                      (find_result.x, find_result.y),
                      (find_result.x + find_result.w, find_result.y + find_result.h),
                      color, 10)

    def draw_rectangle(self, x1, y1, x2, y2):
        cv2.rectangle(self.source, (x1, y1),(x2, y2), (0, 0, 255), 10)

    def draw_circle(self, x,y):
        cv2.circle(self.source, (x, y), 50, (0, 0, 255), 10)

    def draw_line(self,x1,y1,x2,y2):
        cv2.line(self.source, (x1, y1), (x2, y2), (0, 0, 255), 10)

    def coordinate(self, find_result):
        coordinate_x = find_result.x + find_result.w/2
        coordinate_y = find_result.y + find_result.h/2
        return coordinate_x,coordinate_y

    def draw_Arrow(self,fromX, fromY, toX, toY):
        angle = math.atan2(fromY - toY, fromX - toX) * 180 / math.pi
        angle1 = (angle + 30) * math.pi / 180
        angle2 = (angle - 30) * math.pi / 180
        topX = 100 * math.cos(angle1)
        topY = 100 * math.sin(angle1)
        botX = 100 * math.cos(angle2)
        botY = 100 * math.sin(angle2)

        cv2.line(self.source, (int(fromX), int(fromY)), (int(toX), int(toY)), (0, 0, 255), 10)
        print(toX, toY)

        arrowX = toX + topX
        arrowY = toY + topY
        cv2.line(self.source, (int(toX), int(toY)), (int(arrowX), int(arrowY)), (0, 0, 255), 10)
        print(arrowX, arrowY)

        arrowX = toX + botX
        arrowY = toY + botY
        cv2.line(self.source, (int(toX), int(toY)), (int(arrowX), int(arrowY)), (0, 0, 255), 10)
        print(arrowX, arrowY)

    def save(self, path):
        cv2.imwrite(path, self.source)

    #############################################################################
    #
    # Operator
    #
    #############################################################################
    def __lt__(self, other):
        shape = self.source.shape
        other_shape = other.source.shape

        return shape[0] < other_shape[0] or shape[1] < other_shape[1]

    def __gt__(self, other):
        shape = self.source.shape
        other_shape = other.source.shape

        return shape[0] > other_shape[0] or shape[1] > other_shape[1]

    def __eq__(self, other):
        return np.array_equal(self.source, other.source)
