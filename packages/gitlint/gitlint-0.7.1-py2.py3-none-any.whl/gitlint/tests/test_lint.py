try:
    # python 2.x
    from StringIO import StringIO
except ImportError:
    # python 3.x
    from io import StringIO

from mock import patch

from gitlint.tests.base import BaseTestCase
from gitlint.lint import GitLinter
from gitlint.rules import RuleViolation
from gitlint.config import LintConfig


class RuleOptionTests(BaseTestCase):
    def test_lint_sample1(self):
        linter = GitLinter(LintConfig())
        gitcontext = self.gitcontext(self.get_sample("commit_message/sample1"))
        violations = linter.lint(gitcontext.commits[-1], gitcontext)
        expected_errors = [RuleViolation("T3", "Title has trailing punctuation (.)",
                                         "Commit title containing 'WIP', as well as trailing punctuation.", 1),
                           RuleViolation("T5", "Title contains the word 'WIP' (case-insensitive)",
                                         "Commit title containing 'WIP', as well as trailing punctuation.", 1),
                           RuleViolation("B4", "Second line is not empty", "This line should be empty", 2),
                           RuleViolation("B1", "Line exceeds max length (135>80)",
                                         "This is the first line of the commit message body and it is meant to test " +
                                         "a line that exceeds the maximum line length of 80 characters.", 3),
                           RuleViolation("B2", "Line has trailing whitespace", "This line has a trailing space. ", 4),
                           RuleViolation("B2", "Line has trailing whitespace", "This line has a trailing tab.\t", 5),
                           RuleViolation("B3", "Line contains hard tab characters (\\t)",
                                         "This line has a trailing tab.\t", 5)]

        self.assertListEqual(violations, expected_errors)

    def test_lint_sample2(self):
        linter = GitLinter(LintConfig())
        gitcontext = self.gitcontext(self.get_sample("commit_message/sample2"))
        violations = linter.lint(gitcontext.commits[-1], gitcontext)
        expected = [RuleViolation("T5", "Title contains the word 'WIP' (case-insensitive)",
                                  "Just a title containing WIP", 1),
                    RuleViolation("B6", "Body message is missing", None, 3)]

        self.assertListEqual(violations, expected)

    def test_lint_sample3(self):
        linter = GitLinter(LintConfig())
        gitcontext = self.gitcontext(self.get_sample("commit_message/sample3"))
        violations = linter.lint(gitcontext.commits[-1], gitcontext)

        title = " Commit title containing 'WIP', \tleading and trailing whitespace and longer than 72 characters."
        expected = [RuleViolation("T1", "Title exceeds max length (95>72)", title, 1),
                    RuleViolation("T3", "Title has trailing punctuation (.)", title, 1),
                    RuleViolation("T4", "Title contains hard tab characters (\\t)", title, 1),
                    RuleViolation("T5", "Title contains the word 'WIP' (case-insensitive)", title, 1),
                    RuleViolation("T6", "Title has leading whitespace", title, 1),
                    RuleViolation("B4", "Second line is not empty", "This line should be empty", 2),
                    RuleViolation("B1", "Line exceeds max length (101>80)",
                                  "This is the first line is meant to test a line that exceeds the maximum line " +
                                  "length of 80 characters.", 3),
                    RuleViolation("B2", "Line has trailing whitespace",
                                  "This line has a trailing space. ", 4),
                    RuleViolation("B2", "Line has trailing whitespace", "This line has a trailing tab.\t",
                                  5),
                    RuleViolation("B3", "Line contains hard tab characters (\\t)",
                                  "This line has a trailing tab.\t", 5)]

        self.assertListEqual(violations, expected)

    def test_lint_sample4(self):
        gitcontext = self.gitcontext(self.get_sample("commit_message/sample4"))
        lintconfig = LintConfig()
        lintconfig.apply_config_from_commit(gitcontext.commits[-1])
        linter = GitLinter(lintconfig)
        violations = linter.lint(gitcontext.commits[-1], gitcontext)
        # expect no violations because sample4 has a 'gitlint: disable line'
        expected = []
        self.assertListEqual(violations, expected)

    def test_lint_sample5(self):
        gitcontext = self.gitcontext(self.get_sample("commit_message/sample5"))
        lintconfig = LintConfig()
        lintconfig.apply_config_from_commit(gitcontext.commits[-1])
        linter = GitLinter(lintconfig)
        violations = linter.lint(gitcontext.commits[-1], gitcontext)
        title = " Commit title containing 'WIP', \tleading and trailing whitespace and longer than 72 characters."
        # expect only certain violations because sample5 has a 'gitlint: T3,'
        expected = [RuleViolation("T1", "Title exceeds max length (95>72)", title, 1),
                    RuleViolation("T4", "Title contains hard tab characters (\\t)", title, 1),
                    RuleViolation("T5", "Title contains the word 'WIP' (case-insensitive)", title, 1),
                    RuleViolation("B4", "Second line is not empty", "This line should be empty", 2),
                    RuleViolation("B2", "Line has trailing whitespace",
                                  "This line has a trailing space. ", 4),
                    RuleViolation("B2", "Line has trailing whitespace", "This line has a trailing tab.\t",
                                  5),
                    RuleViolation("B3", "Line contains hard tab characters (\\t)",
                                  "This line has a trailing tab.\t", 5)]
        self.assertListEqual(violations, expected)

    def test_lint_merge_commit(self):
        gitcontext = self.gitcontext(self.get_sample("commit_message/sample6"))  # Sample 6 is a merge commit
        lintconfig = LintConfig()
        linter = GitLinter(lintconfig)
        violations = linter.lint(gitcontext.commits[-1], gitcontext)
        # Even though there are a number of violations in the commit message, they are ignored because
        # we are dealing with a merge commit
        self.assertListEqual(violations, [])

        # Check that we do see violations if we disable 'ignore-merge-commits'
        lintconfig.ignore_merge_commits = False
        linter = GitLinter(lintconfig)
        violations = linter.lint(gitcontext.commits[-1], gitcontext)
        self.assertTrue(len(violations) > 0)

    def test_print_violations(self):
        violations = [RuleViolation("RULE_ID_1", "Error Message 1", "Violating Content 1", 1),
                      RuleViolation("RULE_ID_2", "Error Message 2", "Violating Content 2", 2)]
        linter = GitLinter(LintConfig())

        # test output with increasing verbosity
        with patch('gitlint.display.stderr', new=StringIO()) as stderr:
            linter.config.verbosity = 0
            linter.print_violations(violations)
            self.assertEqual("", stderr.getvalue())

        with patch('gitlint.display.stderr', new=StringIO()) as stderr:
            linter.config.verbosity = 1
            linter.print_violations(violations)
            expected = "1: RULE_ID_1\n2: RULE_ID_2\n"
            self.assertEqual(expected, stderr.getvalue())

        with patch('gitlint.display.stderr', new=StringIO()) as stderr:
            linter.config.verbosity = 2
            linter.print_violations(violations)
            expected = "1: RULE_ID_1 Error Message 1\n2: RULE_ID_2 Error Message 2\n"
            self.assertEqual(expected, stderr.getvalue())

        with patch('gitlint.display.stderr', new=StringIO()) as stderr:
            linter.config.verbosity = 3
            linter.print_violations(violations)
            expected = "1: RULE_ID_1 Error Message 1: \"Violating Content 1\"\n" + \
                       "2: RULE_ID_2 Error Message 2: \"Violating Content 2\"\n"
            self.assertEqual(expected, stderr.getvalue())
