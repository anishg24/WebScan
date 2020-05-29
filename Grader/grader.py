#  Copyright (c) 2020. Anish Govind
#  https://github.com/anishg24

# https://www.pyimagesearch.com/2016/10/03/bubble-sheet-multiple-choice-scanner-and-test-grader-using-omr-python-and-opencv/
# Modified to fit my purposes

import cv2
import imutils
import numpy as np
from imutils import contours

ANSWER_KEY = {i: 1 for i in range(31)}

ANSWER_KEY[1] = 2
ANSWER_KEY[30] = 3


def grade(image, info):
    info = info[0]
    test_id, num_questions, num_choices, page_count = eval(info.data)
    qrl, qrt, qrw, qrh = info.rect

    warped = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)  # Every single contour in the page
    questionCnts = []  # Contours that will correspond with a singular bubble

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        aspect_ratio = w / float(h)
        # print(x, y)

        if w >= 10 and h >= 10 and 0.5 <= aspect_ratio <= 1.5 and x + y < qrl + qrt:  # Ensure that the contour is a bubble
            questionCnts.append(c)
            # cv2.drawContours(image, c, -1, (0, 255, 0), 3)

    if not len(
            questionCnts) == num_choices * num_questions:
        return image, None

    questionCnts = np.asarray(contours.sort_contours(questionCnts, method="top-to-bottom")[0])

    find_dist = lambda i: cv2.pointPolygonTest(i, (0, 0), True)
    first_bubble_index = max([i for i, _ in enumerate(list(map(find_dist, questionCnts)))])
    last_bubble_in_column = questionCnts[first_bubble_index - num_choices + 1]
    rightmost_point = tuple(np.amin(last_bubble_in_column, axis=0)[0])
    print(rightmost_point)
    x, y, _ = image.shape
    print(x, y)
    cv2.line(image, (int(x / 2), rightmost_point[0]), (int(x / 2), int(y)), (255, 0, 0), 5)
    cv2.circle(image, rightmost_point, 5, (0, 0, 255), -1)
    # cv2.drawContours(image, last_bubble_in_column, -1, (0, 255, 0), 3)
    cv2.imshow("t", image)
    cv2.waitKey(0)

    # correct = 0
    # # num_bubbles = 10
    # for (q, i) in enumerate(np.arange(0, len(questionCnts), num_choices)):
    #     cnts = contours.sort_contours(questionCnts[i:i + num_choices])[0]
    #     bubbled = None
    #
    #     for (j, c) in enumerate(cnts):
    #         mask = np.zeros(thresh.shape, dtype="uint8")
    #         cv2.drawContours(mask, [c], -1, 255, -1)
    #
    #         mask = cv2.bitwise_and(thresh, thresh, mask=mask)
    #         total = cv2.countNonZero(mask)
    #
    #         if total < 105:  # If the person left the bubble empty (which gives a value between 80-100) ignore it. As good as wrong.
    #             continue
    #
    #         # print(q, total)
    #
    #         if bubbled is None or total > bubbled[0]:
    #             bubbled = (total, j)
    #
    #     try:
    #         color = (0, 0, 255)
    #         k = ANSWER_KEY[q]
    #
    #         if k == bubbled[1]:
    #             color = (0, 255, 0)
    #             correct += 1
    #
    #         cv2.drawContours(image, [cnts[k]], -1, color, 3)
    #     except:
    #         pass
    #     # break
    #
    # score = (correct / len(ANSWER_KEY)) * 100
    # # print("[INFO] score: {:.2f}%".format(score))
    # # cv2.putText(image, "{:.2f}%".format(score), (10, 30),
    # #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    # return image, round(score, 2)
    return image, None
