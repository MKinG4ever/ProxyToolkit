from Toolkit import Toolkit


def main():
    """
    proxyToolkit Module v1.0
    The MAIN function runs the proxyToolkit sample
    """

    # Create an Object
    tools = Toolkit()

    # Import JSON File
    json_all = tools.import_standard_json('sample.json')

    # Check the proxies from JSON File
    tools.check_the_proxies(json_all, timeout=5)


if __name__ == '__main__':
    main()
