# Redfish-Resource-Walker

#### Introduction

The Redfish Resource Walker is a Python tool designed to facilitate the retrieval and storage of data from Redfish-compliant servers. Redfish is an industry-standard protocol that simplifies the management and monitoring of hardware infrastructure. This tool leverages Python's `requests` library to interact with Redfish endpoints, retrieving JSON data and saving it locally for further analysis or mocking purposes.

#### Features

- **Recursive Crawling:** Initiates from a specified starting resource and recursively crawls related resources based on `@odata.id` references.
  
- **Data Storage:** Saves JSON responses from each crawled resource into structured directories and files (`index.json`).
  
- **Debug Mode:** Optional verbose output mode for debugging purposes, providing detailed messages about request successes, failures, and file creation status.
  
- **HTTPS Support:** Establishes secure connections using HTTPS for data retrieval.
  
- **Basic Authentication:** Supports authentication with username and password credentials if required by the Redfish server.
  
- **SSL Certificate Verification:** Allows for the disabling of SSL certificate verification to accommodate development and testing environments.

#### Installation

1. **Clone Repository:**
   ```
   git clone https://github.com/your/repository.git
   cd redfish-api-crawler
   ```

2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

#### Usage

1. **Initialize Crawler:**
   - Replace placeholders in the `__main__` section of `redfish-spider.py` with your Redfish server's IP, desired starting resource, and authentication credentials (if needed).

   ```python
   if __name__ == "__main__":
       host_ip = "your_host_ip"
       start_resource = "/redfish/v1/Chassis"
       output_dir = "redfish_mock_data"
       debug_mode = True
       username = "your_username"
       password = "your_password"

       crawler = RedfishCrawler(host_ip, start_resource, output_dir, debug_mode, username, password)
       crawler.crawl()
   ```

2. **Run the Crawler:**
   ```
   python redfish-spider.py
   ```

#### Example

Assume you want to crawl data starting from `/redfish/v1/Chassis` on a Redfish server located at `192.168.1.100`, using basic authentication with credentials `admin` and `password`, and storing data in `redfish_mock_data` directory. Here’s how you would configure and execute the crawler:

```python
if __name__ == "__main__":
    host_ip = "192.168.1.100"
    start_resource = "/redfish/v1/Chassis"
    output_dir = "redfish_mock_data"
    debug_mode = True
    username = "admin"
    password = "password"

    crawler = RedfishCrawler(host_ip, start_resource, output_dir, debug_mode, username, password)
    crawler.crawl()
```

#### Contributing

Contributions are welcome! Please feel free to fork this repository, make improvements, and submit pull requests.

#### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

#### Acknowledgments

This tool was inspired by the need to efficiently retrieve and mock Redfish API data for development and testing purposes. Special thanks to the developers of the `requests` library for their robust HTTP handling capabilities.

---
