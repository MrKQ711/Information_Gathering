# Content

- [Content](#content)
  - [Whois](#whois)
    - [The way to work](#the-way-to-work)
    - [Demo](#demo)
  - [Google Hacking](#google-hacking)
    - [The way to work](#the-way-to-work-1)
    - [Demo](#demo-1)
  - [Netcraft](#netcraft)
    - [The way to work](#the-way-to-work-2)
    - [Demo](#demo-2)
  - [Recon-ng](#recon-ng)
    - [The way to work](#the-way-to-work-3)
    - [Demo](#demo-3)
  - [Shodan](#shodan)
    - [The way to work](#the-way-to-work-4)
    - [Demo](#demo-4)
  - [Security Headers Scanner](#security-headers-scanner)
    - [The way to work](#the-way-to-work-5)
    - [Demo](#demo-5)
  - [SSL Server Test](#ssl-server-test)
    - [The way to work](#the-way-to-work-6)
    - [Demo](#demo-6)
  - [User Information Gathering](#user-information-gathering)
    - [Harvesting](#harvesting)
      - [The way to work](#the-way-to-work-7)
  - [Social Media Tools](#social-media-tools)
    - [Social-Searcher](#social-searcher)
      - [The way to work](#the-way-to-work-8)
      - [Demo](#demo-7)
  
## Whois

### The way to work

- WHOIS is a service on the internet that allows users to search for information related to domain names or IP addresses. The WHOIS mechanism of action consists of storing detailed information about domain names and IP addresses in a global database managed by the Internet Corporation for Assigned Names and Numbers (ICANN).
- Information fed into WHOIS includes details such as the domain name owner's name or IP address, email address, contact phone number, and DNS server information. This information must be provided as required by ICANN to ensure the transparency and reliability of the domain name system and IP address on the internet.
- When users want to access information related to domain names or IP addresses, they can make WHOIS queries on websites that provide this service. The results from this query will display information related to the domain name or IP address the user searched for.

### Demo

  ![Picture](../6.%20Active%20Information%20Gathering/Image/1.png)
- We should notice something:
  - Domain name: epicnpc.com
  - Registrar: GoDaddy.com, LLC
  - Creation date: 2010-04-29T22:30:22Z
  - Expiration date: 2025-04-29T22:30:22Z
  - Name servers: lisa.ns.cloudflare.com and walt.ns.cloudflare.com
  - Domain status: clientDeleteProhibited, clientRenewProhibited, clientTransferProhibited and clientUpdateProhibited.
  - DNSSEC status: unsigned
  - Whois database last update date: 2023-06-13T07:09:47Z

## Google Hacking

### The way to work

- Google hacking is a technique of searching information on the Internet by using special keywords or syntactic components in Google queries to find hidden information and resources of systems, servers and applications. web.
- When a user types a query into Google Search, that query is sent to Google's database to perform searches on web pages on the Internet. Google uses a complex algorithm to identify sites that are relevant to the query and sort them by priority.
- The keywords and syntax in the query will help Google's algorithm better understand the needs of the user and find the most suitable websites. Then, Google will return the user search results in order of preference.
- However, not all web pages are stored in Google's database and not all web pages are searchable by Google. This may result in incomplete or incomplete search results.

### Demo

  ![Picture](../6.%20Active%20Information%20Gathering/Image/2.png)
  ![Picture](../6.%20Active%20Information%20Gathering/Image/3.png)
  ![Picture](../6.%20Active%20Information%20Gathering/Image/4.png)

## Netcraft

### The way to work

- Netcraft's mechanism of action includes the following steps:
  - Data Collection: Netcraft uses an IDM engine to collect information about websites, servers, and networks on the Internet. These tools are programmed to automatically visit websites and get information about them. Depending on the intended use, IDM may collect information about the domain name, IP address, server type, information about applications and web services running on the server, server response time, etc. , and security metrics.
  - Data analysis and processing: Once data is collected, Netcraft uses data analysis and processing technologies to generate reports and visualizations on the security and performance status of websites. and server. These technologies include data mining, artificial intelligence, and data modeling and statistical analysis.
  - Providing services and products: Based on reports and images on the security and performance of websites and servers, Netcraft provides security and system administration related products and services. web such as: Malware analysis, server progress monitoring, security threat and author analysis, blacklist matching of domains involved in phishing and phishing.
- IDM is a Netcraft tool used to collect information about websites, servers, and networks on the Internet. To be able to collect this information, IDM uses crawling and scraping techniques.
  - Crawling is the automatic process of visiting websites and collecting links related to that website. These links will be stored in a list and then IDM will continue to visit new sites to collect information.
  - Scraping is the automatic process of getting information from web pages by parsing the HTML of that web page. This information may include the domain name, IP address, server type, and applications and web services running on the server.
  - Once the information is collected, IDM uses data processing and analysis technologies to generate reports and visualizations on the security and performance status of websites and servers.

### Demo

- We can use Netcraft’s DNS search page 
(https://searchdns.netcraft.com) to gather information about the epicnpc.com domain
  ![Picture](../6.%20Active%20Information%20Gathering/Image/5.png)
- We can view a “site report” that provides additional information and history 
about the server by clicking on the file icon next to each site URL
  ![Picture](../6.%20Active%20Information%20Gathering/Image/6.png)
- If we scroll down, we discover various “site technology” entries:
  ![Picture](../6.%20Active%20Information%20Gathering/Image/7.png)

## Recon-ng

### The way to work

- Recon-ng is an open source framework used for performing information retrieval and vulnerability identification operations of a system. The mechanism of action of Recon-ng includes the following steps:
  - Perform a target search: Recon-ng uses modules to gather information about a target. These modules can be configured to look up information from a variety of sources, such as domains, IPs, emails, social media accounts, and more.
  - Information analysis and vulnerability identification: After gathering information, Recon-ng analyzes and displays the results in a structured format. These results can be used to identify vulnerabilities in the target system.
  - Automate activities: Recon-ng allows to automate operations through the use of built-in scripts and modules. This reduces the time and effort required for information retrieval and vulnerability identification.
  - Store results: Recon-ng allows to store the results obtained in different databases, such as SQLite or PostgreSQL. This makes it easy to re-access the results gathered during testing and searching.
  
### Demo

  ![Picture](../6.%20Active%20Information%20Gathering/Image/8.png)
- According to the output, we need to install various modules to use recon-ng.
- We can add modules from the recon-ng “Marketplace”.150 We’ll search the marketplace from the main prompt with marketplace search, providing a search string as an argument.
- In this example, we will search for modules that contain the term github.
- Let’s use this command to examine the recon/domains-hosts/google_site_web module.
  ![Picture](../6.%20Active%20Information%20Gathering/Image/9.png)
- According to its description, this module searches Google with the “site” operator and it doesn’t require an API key. Let’s install the module with marketplace install and run it.
- Notice that the output contains additional information about the module now that we’ve installed and loaded it. According to the output, the module requires the use of a source, which is the target we want to gather information about.
  ![Picture](../6.%20Active%20Information%20Gathering/Image/10.png)
  ![Picture](../6.%20Active%20Information%20Gathering/Image/11.png)
  ![Picture](../6.%20Active%20Information%20Gathering/Image/12.png)
- It same with the thing we found in Netcraft DNS search.
- We have host in our database but no additional information on them. Perhaps another module can fill in the IP addresses.
- Let’s examine recon/hosts-hosts/resolve with marketplace info. We will install and run it.
  ![Picture](../6.%20Active%20Information%20Gathering/Image/13.png)

## Shodan

### The way to work

- Shodan's mechanism of action includes the following steps:
  - Data collection: Shodan uses scanning tools to collect information about internet-connected devices around the world.
  - Data storage and processing: Once collected, Shodan stores this data and uses analytical algorithms to process and extract useful information from the devices.
  - Search and query: Users can search for devices by various criteria using queries in Shodan.
- Shodan uses a variety of network scanning tools to gather information about internet-connected devices. Some of the tools Shodan uses include:
  - Nmap: This is a widely used open source network scanning tool to find internet-connected devices.
  - Zmap: This is an open source network scanner that scans the entire IP address space within minutes.
  - Masscan: This is an open source port scanning tool that allows to scan hundreds of thousands of ports in seconds.
  - Censys: This is a network search and scan tool used to find internet-connected devices and store information related to them.

### Demo

- Let’s start by using Shodan to search for hostname:epicnpc.com
  ![Picture](../6.%20Active%20Information%20Gathering/Image/14.png)
- I try to get more information about port 2200.
  ![Picture](../6.%20Active%20Information%20Gathering/Image/15.png)
- Actually, i get the version of OpenSSh is running on each server.

## Security Headers Scanner

### The way to work

- The site securityheaders.com works by using technology from the Mozilla Observatory to analyze the security headers on the web page and produce a detailed report on the security level of that site.
- When you enter a website's URL into the securityheaders.com website, it sends a request to the Mozilla Observatory for analysis. The analysis results are then returned and the securityheaders.com website generates a detailed report on the security headers available on that site. This report shows what security headers have been installed on the website, their security level, and recommendations for improving website security.
- Mozilla Observatory technology uses various testing tools to analyze security headers on web pages, including CSP, HSTS, and HPKP testing tools. These tools help identify weaknesses in site protection and provide insights to help users improve their site's security.

### Demo

 ![Picture](../6.%20Active%20Information%20Gathering/Image/16.png)

## SSL Server Test

### The way to work

- Check the security of an HTTPS connection to a web server. This tool checks that the web server is using a valid SSL certificate, and that the server's other security settings are configured correctly, to ensure that users accessing Your site is being protected as best as possible.
- The working mechanism of SSL Server Test is quite simple. When you enter the domain name of a website to be tested into the tool, SSL Labs will perform the following steps:
  - Download the SSL certificate from the web server.
  - Check the validity of the SSL certificate and verify that it was issued by a reputable organization.
  - Check the server's other security settings, such as the type of encryption used to protect data transmitted over HTTPS connections.
  - Give a score and other assessments of the security of the HTTPS connection to the server.

### Demo

  ![Picture](../6.%20Active%20Information%20Gathering/Image/17.png)
  ![Picture](../6.%20Active%20Information%20Gathering/Image/18.png)

## User Information Gathering

### Harvesting

#### The way to work

- TheHarvester uses built-in search engines and techniques to gather information about a given target. These tools include Google Dorking, DNS Enumeration, HTML Parsing, and Search Engine Footprinting.
- It will use techniques like Google Dorking to filter and find the necessary information. It then uses DNS Enumeration to find information about DNS servers, domain names, and IP addresses connecting to the domain. It then parses the web pages and extracts the necessary information from the HTML tags using HTML Parsing. Finally, it uses Search Engine Footprinting techniques to find information about websites through exploiting techniques of Google hacking, Bing hacking and other search engines.

## Social Media Tools

### Social-Searcher

#### The way to work

- Social-Searcher uses search and data analysis technologies to collect information from social networking sites. These sites provide APIs (Application Programming Interfaces) that allow access to their data through HTTP requests.
- When a user enters a keyword or hashtag to search, Social-Searcher sends a request to the APIs of the related social networks and collects data about posts, articles, images, videos and categories. other content containing that keyword.
- Then, Social-Searcher uses data analysis tools to filter and analyze the results, providing quick analysis reports and graphs to help users better understand trends and information on social networks. .

#### Demo

  ![Picture](../6.%20Active%20Information%20Gathering/Image/19.png)
- The search results will include information posted by the target organization and what people are saying about it. Among other things, this can help us determine what sort of footprint and coverage an organization has on social media. Once we’ve done this, we may choose to move on to using site-specific tools.


