# Standard Python modules
from dataclasses import dataclass
from py.xml import html  # pylint: disable=(import-error, no-name-in-module, wrong-import-order)

# First party external modules
from testing.utilities import Utilities


@dataclass
class PytestTestData:
    only_linting: bool = False
    report_line_id: int = 0


pytest_test_data = PytestTestData()


def pytest_addoption(parser):
    parser.addoption('--only-linting',
                     action='store_true',
                     default=False,
                     help='Only run linting checks')


def pytest_collection_modifyitems(session, config, items):  # pylint: disable=(unused-argument)
    if config.getoption('--only-linting'):
        pytest_test_data.only_linting = True
        lint_items = []
        for linter in ['pylint', 'flake8', 'mypy']:
            if config.getoption(f'--{linter}'):
                lint_items.extend([item for item in items if item.get_closest_marker(linter)])
        items[:] = lint_items


def pytest_configure(config):
    # Additional environment information's to HTML test report
    config._metadata['WSL (Windows Subsystem for Linux)'] = Utilities.wsl_info()  # pylint: disable=(protected-access)

    if config.getoption('--only-linting'):
        plugin = config.pluginmanager.getplugin('mypy')
        plugin.mypy_argv.append('--config-file=testing/mypy.ini')
        return


def pytest_html_report_title(report):
    report.title = f'Report File: {report.title}'


def pytest_html_results_table_header(cells):
    cells.insert(0, html.th('ID', class_='sortable'))  # Add test ID number header
    # if pytest_test_data.only_linting:
    #     cells[1] = html.th('File::linter', class_='sortable')
    cells.pop()  # Remove "Links" header


def pytest_html_results_table_row(report, cells):
    pytest_test_data.report_line_id += 1
    id_string = str(pytest_test_data.report_line_id).rjust(8)  # rjust necessary for correct sorting
    cells.insert(0, html.th(id_string))

    _ = report  # To avoid PYLINT 'Unused argument'
    cells.pop()  # Remove "Links" column cell
