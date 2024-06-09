import math
from typing import List, Optional

from pdfminer.layout import (
    LTAnno,
    LTChar,
    LTPage,
    LTTextBoxHorizontal,
    LTTextLineHorizontal,
)


class PdfTextStripper:

    def __init__(self):
        self.previous_text_position: Optional[dict] = None
        self.all_text_positions: List[str] = []
        self.current_line_text_positions: List[str] = []
        self.result: str = ''

    def process_page(self, page: LTPage):
        self.previous_text_position = None
        self.all_text_positions = []
        self.current_line_text_positions = []

        self.collect_all_glyphs(page)
        self.sort_all_text_positions_vertically()
        self.iterate_through_text_list()

        return self.result

    def collect_all_glyphs(self, page: LTPage):
        for element in page:
            if isinstance(element, LTTextBoxHorizontal):
                for text_line in element:
                    if isinstance(text_line, LTTextLineHorizontal):
                        for char in text_line:
                            if isinstance(char, LTChar):
                                self.all_text_positions.append({
                                    'x': char.x0,
                                    'y': page.height - char.y0,
                                    'text': char.get_text(),
                                    'width': char.width,
                                    'height': char.height
                                })

                            # When pdfminer finds a space or a new line, replace it by a pipe for a better visualization.
                            elif isinstance(char, LTAnno):
                                if self.all_text_positions:
                                    last_text_position = self.all_text_positions[-1]
                                    self.all_text_positions.append({
                                        'x': last_text_position['x'] + 0.01,  # + 0.01 To ensure it comes after the previous character when sorting horizontally
                                        'y': last_text_position['y'],
                                        'text': ' | ',
                                        'width': last_text_position['width'],
                                        'height': last_text_position['height']
                                    })

    def sort_all_text_positions_vertically(self):
        self.all_text_positions.sort(
            key=lambda tp: (
                tp["y"]
            )
        )

    def sort_current_line_text_positions_horizontally(self):
        self.current_line_text_positions.sort(
            key=lambda tp: (
                tp["x"]
            )
        )

    def iterate_through_text_list(self):
        for text_position in self.all_text_positions:
            number_of_new_lines = self.get_number_of_new_lines_from_previous_text_position(text_position)

            if number_of_new_lines == 0:
                self.current_line_text_positions.append(text_position)
            else:
                self.sort_current_line_text_positions_horizontally()
                self.write_text_position_list()
                self.create_new_empty_lines(number_of_new_lines)
                self.current_line_text_positions.append(text_position)

            self.previous_text_position = text_position

        if self.current_line_text_positions:
            self.sort_current_line_text_positions_horizontally()
            self.write_text_position_list()

    def write_text_position_list(self, ):
        self.write_line()
        self.current_line_text_positions.clear()

    def write_line(self, ):
        if self.current_line_text_positions:

            # Try to detect new lines again in this line.
            while self.current_line_text_positions:
                next_line_text_positions = []
                self.previous_text_position = None
                text_line = ''

                for text_position in self.current_line_text_positions:
                    number_of_new_lines = self.get_number_of_new_lines_from_previous_text_position(text_position)

                    if number_of_new_lines == 0:
                        text_line += text_position['text']
                        self.previous_text_position = text_position
                    else:
                        next_line_text_positions.append(text_position)

                self.result += text_line.strip()

                if next_line_text_positions:
                    self.result += "\n"

                self.current_line_text_positions = next_line_text_positions

    def create_new_empty_lines(self, number_of_new_lines):
        for _ in range(number_of_new_lines):
            self.result += '\n'

    def get_number_of_new_lines_from_previous_text_position(self, text_position):
        if self.previous_text_position is None:
            return 0

        text_y_position = text_position["y"]
        previous_text_height = self.previous_text_position["height"]
        previous_text_y_position = self.previous_text_position["y"]
        previous_text_y_end_position = previous_text_y_position + previous_text_height

        if text_y_position > previous_text_y_end_position:
            number_of_lines = math.floor((text_y_position - previous_text_y_position) / previous_text_height)
            number_of_lines = max(1, number_of_lines - 1)
            return number_of_lines
        else:
            return 0


# For quick debug. Run this from root folder: python src/pdftextstripper/PdfTextStripper.py
# if __name__ == '__main__':

#     from pdfminer.high_level import extract_pages
#     import os

#     test_file_path = os.path.join("tests", "assets", "sample.pdf")
#     test_file = open(test_file_path, 'rb')

#     doc = extract_pages(test_file)
#     page = next(doc)

#     stripper = PdfTextStripper()
#     output = stripper.process_page(page)

#     print(output)
