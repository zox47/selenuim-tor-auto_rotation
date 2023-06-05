from selenium import webdriver
from stem import Signal
from stem.control import Controller
import subprocess
import undetected_chromedriver as uc
import time

# Start Tor with a control port enabled
tor_process = subprocess.Popen([r"C:\Users\viiru\Desktop\tor\tor\tor"])

# Connect to the Tor control port
with Controller.from_port(port=9051) as controller:
    controller.authenticate(password="abdo2000")

    # Set the IP address to change with Tor
    def set_tor_proxy():
        options = uc.ChromeOptions()
        options.add_argument("--proxy-server=socks5://127.0.0.1:9050")  # Use Tor proxy
        return options

    # Create a new Selenium Chrome driver with the Tor proxy
    options = set_tor_proxy()
    driver = uc.Chrome(options=options)

    # Use the driver with Tor
    driver.get("https://ipgeolocation.io/ip-location-api.html")

    # Change Tor IP address
    def renew_tor_ip():
        controller.signal(Signal.NEWNYM)
        options = set_tor_proxy()
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
        driver.execute_cdp_cmd("Network.clearBrowserCache", {})
        driver.set_network_conditions(
            offline=False,
            latency=0,
            download_throughput=0,
            upload_throughput=0,
        )

    # Renew the Tor IP address and visit a new URL
    while True:
        input('Press Enter to change IP...')
        renew_tor_ip()
        driver.get("https://ipgeolocation.io/ip-location-api.html")
        time.sleep(1)  # Wait for the new IP to take effect
