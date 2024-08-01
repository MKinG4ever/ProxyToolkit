import requests  # For making HTTP/HTTPS requests.
import time  # For measuring response time (ping).
import socket  # For handling socket operations for SOCKS proxy.
import socks  # For handling SOCKS proxy setup.
import json  # For handling JSON files.
import Art  # Add ASCII arts.
from requests.exceptions import ProxyError, Timeout, RequestException  # For handling specific exceptions from requests.


class Toolkit:
    """
    proxyToolkit Module.
    A simple, lightweight, and fast proxy toolkit for handling and checking proxies.


    Author: NightFox
    Timestamp: 1722540206.9788792
    Powered-by: Python3
    """

    def __init__(self):
        """Initialize the Toolkit class with default attributes."""

        self.proxies = []  # List to store proxies.
        self.view = "https://www.google.com"  # URL to test proxy connection.

    def __len__(self):
        """Return the number of proxies in the list."""
        return len(self.proxies)

    def __repr__(self):
        """Return a representation of the Toolkit instance."""
        return f"{Art.repr_logo}ProxyToolkit {self.version} | ID: {id(self)}"

    def __str__(self):
        """Return a string representation of the Toolkit instance."""
        return f"{self.__repr__()}\n- List: {self.__len__()} proxies\n"

    # Version
    @property
    def version(self):
        """Return the version of the ProxyToolkit."""
        return "v1.0"

    # Echo, Print, Write
    @staticmethod
    def echo(*args, color: str | tuple = None, bgcolor: str | tuple = None, sep: str = ' ', end: str = '\n') -> None:
        """
        Prints a message with specified foreground and background colors (named or RGB).

        :param color: The foreground color of the message. Can be a name or a tuple of three integers for RGB color.
        :param bgcolor: The background color of the message. Can be a name or a tuple of three integers for RGB color.
        :param args: Variable length argument list for the message parts to be printed.
        :param sep: Separator between the messages. Default is a single space.
        :param end: End character after the message. Default is a newline.
        :return: None
        """

        # Define ANSI color codes for named colors
        color_codes = {
            'red': '\033[91m',  # Normal: "\033[91m" Bold: "\033[1;91m" | Red color code
            'yellow': '\033[93m',  # Yellow color code
            'green': '\033[92m',  # Green color code
            'blue': '\033[94m',  # Blue color code
            'magenta': '\033[95m',  # Magenta color code
            'cyan': '\033[96m',  # Cyan color code
            'black': '\033[30m',  # Black color code
            'gray': '\033[37m',  # Gray color code
            'darkgray': '\033[90m',  # Dark gray color code
            'lightgray': '\033[37m',  # Light gray color code (same as gray)
            'white': '\033[97m',  # White color code
            'purple': '\033[35m',  # Purple color code
            'brown': '\033[33m',  # Brown color code (represented as yellow, closest to brown in ANSI)
            'skyblue': '\033[36m',  # Sky blue color code (represented as cyan, closest to sky blue in ANSI)
            'reset': '\033[0m'  # Reset color code to default
        }

        # Define ANSI color codes for background colors
        bgcolor_codes = {
            'red': '\033[101m',  # Red background color code
            'yellow': '\033[103m',  # Yellow background color code
            'green': '\033[102m',  # Green background color code
            'blue': '\033[104m',  # Blue background color code
            'magenta': '\033[105m',  # Magenta background color code
            'cyan': '\033[106m',  # Cyan background color code
            'black': '\033[40m',  # Black background color code
            'gray': '\033[47m',  # Gray background color code
            'darkgray': '\033[100m',  # Dark gray background color code
            'lightgray': '\033[47m',  # Light gray background color code (same as gray)
            'white': '\033[107m',  # White background color code
            'purple': '\033[45m',  # Purple background color code
            'brown': '\033[43m',  # Brown background color code (represented as yellow, closest to brown in ANSI)
            'skyblue': '\033[46m',  # Sky blue background color code (represented as cyan, closest to sky blue in ANSI)
            'reset': '\033[49m'  # Reset background color code to default
        }

        # Determine foreground color ANSI code
        if isinstance(color, tuple) and len(color) == 3 and all(0 <= val <= 255 for val in color):
            r, g, b = color
            color_code = f'\033[38;2;{r};{g};{b}m'
        elif isinstance(color, str) and color in color_codes:
            color_code = color_codes[color]
        else:
            color_code = ''

        # Determine background color ANSI code
        if isinstance(bgcolor, tuple) and len(bgcolor) == 3 and all(0 <= val <= 255 for val in bgcolor):
            r, g, b = bgcolor
            bgcolor_code = f'\033[48;2;{r};{g};{b}m'
        elif isinstance(bgcolor, str) and bgcolor in bgcolor_codes:
            bgcolor_code = bgcolor_codes[bgcolor]
        else:
            bgcolor_code = ''

        # Combine the args into a single string with the specified separator
        message = sep.join(map(str, args))

        # Print the message with the selected colors and specified end character
        if bgcolor_code and color_code:
            print(f"{bgcolor_code}{color_code}{message}{color_codes['reset']}", end=end)
        elif bgcolor_code:
            print(f"{bgcolor_code}{message}{color_codes['reset']}", end=end)
        elif color_code:
            print(f"{color_code}{message}{color_codes['reset']}", end=end)
        else:
            print(message, end=end)

    # Read: any file
    def read_a_file(self, path: str) -> str:
        """
        Read the content of a file.

        :param path: Path to the file.
        :return: Content of the file as a string.
        """

        # Verbose output to indicate the start of the file reading process.
        self.echo(f'Reading file ({path}):', end=' ')

        try:
            # Open the file in read mode with UTF-8 encoding, replacing any errors.
            with open(file=path, mode='r', encoding='utf-8', errors='replace') as file:
                # Verbose output to indicate successful file reading.
                self.echo('Successful', color='green', bgcolor='darkgray', end='\n')

                # Return the content of the file.
                return file.read()

        except Exception as e:
            # Verbose output to indicate unsuccessful file reading.
            self.echo('Unsuccessful', color='red', bgcolor='darkgray', end='\n')

            # Output error message with details of the exception.
            self.echo(f"[Error:] Reading file error '{path}'\n{e}", color="red")

    # Import: TXT
    def import_standard_txt(self, path: str) -> list:
        """
        Imports proxies from a standard TXT file.

        :param path: The path to the TXT file containing proxy information.
        :return: A list of dictionaries containing proxy details (IP, port, protocol).
        """

        # Read the content of the file using the read_a_file method.
        file = self.read_a_file(path)

        # Verbose output to indicate the start of proxy extraction.
        self.echo(f'Extracting proxies (from {path}):', end=' ')

        try:
            # Split the file content into lines.
            proxies = file.splitlines()

            # Initialize a list to hold the extracted proxies.
            proxies_list = []

            for proxy in proxies:
                # Split each line into components and extract IP, port, and protocol.
                extract = {
                    'ip': proxy.split(' ')[0].split(':')[0].strip(),  # Extract IP address
                    'port': proxy.split(' ')[0].split(':')[1].strip(),  # Extract port number
                    'protocol': proxy.split(' ')[1].strip(),  # Extract protocols
                }
                # Add the extracted proxy details to the list.
                proxies_list.append(extract)

            # Verbose output to indicate successful extraction.
            self.echo('Successful', color='green', bgcolor='darkgray', end='\n')

            # Return the list of extracted proxies.
            return proxies_list

        except Exception as e:
            # Verbose output to indicate unsuccessful extraction.
            self.echo('Unsuccessful', color='red', bgcolor='darkgray', end='\n')

            # Output error message with details of the exception.
            self.echo(f"[Error:] Reading proxies error\n{e}", color="red")

    # Import: JSON
    def import_standard_json(self, path: str) -> list:
        """
        Imports proxies from a standard JSON file.

        :param path: The path to the JSON file containing proxy information.
        :return: A list of dictionaries containing proxy details (IP, port, protocol).
        """

        # Read the content of the file using the read_a_file method.
        file = self.read_a_file(path)

        # Verbose output to indicate the start of proxy extraction.
        self.echo(f'Extracting proxies (from {path}):', end=' ')

        try:
            # Load the JSON data from the file content.
            proxies = json.loads(file)

            # Initialize a list to hold the extracted proxies.
            proxies_list = []

            for proxy in proxies:
                # Extract IP, port, and protocol from each JSON object.
                extract = {
                    'ip': proxy.get('ip', ''),  # Extract IP address; default to empty string if not found
                    'port': proxy.get('port', 8080),  # Extract port number; default to 8080 if not found
                    'protocol': proxy.get('protocol', 'http'),  # Extract protocol; default to 'http' if not found
                }
                # Add the extracted proxy details to the list.
                proxies_list.append(extract)

            # Verbose output to indicate successful extraction.
            self.echo('Successful', color='green', bgcolor='darkgray', end='\n')

            # Return the list of extracted proxies.
            return proxies_list

        except Exception as e:
            # Verbose output to indicate unsuccessful extraction.
            self.echo('Unsuccessful', color='red', bgcolor='darkgray', end='\n')

            # Output error message with details of the exception.
            print(f"[Error:] Reading proxy information from JSON file: {e}")

    # Core: SOCKS
    def check_socks_proxy(self, ip: str, port: int, protocol: str, timeout: int = 9) -> dict:
        """
        Check the status of a SOCKS proxy.

        :param ip: IP address of the SOCKS proxy.
        :param port: Port number of the SOCKS proxy.
        :param protocol: Protocol type ('socks4' or 'socks5').
        :param timeout: Timeout in seconds for the proxy check.
        :return: Dictionary with proxy status information.
        """

        # Verbose output to indicate the start of the proxy status check.
        self.echo(f'Proxy status:', end=' ')

        # Determine SOCKS protocol type based on the provided protocol.
        proxy_type = socks.SOCKS4 if protocol.lower() == 'socks4' else socks.SOCKS5

        # Set up SOCKS proxy with the specified parameters.
        socks.set_default_proxy(proxy_type, ip, int(port))

        # Patch the socket module to use the SOCKS proxy.
        socket.socket = socks.socksocket

        # Record the start time for the proxy check.
        timer = time.time()

        try:
            # Make a GET request through the proxy to a test URL.
            response = requests.get(self.view, timeout=timeout)

            # Verbose output indicating the proxy is online.
            self.echo('Online', color='green', end='\n')

            # Return status information if the request succeeds.
            return {
                'info': {'ip': ip, 'port': port, 'protocol': protocol},
                'alive': True,
                'status_code': response.status_code,
                'content': response.text,
                'time': time.time() - timer
            }

        except (ProxyError, Timeout, RequestException, ConnectionError) as e:
            # Verbose output indicating the proxy is offline.
            self.echo('Offline', color='red', end='\n')

            # Handle exceptions and return status information indicating failure.
            return {
                'info': {'ip': ip, 'port': port, 'protocol': protocol},
                'alive': False,
                'status_code': None,
                'content': None,
                'time': time.time() - timer,
                'error': str(e)
            }

        finally:
            # Reset default proxy settings to None after the request is complete.
            socks.set_default_proxy(None)

    # Core: HTTPS
    def check_http_proxy(self, ip: str, port: int, protocol: str, timeout: int = 9) -> dict:
        """
        Check the status of an HTTP/HTTPS proxy.

        :param ip: IP address of the HTTP/HTTPS proxy.
        :param port: Port number of the HTTP/HTTPS proxy.
        :param protocol: Protocol type ('http' or 'https').
        :param timeout: Timeout in seconds for the proxy check.
        :return: Dictionary with proxy status information.
        """

        # Verbose output to indicate the start of the proxy status check.
        self.echo(f'Proxy status:', end=' ')

        # Construct the proxy dictionary for HTTP and HTTPS.
        proxies = {
            "http": f"http://{ip}:{int(port)}",
            "https": f"http://{ip}:{int(port)}"
        }

        # Record the start time for the proxy check.
        timer = time.time()

        try:
            # Make a GET request through the proxy to a test URL.
            response = requests.get(self.view, proxies=proxies, timeout=timeout)

            # Verbose output indicating the proxy is online.
            self.echo('Online', color='green', end='\n')

            # Return status information if the request succeeds.
            return {
                'info': {'ip': ip, 'port': port, 'protocol': protocol.lower()},
                'alive': True,
                'status_code': response.status_code,
                'content': response.text,
                'time': time.time() - timer
            }

        except (ProxyError, Timeout, RequestException, ConnectionError) as e:
            # Verbose output indicating the proxy is offline.
            self.echo('Offline', color='red', end='\n')

            # Handle exceptions and return status information indicating failure.
            return {
                'info': {'ip': ip, 'port': port, 'protocol': protocol.lower()},
                'alive': False,
                'status_code': None,
                'content': None,
                'time': time.time() - timer,
                'error': str(e)
            }

    # Present: theProxy
    def present_the_proxy(self, response: dict) -> None:
        """
        Present the results of a proxy check.

        :param response: Dictionary containing proxy status information.
        :type response: dict
        :return: None
        """

        # Check if the status code is 200 (OK) and print the details in green.
        if response['status_code'] == 200:
            self.echo(f"[Info:] {response['info']}", color="green", bgcolor="darkgray")
            self.echo(f"[Alive:] {response['alive']}", color="green", bgcolor="darkgray")
            self.echo(f"[Code:] {response['status_code']}", color="green", bgcolor="darkgray")
            self.echo(f"[Time:] {response['time']}", color="green", bgcolor="darkgray")
            self.echo(f"[Content:] {response['content'][:125]}...", bgcolor="darkgray")

        # Check if the proxy is alive but the status code is not 200, print the details in blue.
        elif response['alive']:
            self.echo(f"[Info:] {response['info']}", color="blue", bgcolor="darkgray")
            self.echo(f"[Alive:] {response['alive']}", color="blue", bgcolor="darkgray")
            self.echo(f"[Code:] {response['status_code']}", color="blue", bgcolor="darkgray")
            self.echo(f"[Time:] {response['time']}", color="blue", bgcolor="darkgray")
            self.echo(f"[Content:] {response['content'][:125]}...", bgcolor="darkgray")

        # If the proxy is not alive, print the details in red, including any error message.
        else:
            self.echo(f"[Info:] {response['info']}", color="red", bgcolor="darkgray")
            self.echo(f"[Alive:] {response['alive']}", color="red", bgcolor="darkgray")
            self.echo(f"[Code:] {response['status_code']}", color="red", bgcolor="darkgray")
            self.echo(f"[Time:] {response['time']}", color="red", bgcolor="darkgray")
            self.echo(f"[Error:] {response['error'][:125]}...", color="red", bgcolor="darkgray")

    # Add: theProxy
    def add_the_proxy(self, response: dict, verbose: bool = True) -> None:
        """
        Adds a proxy to the list if it is alive and optionally prints the proxy details.

        :param response: Dictionary containing the proxy's status information.
        :param verbose: Boolean flag to indicate if the proxy details should be printed.
                        Default is True.
        :type verbose: bool
        :return: None
        """

        # If verbose flag is True, present the proxy details using the present_the_proxy method
        if verbose:
            self.present_the_proxy(response=response)

        # Check if the proxy is alive
        if response['alive']:
            # Create a proxy dictionary with relevant details
            proxy = {
                'ip': response['info']['ip'],
                'port': response['info']['port'],
                'protocol': response['info']['protocol'],
                'code': response['status_code'],
                'ping': response['time'],
            }

            # Append the proxy to the proxies list
            self.proxies.append(proxy)

            # verbose: Notify that the proxy has been added to the list
            self.echo('Proxy added to list.', color='blue')

        # Print a newline character to separate output
        self.echo(end='\n')

    # Check: theProxy
    def check_the_proxy(self, ip: str, port: int, protocol: str, timeout: int = 9) -> dict:
        """
        Checks the status of a single proxy based on its protocol.

        :param ip: IP address of the proxy.
        :param port: Port number of the proxy.
        :param protocol: Protocol used by the proxy (http, https, socks4, socks5).
        :param timeout: Timeout for the proxy check in seconds. Default is 9 seconds.
        :return: Dictionary with proxy status information.
        """

        try:
            # Check if the protocol is either 'http' or 'https'
            if protocol.lower() in ['http', 'https']:
                return self.check_http_proxy(ip=ip, port=port, protocol=protocol, timeout=timeout)

            # Check if the protocol is either 'socks4' or 'socks5'
            elif protocol.lower() in ['socks4', 'socks5']:
                return self.check_socks_proxy(ip=ip, port=port, protocol=protocol, timeout=timeout)

            else:
                # Handle unsupported protocols
                self.echo(f"[Error:] Unsupported protocol error", color="red")
                return {
                    'info': {'ip': ip, 'port': port, 'protocol': protocol},
                    'alive': False,
                    'status_code': None,
                    'content': None,
                    'time': None,
                    'error': 'Unsupported protocol'
                }

        except Exception as e:
            # Handle general exceptions
            self.echo(f"[Error:] Proxy server error\n{e}", color="red")
            return {
                'info': {'ip': ip, 'port': port, 'protocol': protocol},
                'alive': False,
                'status_code': None,
                'content': None,
                'time': None,
                'error': str(e)
            }

    # Check: Proxies
    def check_the_proxies(self, proxy_list: list, timeout: int = 9, verbose: bool = True) -> None:
        """
        Checks the status of multiple proxies and adds them to the list if they are alive.

        :param proxy_list: List of proxies to check, where each proxy is a dictionary containing 'ip', 'port', and 'protocol'.
        :param timeout: Timeout for the proxy check in seconds. Default is 9 seconds.
        :param verbose: Boolean flag to indicate if detailed proxy information should be printed. Default is True.
        :return: None
        """

        # Display the initial logo/art
        self.echo(Art.default_logo)
        time.sleep(1)

        # Display the initiation logo/art
        self.echo(Art.initiate_logo)
        time.sleep(1)

        # Iterate over each proxy in the list
        for flag, proxy in enumerate(proxy_list):
            try:
                # Extract proxy details from the dictionary
                ip = proxy.get('ip', '')
                port = proxy.get('port', '')
                protocol = proxy.get('protocol', '')
                length = self.__len__()  # Get the current length of the proxies list

                # Verbose output of current proxy being checked
                self.echo(f'[{flag + 1}/{len(proxy_list)}][{length}] {protocol.upper()} {ip}:{port}', color='blue')

                # Check the proxy status
                result = self.check_the_proxy(ip=ip, port=port, protocol=protocol, timeout=timeout)

                # Add the proxy to the list if it is alive
                self.add_the_proxy(response=result, verbose=verbose)

            except Exception as e:
                # Handle and print any errors encountered
                self.echo(f"[Error:] Proxy information.\n{e}", color="red")
                continue  # Continue with the next proxy in the list

        # Display the end logo/art
        self.echo(Art.end_logo)

        # Display the final list of proxies
        self.echo(self.__str__())
