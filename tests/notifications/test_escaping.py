import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../plugins/notifications/scripts'))

from platform_utils import escape_applescript_string, escape_xml_content


class TestEscapeApplescriptString:
    def test_plain_text_unchanged(self):
        assert escape_applescript_string("Hello World") == "Hello World"

    def test_double_quotes_escaped(self):
        assert escape_applescript_string('Say "Hello"') == 'Say \\"Hello\\"'

    def test_backslashes_escaped(self):
        assert escape_applescript_string("path\\to\\file") == "path\\\\to\\\\file"

    def test_newlines_escaped(self):
        assert escape_applescript_string("line1\nline2") == "line1\\nline2"

    def test_combined_special_chars(self):
        input_text = 'He said "Hello\\World"\nGoodbye'
        expected = 'He said \\"Hello\\\\World\\"\\nGoodbye'
        assert escape_applescript_string(input_text) == expected

    def test_unicode_preserved(self):
        assert escape_applescript_string("Hello 🎉 World") == "Hello 🎉 World"


class TestEscapeXmlContent:
    def test_plain_text_unchanged(self):
        assert escape_xml_content("Hello World") == "Hello World"

    def test_ampersand_escaped(self):
        assert escape_xml_content("Tom & Jerry") == "Tom &amp; Jerry"

    def test_less_than_escaped(self):
        assert escape_xml_content("a < b") == "a &lt; b"

    def test_greater_than_escaped(self):
        assert escape_xml_content("a > b") == "a &gt; b"

    def test_double_quotes_escaped(self):
        assert escape_xml_content('"quoted"') == "&quot;quoted&quot;"

    def test_single_quotes_escaped(self):
        assert escape_xml_content("it's") == "it&apos;s"

    def test_combined_special_chars(self):
        input_text = '<script>alert("XSS & more")</script>'
        expected = "&lt;script&gt;alert(&quot;XSS &amp; more&quot;)&lt;/script&gt;"
        assert escape_xml_content(input_text) == expected

    def test_unicode_preserved(self):
        assert escape_xml_content("Hello 🎉") == "Hello 🎉"

    def test_already_escaped_gets_double_escaped(self):
        # If someone passes "&amp;" it should become "&amp;amp;"
        assert escape_xml_content("&amp;") == "&amp;amp;"
