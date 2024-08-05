from Toolkit import Toolkit
from Geonode import Geonode


def main():
    """
    proxyToolkit Module v1.1
    The MAIN function runs the proxyToolkit sample
    """
    # Test: Toolkit Version
    toolkit_version()

    # Test: Geonode Version
    geonode_version()


def toolkit_version():
    # Create an Object from Toolkit class
    tools = Toolkit()

    # Import JSON File
    json_all = tools.import_standard_json('sample.json')

    # Check the proxies from JSON File
    tools.check_the_proxies(json_all, timeout=5)


def geonode_version():
    # Create an Object from Geonode class (child of Toolkit)
    tools = Geonode()

    # Sample List | Toolkit
    # json_file = tools.import_standard_json('sample.json')

    # Iran Proxy List | Geonode
    # api_fetch = tools.fetch_api(tools.generate_url())
    api_data = tools.read_api('api_file.json')
    api_list = tools.export_proxies(api_data)

    # tools.check_the_proxies(proxy_list=json_file, timeout=5)
    tools.check_the_proxies(proxy_list=api_list, timeout=5)

    # Final presentation
    print(tools)


if __name__ == '__main__':
    main()
