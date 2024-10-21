def pytest_addoption(parser):
    parser.addoption(
        "--token", help="User's token"
    )