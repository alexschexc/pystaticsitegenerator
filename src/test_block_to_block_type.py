import unittest
from block_to_block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("A normal paragraph."), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        self.assertEqual(block_to_block_type("First line\nSecond line"), BlockType.PARAGRAPH)

    def test_heading_levels_one_through_six(self):
        for level in range(1, 7):
            with self.subTest(level=level):
                self.assertEqual(block_to_block_type("#" * level + " Heading"), BlockType.HEADING)

    def test_seven_hashes_are_not_a_heading(self):
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    def test_heading_requires_space(self):
        for block in ("#Heading", "##Heading", "#\tHeading"):
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_multiline_code_block(self):
        fence = "`" * 3
        block = fence + "\nprint('hello')\nprint('world')\n" + fence
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_contents_do_not_change_block_type(self):
        fence = "`" * 3
        block = fence + "\n# heading\n> quote\n- item\n1. item\n" + fence
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_requires_both_fences(self):
        fence = "`" * 3
        for block in (fence + "\nunfinished", "unfinished\n" + fence):
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_requires_newline_after_opening_fence(self):
        fence = "`" * 3
        self.assertEqual(block_to_block_type(fence + "code" + fence), BlockType.PARAGRAPH)

    def test_inline_code_is_a_paragraph(self):
        self.assertEqual(block_to_block_type("`inline code`"), BlockType.PARAGRAPH)

    def test_quote_with_and_without_spaces(self):
        self.assertEqual(block_to_block_type("> first\n>second\n> third"), BlockType.QUOTE)

    def test_single_line_quote(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)

    def test_every_quote_line_must_have_marker(self):
        self.assertEqual(block_to_block_type("> first\nnot a quote"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- first\n- second\n- third"), BlockType.UNORDERED_LIST)

    def test_single_unordered_item(self):
        self.assertEqual(block_to_block_type("- first"), BlockType.UNORDERED_LIST)

    def test_every_unordered_line_must_have_marker(self):
        for block in ("- first\nplain text", "- first\n-second", "- first\n* second"):
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_requires_space(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_single_ordered_item(self):
        self.assertEqual(block_to_block_type("1. first"), BlockType.ORDERED_LIST)

    def test_ordered_list_supports_two_digit_numbers(self):
        block = "\n".join(f"{number}. item" for number in range(1, 12))
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_must_start_at_one(self):
        self.assertEqual(block_to_block_type("2. first\n3. second"), BlockType.PARAGRAPH)

    def test_ordered_list_must_increment_by_one(self):
        for block in ("1. first\n3. second", "1. first\n1. second", "1. first\n2. second\n2. third"):
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_requires_period_and_space(self):
        for block in ("1.first", "1 first", "1.\tfirst", "1. first\n2.second"):
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_every_ordered_line_must_have_marker(self):
        self.assertEqual(block_to_block_type("1. first\nplain text"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
