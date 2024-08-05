from Toolkit import requests, json, Art, Toolkit


class Geonode(Toolkit):
    """
    GeoNode(proxyToolkit): A class for interacting with GeoNode services

    This class provides methods to create API URLs, fetch proxy data,
    and handle various tasks related to GeoNode proxy services.
    Thanks to "geonode.com" for providing free proxies.

    Visit GeoNode Website for more details.

    GeoNode Resources:
    - Home: https://geonode.com/
    - Free Proxies: https://geonode.com/free-proxy-list
    - Documentation: https://docs.geonode.com/


    Author: NightFox
    Timestamp: 1722561426.3625014
    Powered-by: Python Programing language and GeoNode Technologies
    """

    def __init__(self):
        """
        Initialize the Geonode class.
        This sets up the default logo and any necessary initial configuration.

        + [4] GeoNode Module Abilities (API Service):
            - 1[/4]. Create API url for GeoNode Free-Proxy-List service.

            - 2[/4]. Providing API Data. (Original Type of GeoNode API Data)
                2-1. Get API Data from 'Web' with GET/POST request with python.
                2-2. Read API Data from 'File'. (that may create manually or user did 'save as' it with browser)

            - 3[/4]. Convert API Data to Pure proxy list. (Original GeoNode to Standard List)

            - 4[/4]. Save(any data, list or dict) as json.
        """
        super().__init__()
        Art.default_logo = Art.geonode_logo  # New Art for "check_the_proxies()" from Toolkit class

    def __repr__(self):
        """Return a representation of the GeoNode(Toolkit) instance."""
        return f"{Art.geonode_repr_logo}GeoNode:ProxyToolkit {self.version} | ID: {id(self)}"  # New Art

    @property
    def version(self):
        """Return the version of the GeoNode:ProxyToolkit."""
        return "v2.1"

    def save_as_json(self, data: list or dict, path: str) -> None:
        """
        Save data as a JSON file.

        :param data: Data to be saved, either as a list or a dictionary.
        :param path: Path where the JSON file should be saved.
        :return: None
        """
        self.echo(f'Writing JSON file ({path}):', end=' ')

        try:
            with open(file=path, mode='w', encoding='utf-8', errors='replace') as file:
                file.write(json.dumps(data))
                self.echo('Successful', color='green', bgcolor='darkgray', end='\n')

        except Exception as e:
            self.echo('Unsuccessful', color='red', bgcolor='darkgray', end='\n')

            # Output error message with details of the exception.
            self.echo(f"[Error:] Writing file '{path}'\n{e}", color="red")

    # Creating API url for GeoNode "Free-Proxy-List"
    def generate_url(self, anonymity_level=None, protocols=None, up_time=None, last_checked=None, speed=None,
                     google=None, country=None, limit=500, page=1, sort_by='lastChecked', sort_type='desc') -> str:
        """
        Constructs the Geonode API URL based on provided options.

        :param anonymity_level: Filter by anonymity level (e.g., 'elite', 'anonymous', 'transparent').
        :param protocols: Filter by protocols (e.g., 'http', 'https', 'socks4', 'socks5').
        :param up_time: Filter by uptime percentage.
        :param last_checked: Filter by how recently the proxies were checked (in minutes).
        :param speed: Filter by speed (e.g., 'fast', 'medium', 'slow').
        :param google: Filter by Google Passed support (True/False).
        :param limit: Limit the number of proxies returned (default is 500).
        :param page: Page number of results (default is 1).
        :param sort_by: Sort results by this field (default is 'lastChecked').
        :param sort_type: Sort direction ('asc' for ascending or 'desc' for descending, default is 'desc').
        :param country: Filter by country code (e.g., 'US', 'AR', 'AU', 'BR', 'DE', 'FR', 'GB',... ).
        :return: Constructed URL string for the Geonode API.
        """

        self.echo('Geonode-API url Generator', color='blue', end='\n')

        # Base URL for the API
        base_url = "https://proxylist.geonode.com/api/proxy-list"

        # Initialize query parameters with required options
        params = {
            "limit": limit,
            "page": page,
            "sort_by": sort_by,
            "sort_type": sort_type
        }

        # Add optional filters to the query parameters
        if anonymity_level:
            params["anonymityLevel"] = ",".join(anonymity_level)  # elite | anonymous | transparent

        if protocols:
            params["protocols"] = ",".join(protocols)  # http | https | socks4| socks5

        if up_time is not None:
            params["filterUpTime"] = up_time  # %0 ~ 100

        if last_checked is not None:
            params["filterLastChecked"] = last_checked  # 1 ~ 60min

        if speed:
            params["speed"] = speed  # Fast | Medium | Slow

        if google is not None:
            params["google"] = str(google).lower()  # True | False

        if country:
            params["country"] = country  # 'US', 'AR', 'AU', 'BR', 'DE', 'FR', 'GB'...

        # Construct the query string
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])

        # Complete URL
        complete_url = f"{base_url}?{query_string}"

        self.echo(f'[URL:] {complete_url}', end='\n')
        return complete_url

    # Get DATA from web
    def fetch_api(self, api_url: str) -> dict:
        """
        Send a request to the provided URL and return the response data.

        :param api_url: The URL to fetch the data from.
        :return: A dictionary containing the response data or an error message.
        """
        self.echo(f'Fetch API:', end=' ')

        try:
            # Send a GET request to the specified URL
            response = requests.get(api_url)

            # Raise an exception if the request was unsuccessful
            response.raise_for_status()

            self.echo('Successful', color='green', bgcolor='darkgray', end='\n')

            # Return the response data in JSON format
            return response.json()

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            self.echo('Unsuccessful', color='red', bgcolor='darkgray', end='\n')
            self.echo(f"[Error:] fetching data from: '{api_url}'\n{e}")

            return {"error": str(e)}

    # Read DATA from files that created manually
    def read_api(self, path: str) -> dict:
        """
        Read data from a file.

        :param path: The path to the JSON file containing data.
        :return: A dictionary containing the response data or an error message.
        """
        # Read the content of the file using the read_a_file method.
        file = self.read_a_file(path)

        self.echo(f'Read API from JSON:', end=' ')

        try:
            # Load the JSON data from the file content.
            api = json.loads(file)
            self.echo('Successful', color='green', bgcolor='darkgray', end='\n')
            return api

        except Exception as e:
            self.echo('Unsuccessful', color='red', bgcolor='darkgray', end='\n')
            self.echo(f'[Error:] Load file as JSON module:\n{e}')
            return {"error": str(e)}

    # Turn DATA to list of pure proxies ('ip', 'port', 'protocol' only)
    def export_proxies(self, data: dict) -> list:
        """
        Extract a list of proxies from the provided data.

        :param data: Dictionary containing the original GeoNode API data.
        :return: List of proxies with 'ip', 'port', and 'protocol' information.
        """
        # Proxy Storage
        proxies_list = []

        self.echo(f'Proxies exporting:', end=' ')

        for proxy in data['data']:  # GeoNode API Data
            try:
                ip = proxy.get('ip', '')  # Extract IP address or default to empty string if not present
                port = proxy.get('port', '')  # Extract port number or default to empty string if not present
                protocol = proxy.get('protocols', '')  # Extract protocols or default to an empty list if not present

                extract = {
                    'ip': ip,
                    'port': port,
                    'protocol': protocol[0]
                }

                proxies_list.append(extract)

            except Exception as e:
                self.echo(f"[Error:] reading proxy information from JSON file: {e}", color='red')
                continue

        self.echo('Done', color='green', bgcolor='darkgray', end='\n')
        # Return the list
        return proxies_list

    # Cut pure proxies ('ip', 'port', 'protocol' only) from standard lists
    def cut_proxy(self, proxies: list) -> list:
        """
        Extract only 'ip', 'port', and 'protocol' from a list of proxies.

        :param proxies: List of proxy data.
        :return: List of proxies with minimal information.
        """
        # Initialize a list to hold the extracted proxies.
        proxies_list = []

        self.echo(f"Cut only 'ip', 'port' and 'protocol' from data", end=' ')

        for proxy in proxies:
            try:
                # Extract only "IP", "Port", and "Protocol" from each JSON object.
                extract = {
                    'ip': proxy.get('ip', ''),  # Extract IP address; default is ''
                    'port': proxy.get('port', ''),  # Extract port number; default is ''
                    'protocol': proxy.get('protocol', ''),  # Extract protocol; default is ''
                }

                # Add the extracted proxy details to the list.
                proxies_list.append(extract)

            except Exception as e:
                self.echo(f'[Error:] while reading data:\n{e}')
                continue

        return proxies_list

    def help(self):
        """
        Display available methods and properties in Geonode and Toolkit.

        - Toolkit Version

            # Magic Functions
                __init__
                __len__
                __repr__
                __str__

            # Property
                version

            # Present text
                echo

            # Read Files
                read_a_file
                import_standard_txt
                import_standard_json

            # Check proxy | Core functions
                check_socks_proxy
                check_http_proxy

            # Handle the proxy checking
                present_the_proxy
                add_the_proxy
                check_the_proxy

            # Prime function
                check_the_proxies

        - Geonode Version

            # Save as JSON
                save_as_json

            # Handle Geonode API
                generate_url
                fetch_api
                read_api

            # Export proxies from data
                export_proxies

            # Cut only proxies (ip, port, protocol) from data
                cut_proxy
        """
        self.echo("Read documentations for more information", color='blue')
