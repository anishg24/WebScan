#  Copyright (c) 2020. Anish Govind
#  https://github.com/anishg24

import os
import shutil
from string import ascii_lowercase

import cv2.aruco as aruco
import pyqrcodeng as qr
from cv2 import imwrite
from fpdf import FPDF  # Consider switching over to Jinja Template + PDFKit

# NOTE:
# All these calculations were done via trial and error. If you decide to change constants predefined then end result
# may not look the same!

# GOLDEN EXPRESSION
# self.bubble_coordinates[i].append((x, y, HALF_BUBBLE_SIZE / 2 + x + 0.25 * self.pdf.font_size - 0.3,
#                                                    HALF_BUBBLE_SIZE / 2 + y + 0.75 * self.pdf.font_size - 0.1))

# EXAMS_FOLDER = os.getcwd() + "/custom_exams/"
EXAMS_FOLDER = "../custom_exams/"
# TODO DELETE IN PRODUCTION
try:
    shutil.rmtree(os.path.join(os.getcwd(), "created_exams/") + "1")
    shutil.rmtree(os.path.join(os.getcwd(), "created_exams/") + "markers")
except FileNotFoundError:
    pass


class PaperFactory:
    def __init__(self, name, num_questions, num_choices=4):
        if num_choices > 10:
            return
        if len(name) > 20:
            return
        self.directory = os.path.join(os.getcwd(), "created_exams/")
        self.marker_directory = os.path.join(self.directory, "markers/")
        if not os.path.exists(self.marker_directory):
            try:
                os.mkdir(self.directory)
            except FileExistsError:
                pass
            os.mkdir(self.marker_directory)
        self.name = name
        self.num_questions = num_questions
        self.num_choices = num_choices
        self.bubble_size = 5
        self.marker_size = 24
        self.pdf = FPDF('P', 'mm', 'A4')
        self.pdf.set_auto_page_break(True, 270)
        self.page_count = 0
        self.pdf.set_font('Courier', '', self.bubble_size + 3)
        self._generate_markers()
        self._generate_id()
        self._add_question_page()
        self.generate_paper()
        self.save_pdf()

    def _generate_markers(self):
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        li = [aruco.drawMarker(aruco_dict, i + 1, self.marker_size) for i in range(5)]
        for i in range(len(li)):
            imwrite(f"{self.marker_directory}{i + 1}.png", li[i])

    def _generate_id(self):
        self.exam_id = len(os.listdir(self.directory))
        if not os.path.exists(self.directory + f"{self.exam_id}/"):
            os.mkdir(self.directory + f"{self.exam_id}/")
        self.ID = (self.exam_id, self.num_questions, self.num_choices,
                   self.page_count)  # QR Code effectively gives all the data across scripts
        self.qr_code = qr.create(str(self.ID))
        self.qr_code.png(self.directory + f"{self.exam_id}/qr.png", scale=3)

    def _add_markers_to_paper(self):
        # A4 is 210 x 297 mm
        # QR is size 24,
        # need 8 padding (vertically) = 32
        # need 10 padding (horizontally) = 34
        # Marker is size 24 as well
        # self.pdf.line(self.pdf.w/2, 0, self.pdf.w/2, self.pdf.h)  # Guideline
        # self.pdf.line(0, self.pdf.h/2, self.pdf.w, self.pdf.h/2)  # Guideline
        self.pdf.image(f"{self.marker_directory}1.png", 10, 8)  # top left
        self.pdf.image(f"{self.marker_directory}2.png", 186, 8)  # top right
        self.pdf.image(f"{self.marker_directory}3.png", 10, 265)  # bottom left
        self.pdf.image(f"{self.directory}{self.exam_id}/qr.png", 150, 235)  # bottom middle (was 235 before)

    def _add_question_page(self):
        self.pdf.add_page("P")
        self.page_count += 1
        self._add_markers_to_paper()

    def _create_bubble_coordinates(self, START_X, START_Y, num=None, choices=None, size=None):
        if not num:
            num = self.num_questions
        self.bubble_coordinates = [[] for _ in range(num)]

        if not choices:
            choices = self.num_choices

        if not size:
            size = self.bubble_size
        SPACE_FACTOR = size * (7 / 5)
        questions_until_max = 0
        column = 0
        next_page = False
        questions_per_page = 0
        right_side_limit = 184
        for r in range(num):
            y = START_Y + SPACE_FACTOR * (r + 1)
            if y > 260:
                column = r // questions_until_max
                y = START_Y + SPACE_FACTOR * (r - (questions_until_max * column) + 1)
            else:
                questions_until_max += 1
            for c in range(choices):
                sx = START_X + ((self.bubble_size + 4) * choices * column)
                x = sx + SPACE_FACTOR * (c + 1)
                if x > right_side_limit:
                    next_page = True
                    return self.bubble_coordinates, next_page, questions_per_page
                self.bubble_coordinates[r].append((x, y))
            questions_per_page += 1
        # self.pdf.line(right_side_limit, 0, right_side_limit, 300)  # Guideline to ensure that questions aren't outside scanned area
        return self.bubble_coordinates, next_page, questions_per_page

    def get_text_coordinates(self, coordinates):
        x, y = coordinates
        tx = self.bubble_size / 4 + x + 0.25 * self.pdf.font_size - 0.3
        ty = self.bubble_size / 4 + y + 0.75 * self.pdf.font_size - 0.1
        return tx, ty

    def _create_bubble(self, coordinates, text):
        initial_width = self.pdf.line_width
        self.pdf.set_line_width(.2)
        x, y = coordinates
        tx, ty = self.get_text_coordinates(coordinates)
        self.pdf.ellipse(x, y, self.bubble_size, self.bubble_size)
        self.pdf.set_text_color(125, 125, 125)
        self.pdf.text(tx, ty, text)
        self.pdf.set_line_width(initial_width)

    def _add_question(self, coordinates, question_offset=0):
        bubble_letters = ascii_lowercase[:self.num_choices]
        num = 0
        for num in range(len(coordinates)):
            if not len(coordinates[num]) == self.num_choices:
                break

            qx, qy = self.get_text_coordinates(coordinates[num][0])
            self.pdf.set_text_color(0, 0, 0)
            question_num = f"{num + 1 + question_offset}."
            self.pdf.text(qx - len(question_num) - 5, qy, question_num)
            for i in range(len(coordinates[num])):
                self._create_bubble(coordinates[num][i], bubble_letters[i])
        return num + question_offset

    def _add_questions_to_paper(self):
        # 176 x 255 mm
        # 10 mm horizontally x 8 mm vertically
        # Row 1 should be at 20, 26
        X, Y = self.box_end_coords
        _, more_page, questions_per_page = self._create_bubble_coordinates(X - 5, Y + 2)
        left_off = self._add_question(self.bubble_coordinates)
        counter = 0
        while more_page:
            counter += 1
            self._add_question_page()
            questions_done = self.num_questions - (counter * questions_per_page)
            page_coordinates, more_page, questions_per_page = self._create_bubble_coordinates(20, 12, questions_done)
            left_off = self._add_question(page_coordinates, left_off)
        print(self.page_count)
        # for num in range(len(self.bubble_coordinates)):
        #     if not len(self.bubble_coordinates[num]) == self.num_choices:
        #         continue
        #     _, _, qx, qy = self.bubble_coordinates[num][0]
        #     self.pdf.set_text_color(0, 0, 0)
        #     question_num = f"{num + 1}."
        #     self.pdf.text(qx - len(question_num) - 5, qy, question_num)
        #     for i in range(len(self.bubble_coordinates[num])):
        #         self.___create_bubble(self.bubble_coordinates[num][i], bubble_letters[i])

    def _add_uid_to_paper(self):
        X = 18
        Y = 12
        self.pdf.set_line_width(1)
        self._create_bubble_coordinates(X, Y, 10, 5)  # Rows and columns to be swapped
        for row in range(len(self.bubble_coordinates)):
            for col in range(len(self.bubble_coordinates[row])):
                self._create_bubble(self.bubble_coordinates[row][col], str(row))

        for sx, sy in self.bubble_coordinates[0]:
            self.pdf.set_line_width(.2)
            self.pdf.rect(sx, sy - 10, self.bubble_size, 8.5)

        initial_uid_bubbles = self.bubble_coordinates[0]
        ex, ey = self.bubble_coordinates[-1][0]
        uid_divider = initial_uid_bubbles[0][1] - 0.75
        self.pdf.line(initial_uid_bubbles[0][0] - 2, uid_divider, initial_uid_bubbles[-1][0] + self.bubble_size + 2,
                      uid_divider)
        self.pdf.set_line_width(1)
        self.pdf.rect(23, 8, 37, ey - 2)
        # self.pdf.rect(20, 8, 164, ey - 1)
        self.box_end_coords = (ex-2, ey - 1)

    def _add_fields_to_paper(self):
        x = self.pdf.w * 0.33

        def title(y, text):
            self.pdf.set_font("Arial", size=32)
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.text(x, y, text)

        def field(y, text, subtitle=None):
            self.pdf.set_font("Arial", size=16)
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.text(x, y, text)
            if subtitle:
                self.pdf.set_font("Arial", size=8)
                self.pdf.set_text_color(125, 125, 125)
                self.pdf.text(x, y + 3, subtitle)

        title(20, self.name)
        field(30, f"Name: {'_' * 16}")
        field(40, f"Date: __/__/__")
        field(50, f"Period: __")
        field(60, f"Class: {'_' * 16}", "(Optional)")
        field(70, f"Teacher: {'_' * 16}", "(Optional)")
        field(80, f"Score: __/__", "(Score to be filled by administrator)")

    def generate_paper(self):
        self._add_uid_to_paper()
        self._add_fields_to_paper()
        self.pdf.set_font('Courier', '', self.bubble_size + 3)
        self._add_markers_to_paper()
        self._add_questions_to_paper()

    def save_pdf(self):
        self.pdf.output(f"{self.directory}{self.exam_id}/paper.pdf")

    def get_directory(self):
        return self.directory


PaperFactory("Unit 10 MCQ", 380, 4)
print("CREATED TEST")
