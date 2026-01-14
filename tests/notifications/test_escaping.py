import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../plugins/notifications/scripts'))

from platform_utils import escape_xml_content, escape_powershell_string


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


class TestEscapePowershellString:
    """Tests for PowerShell string escaping to prevent command injection."""

    def test_plain_text_unchanged(self):
        """Plain text without special characters should remain unchanged."""
        assert escape_powershell_string("Hello World") == "Hello World"

    def test_double_quotes_escaped(self):
        """Double quotes must be escaped with backtick to prevent string termination."""
        assert escape_powershell_string('Say "Hello"') == 'Say `"Hello`"'

    def test_backticks_escaped(self):
        """Backticks must be escaped since they are PowerShell's escape character."""
        assert escape_powershell_string("Hello `World") == "Hello ``World"

    def test_dollar_signs_escaped(self):
        """Dollar signs must be escaped to prevent variable expansion."""
        assert escape_powershell_string("$env:USERNAME") == "`$env:USERNAME"

    def test_subexpression_escaped(self):
        """$() subexpressions must be escaped to prevent command execution."""
        assert escape_powershell_string("$(Get-Process)") == "`$(Get-Process)"

    def test_combined_special_chars(self):
        """Test a string with multiple special characters."""
        input_text = 'User "$env:USER" ran `command` with $(calc.exe)'
        # Quotes get escaped too: " -> `"
        expected = 'User `"`$env:USER`" ran ``command`` with `$(calc.exe)'
        assert escape_powershell_string(input_text) == expected

    def test_unicode_preserved(self):
        """Unicode characters should be preserved unchanged."""
        assert escape_powershell_string("Hello 🎉 World") == "Hello 🎉 World"

    def test_empty_string(self):
        """Empty strings should be handled correctly."""
        assert escape_powershell_string("") == ""

    def test_only_special_chars(self):
        """Test strings containing only special characters."""
        assert escape_powershell_string('`$"') == '```$`"'

    def test_malicious_variable_injection(self):
        """Test that variable injection attempts are neutralized."""
        malicious = "Hello $env:COMPUTERNAME"
        escaped = escape_powershell_string(malicious)
        assert escaped == "Hello `$env:COMPUTERNAME"

    def test_malicious_command_injection(self):
        """Test that command injection via $() is neutralized."""
        malicious = 'test$(Remove-Item -Recurse C:\\)end'
        escaped = escape_powershell_string(malicious)
        assert escaped == 'test`$(Remove-Item -Recurse C:\\)end'

    def test_malicious_string_breakout(self):
        """Test that attempts to break out of the string are neutralized."""
        malicious = 'test"; Remove-Item -Recurse C:\\; "'
        escaped = escape_powershell_string(malicious)
        assert escaped == 'test`"; Remove-Item -Recurse C:\\; `"'

    def test_multiple_dollar_signs(self):
        """Test multiple consecutive dollar signs."""
        assert escape_powershell_string("$$$$") == "`$`$`$`$"

    def test_backtick_followed_by_dollar(self):
        """Test backtick followed by dollar sign - both must be escaped."""
        assert escape_powershell_string("`$") == "```$"

    def test_real_world_notification_text(self):
        """Test realistic notification text that might contain special chars."""
        text = 'Build complete! Cost: $1.50 for "my-project"'
        expected = 'Build complete! Cost: `$1.50 for `"my-project`"'
        assert escape_powershell_string(text) == expected
