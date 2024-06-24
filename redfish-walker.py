import os
import json
import requests
from urllib.parse import urljoin, urlparse

class RedfishCrawler:
    def __init__(self, host_ip, start_resource, output_dir='redfish_mock_data', debug=False, username=None, password=None):
        """
        Initialize the RedfishCrawler instance.

        Parameters:
        - host_ip (str): IP address of the Redfish service.
        - start_resource (str): Starting resource path (e.g., "/redfish/v1/Chassis").
        - output_dir (str): Directory to save crawled data (default: 'redfish_mock_data').
        - debug (bool): Flag to enable debug mode with verbose output (default: False).
        - username (str): Username for basic authentication (optional).
        - password (str): Password for basic authentication (optional).
        """
        self.host_ip = host_ip
        self.base_url = f"https://{host_ip}/redfish/v1"
        self.start_resource = start_resource
        self.output_dir = output_dir
        self.debug = debug
        self.auth = (username, password) if username and password else None
        self.session = requests.Session()
        self.session.verify = False  # Ignore SSL certificate verification
        
    def crawl(self):
        """
        Initiate the crawling process starting from the specified resource.
        """
        self._crawl_resource(self.start_resource)
        
    def _crawl_resource(self, resource_url, visited=None):
        """
        Recursively crawl the resource and its related resources.

        Parameters:
        - resource_url (str): URL path of the resource to crawl.
        - visited (set): Set of visited URLs to prevent infinite recursion (default: None).
        """
        full_url = urljoin(self.base_url, resource_url)
        
        try:
            response = self.session.get(full_url, auth=self.auth)
            if response.status_code == 200:
                self._handle_successful_response(full_url, response, visited)
            else:
                self._handle_failed_response(full_url, response)
        except requests.RequestException as e:
            self._handle_request_exception(full_url, e)
    
    def _handle_successful_response(self, full_url, response, visited=None):
        """
        Handle successful response from a GET request.

        Parameters:
        - full_url (str): Full URL of the successfully fetched resource.
        - response (requests.Response): Response object containing the fetched data.
        - visited (set): Set of visited URLs to prevent infinite recursion.
        """
        try:
            data = response.json()
            self._save_data(full_url, data)
            
            if visited is None:
                visited = set()
            visited.add(full_url)
            
            if '@odata.id' in data:
                current_odata_id = data['@odata.id']
                self._crawl_related_resources(data, visited, current_odata_id)
        except json.JSONDecodeError as e:
            self._handle_json_decode_error(full_url, e)
    
    def _crawl_related_resources(self, data, visited, current_odata_id):
        """
        Recursively crawl related resources within the fetched data.

        Parameters:
        - data (dict): JSON data of the current resource.
        - visited (set): Set of visited URLs to prevent infinite recursion.
        - current_odata_id (str): @odata.id of the current resource.
        """
        for key, value in data.items():
            if key == '@odata.id' and isinstance(value, str) and value.startswith('/redfish/v1'):
                member_url = urljoin(self.base_url, value)
                if member_url not in visited and current_odata_id in member_url:
                    self._crawl_resource(member_url, visited)
            elif isinstance(value, dict):
                self._crawl_related_resources(value, visited, current_odata_id)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._crawl_related_resources(item, visited, current_odata_id)
    
    def _save_data(self, full_url, data):
        """
        Save JSON data to a file.

        Parameters:
        - full_url (str): Full URL of the fetched resource.
        - data (dict): JSON data to be saved.
        """
        relative_path = urlparse(full_url).path.lstrip('/redfish/v1')
        output_folder = os.path.join(self.output_dir, relative_path)
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, 'index.json')
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        if self.debug:
            print(f"Saved {full_url} to {output_file}")
    
    def _handle_failed_response(self, full_url, response):
        """
        Handle failed response from a GET request.

        Parameters:
        - full_url (str): Full URL of the resource that failed to fetch.
        - response (requests.Response): Response object containing the failure status.
        """
        if self.debug:
            print(f"Failed to fetch {full_url}. Status code: {response.status_code}")
    
    def _handle_request_exception(self, full_url, exception):
        """
        Handle exceptions raised during a GET request.

        Parameters:
        - full_url (str): Full URL of the resource that caused the exception.
        - exception (Exception): Exception object raised during the request.
        """
        if self.debug:
            print(f"Request failed for {full_url}. Exception: {exception}")
    
    def _handle_json_decode_error(self, full_url, exception):
        """
        Handle JSON decoding errors.

        Parameters:
        - full_url (str): Full URL of the resource that caused the JSON decoding error.
        - exception (json.JSONDecodeError): Exception object raised during JSON decoding.
        """
        if self.debug:
            print(f"Failed to parse JSON response for {full_url}. Exception: {exception}")

# Example usage:
if __name__ == "__main__":
    host_ip = "your_host_ip"
    start_resource = "/redfish/v1/Chassis"
    output_dir = "redfish_mock_data"
    debug_mode = True
    username = "your_username"
    password = "your_password"

    # Initialize RedfishCrawler instance
    crawler = RedfishCrawler(host_ip, start_resource, output_dir, debug_mode, username, password)
    
    # Start crawling from the specified start resource
    crawler.crawl()
