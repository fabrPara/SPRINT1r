import warnings


def pytest_configure(config):
    """Configure pytest to ignore warnings during test execution."""
    config.addinivalue_line("filterwarnings", "ignore")
    warnings.filterwarnings("ignore")
