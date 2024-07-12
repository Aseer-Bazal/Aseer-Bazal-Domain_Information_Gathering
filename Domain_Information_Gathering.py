import socket
import dns.resolver
import requests
import whois

# Function to get the IP address of a domain
def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        return f"Error retrieving IP address: {e}"

# Function to get DNS records
def get_dns_records(domain):
    records = {}
    try:
        resolver = dns.resolver.Resolver()
        records['A'] = [str(rdata) for rdata in resolver.resolve(domain, 'A')]
        records['AAAA'] = [str(rdata) for rdata in resolver.resolve(domain, 'AAAA')]
        records['MX'] = [str(rdata) for rdata in resolver.resolve(domain, 'MX')]
        records['NS'] = [str(rdata) for rdata in resolver.resolve(domain, 'NS')]
        records['TXT'] = [str(rdata) for rdata in resolver.resolve(domain, 'TXT')]
    except Exception as e:
        records['error'] = f"Error retrieving DNS records: {e}"
    return records

# Function to get WHOIS information
def get_whois_info(domain):
    try:
        whois_info = whois.whois(domain)
        return whois_info
    except Exception as e:
        return f"Error retrieving WHOIS information: {e}"

# Function to get subdomains using a third-party service (e.g., crt.sh)
def get_subdomains(domain):
    url = f"https://crt.sh/?q={domain}&output=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            subdomains = {entry['name_value'] for entry in response.json()}
            return list(subdomains)
        else:
            return f"Error retrieving subdomains: HTTP {response.status_code}"
    except Exception as e:
        return f"Error retrieving subdomains: {e}"

# Main function to gather domain information
def gather_domain_info(domain):
    info = {}
    info['IP Address'] = get_ip(domain)
    info['DNS Records'] = get_dns_records(domain)
    info['WHOIS Information'] = get_whois_info(domain)
    info['Subdomains'] = get_subdomains(domain)
    return info

# Example usage
if __name__ == "__main__":
    domain = input("Enter the domain name: ")
    domain_info = gather_domain_info(domain)
    for key, value in domain_info.items():
        if key == "Subdomains" and isinstance(value, list):
            print(f"{key}:")
            for subdomain in value:
                print(f"  - {subdomain}")
        else:
            print(f"{key}:\n{value}\n")
