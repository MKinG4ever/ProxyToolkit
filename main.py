import time
from Geonode import Geonode
from Toolkit import Toolkit


def main():
    """
    Main function for the proxyToolkit Module v1.2
    This function demonstrates the usage of proxyToolkit by calling example functions
    and fetching proxies sorted by response time in ascending order.
    """

    # Toolkit Guide
    # toolkit_sample()

    # GeoNode Guide
    # geo_sample()

    # Function: Get top pages
    get_pages(pages=5, sort_by='responseTime', sort_type='asc')


def toolkit_sample():
    """
    Demonstrates how to use the Toolkit class.


    OPTIONS:

    - Importing Proxies
    toolkit.import_standard_txt()
    toolkit.import_standard_json()

    - Check the Proxies
    toolkit.check_the_proxies()

    - Help
    toolkit.help()
    """

    toolkit = Toolkit()
    toolkit.echo('[+] Toolkit Guide:\n', color='green')
    time.sleep(1)

    # Import proxies from a standard json file with 'ip', 'port' and 'protocol' as Key
    file = toolkit.import_standard_json(path='sample.json')

    # Check the proxies
    toolkit.check_the_proxies(proxy_list=file, timeout=3)

    # See if any live proxy is existed
    print(toolkit.proxies)

    # Help
    # toolkit.help()


def geo_sample():
    """
    Demonstrates how to use the Geonode class.


    OPTIONS:

    - Save as JSON
    geonode.save_as_json()

    - Generate Url and Fetch Proxies / Read Proxies from GeoNode Exported JSON File
    geonode.generate_url()
    geonode.fetch_api()
    geonode.read_api()

    - Export Fetch or Read Proxies from a dict / Cut Proxies from a list
    geonode.export_proxies()
    geonode.cut_proxies()

    - Help
    geonode.help()
    """

    geonode = Geonode()
    geonode.echo('[+] GeoNode Guide:\n', color='green')
    time.sleep(1)

    # Generate url for GeoNode API
    url = geonode.generate_url()

    # Fetch proxies online with url
    data = geonode.fetch_api(url)

    # Export proxies from data
    proxy_list = geonode.export_proxies(data)

    # Check the proxies
    geonode.check_the_proxies(proxy_list)

    # See if any live proxy is existed
    print(geonode.proxies)

    # Help
    # geonode.help()


def get_pages(pages=1, *args, **kwargs):
    """
    Fetches and checks proxies from multiple pages of the GeoNode API.

    Args:
        pages (int): The number of pages to fetch proxies from. Default is 1.
        *args: Additional positional arguments passed to the URL generator.
        **kwargs: Additional keyword arguments passed to the URL generator.

    Workflow:
    - Initializes the Geonode tool.
    - Iterates through the specified number of pages.
    - For each page:
        - Generates a URL for fetching proxies.
        - Fetches the proxies from the API.
        - Exports the proxies and saves them as JSON files.
    - Checks all the proxies for availability.
    - Saves the live proxies to a separate JSON file if any are available.
    """

    tool = Geonode()  # Initialize the Geonode tool
    print(tool)

    _list = []  # List to store all proxies

    for page in range(1, pages + 1):
        print(f'\n[Page: {page}]')

        # Generate URL for the current page with optional arguments
        addr = tool.generate_url(page=page, *args, **kwargs)

        # Fetch proxies from the generated URL
        data = tool.fetch_api(addr)

        # Export proxies from the fetched data
        proxies = tool.export_proxies(data)
        _list.extend(proxies)  # Append the proxies to the list

        # Save the proxies for the current page as a JSON file
        tool.save_as_json(proxies, f'./pages/proxies_page{page}.json')

    print("- All proxies saved as JSON files;\n- Begin checking proxies")

    # Check all collected proxies for availability
    tool.check_the_proxies(proxy_list=_list, timeout=2)

    # Print the live proxies
    print(tool.proxies)

    # Save live proxies to a separate JSON file if any exist
    lives = tool.cut_proxies(tool.proxies)
    if len(lives):
        tool.save_as_json(lives, './lives_proxies.json')


if __name__ == '__main__':
    main()
