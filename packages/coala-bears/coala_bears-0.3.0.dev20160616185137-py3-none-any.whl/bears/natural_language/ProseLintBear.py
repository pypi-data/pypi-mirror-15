from coalib.bearlib.abstractions.Linter import linter


@linter(executable='proselint',
        output_format='regex',
        output_regex=r'.+?:(?P<line>\d+):(?P<column>\d+): \S* (?P<message>.+)')
class ProseLintBear:
    """
    Lints the file using ``proselint``.
    """
    LANGUAGES = {"Natural Language"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
