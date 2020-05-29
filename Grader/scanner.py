#  Copyright (c) 2020. Anish Govind
#  https://github.com/anishg24
from collections import Counter

import cv2
import cv2.aruco as aruco
import numpy as np
import pyzbar.pyzbar as pyzbar
from imutils import grab_contours
from imutils.perspective import four_point_transform

from api.python_scripts.grader import grade


def binarize(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[
        1]  # Increasing the 2nd argument means lighter colors can be classified as black
    return thresh


def get_exam_info(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 1)
    edged = cv2.Canny(blurred, 75, 200)
    # find contours in the edge map, then initialize
    # the contour that corresponds to the document
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = grab_contours(cnts)
    docCnt = None
    f_height, f_width, _ = frame.shape
    # ensure that at least one contour was found
    if len(cnts) > 0:
        # sort the contours according to their size in
        # descending order
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        # loop over the sorted contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            mean = np.mean(approx, axis=0)[0]
            # if our approximated contour has four points,
            # then we can assume we have found the paper
            if len(approx) == 4 and mean[1] < f_height * 0.25:
                docCnt = approx
                return four_point_transform(frame, docCnt.reshape(4, 2)), docCnt.reshape(4, 2)
        return frame, None


def get_exam(marker_points, marker_id, frame):
    get_point = lambda i: marker_points[np.where(marker_id == i)[0][0]][0]
    m1 = get_point(1)
    m2 = get_point(2)
    m3 = get_point(3)
    x = 20  # Space to add to include QR Code, since we "guess" where it is mathematically, and don't find it's location yet.
    tl = m1[np.argmin(np.diff(m1, axis=1))]  # Top left
    tr = m2[np.argmin(np.sum(m2, axis=1))]  # Top right
    bl = m3[np.argmax(np.sum(m3, axis=1))]  # Bottom left
    br = np.array([tr[0] + x, bl[1] + x])  # Bottom right where the QR code exists.
    tl[0] -= x
    tl[1] -= x
    tr[1] -= x
    docCorners = [bl, tl, tr, br]
    warped = four_point_transform(frame, np.array(docCorners))

    return warped


class Scanner:
    def __init__(self):
        self.qr_decoder = cv2.QRCodeDetector()
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.parameters = aruco.DetectorParameters_create()

    def process_frame(self, frame):
        thresh = binarize(frame)

        corners, ids, _ = aruco.detectMarkers(thresh, self.aruco_dict, parameters=self.parameters)
        warped = None
        processed = False
        score = None

        if len(corners) >= 3:
            processed = False
            transformed = get_exam(corners, ids, frame)
            uid_box, points = get_exam_info(transformed)
            if points is not None:
                cx, cy = np.amax(points, axis=0)
                transformed = transformed[cy - 4:, :]
                decodedObjects = pyzbar.decode(binarize(transformed))
                if decodedObjects:
                    # print(decodedObjects)
                    try:
                        warped, score = grade(transformed, decodedObjects)
                        processed = True
                    except IndexError:
                        pass
            else:
                warped = aruco.drawDetectedMarkers(frame, corners)
        else:
            warped = aruco.drawDetectedMarkers(frame, corners)
            processed = False
            uid_box = frame
            transformed = frame

        return frame, warped, processed, score, uid_box, transformed


scanner = Scanner()
cap = cv2.VideoCapture(0)
scores_counter = Counter()
while True:
    # read next frame from VideoCapture
    ret, f = cap.read()
    if f is not None:
        fr, w, p, s, t, tr = scanner.process_frame(frame=f)
        if s:
            scores_counter[s] += 1
        if scores_counter and scores_counter.most_common()[0][1] >= 5:
            print(s)
            break
        try:
            cv2.imshow("a", w)
        except:
            pass
        # cv2.imshow("t", tr)
    # exit if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
