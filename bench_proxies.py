import requests
import time
import multiprocessing
import logging
from tqdm import tqdm  


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

test_url = "https://ipinfo.io/json"

def load_proxies_from_file(filename):
    """Load proxies from a given file."""
    with open(filename, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def check_proxy(proxy):
    """Check the response time of a proxy."""
    start_time = time.time()
    try:
        logging.info(f"Testing proxy: {proxy}")
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=5)
        response_time = time.time() - start_time
        logging.info(f"Proxy {proxy} responded with status code {response.status_code} in {response_time:.2f} seconds.")
        return proxy, response.status_code, response_time
    except requests.RequestException:
        logging.warning(f"Proxy {proxy} failed to respond.")
        return proxy, None, None  

def benchmark_proxies(proxies):
    results = []
    
    with tqdm(total=len(proxies), desc="Testing Proxies") as pbar:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            for proxy, result in zip(proxies, pool.imap(check_proxy, proxies)):
                results.append(result)
                pbar.update(1)  

    return results

def save_results_to_file(results, filename):
    """Save benchmarking results to a file."""
    valid_results = [(proxy, status_code, response_time) for proxy, status_code, response_time in results if status_code is not None]
    sorted_results = sorted(valid_results, key=lambda x: x[2])  # Sort by response time

    with open(filename, 'a') as file:
        for proxy, status_code, response_time in sorted_results:
            file.write(f"{proxy}\n")

if __name__ == "__main__":
    proxies_file = "Proxies\http_proxies.txt"
    proxies = load_proxies_from_file(proxies_file)
    
    logging.info("Starting proxy benchmarking...")
    benchmark_results = benchmark_proxies(proxies)

    # Save the results to a file
    output_file = "proxy_benchmark_results.txt"
    save_results_to_file(benchmark_results, output_file)

    logging.info(f"Results saved to {output_file}.")
