import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector, ProxyType
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

PROXY_LIST_URLS = {
    'SOCKS4': [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
    ],
    'SOCKS5': [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    ],
    'HTTP': [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    ],
}

async def fetch_proxy_list(session, url):
    async with session.get(url) as response:
        text = await response.text()
        return set(text.strip().splitlines())

async def check_proxy(proxy_type, proxy, session, live_proxies, dead_proxies, checking_proxies):
    if not proxy or not proxy.strip():
        return

    try:
        checking_proxies.add(proxy)
        target_url = "https://ifconfig.me"

        if proxy_type in ['SOCKS4', 'SOCKS5']:
            proxy_url = f"socks5://{proxy}" if proxy_type == 'SOCKS5' else f"socks4://{proxy}"
            connector = ProxyConnector.from_url(proxy_url)
            test_session = aiohttp.ClientSession(connector=connector)
        else:
            connector = aiohttp.TCPConnector()
            test_session = aiohttp.ClientSession(connector=connector)
            proxy_url = f"http://{proxy}"

        async with test_session.get(target_url, proxy=proxy_url, timeout=20) as response:
            if response.status == 200:
                live_proxies.add(f"{proxy_type} {proxy}")
            else:
                dead_proxies.add(f"{proxy_type} {proxy}")
    except Exception as e:
        dead_proxies.add(f"{proxy_type} {proxy}")
    finally:
        checking_proxies.discard(proxy)
        await test_session.close()

async def update_layout(layout, live_proxies, dead_proxies, checking_proxies):
    live_proxy_list = "\n".join(live_proxies)
    layout["main"].update(
        Panel(
            Text(f"Live Proxies:\n{live_proxy_list}", style="bold green")
        )
    )
    layout["footer"].update(
        Panel(
            Text(f"Live: {len(live_proxies)} | Dead: {len(dead_proxies)} | Checking: {len(checking_proxies)}", style="bold yellow")
        )
    )

async def main():
    console = Console()
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", minimum_size=10),
        Layout(name="footer", size=3),
    )

    layout["header"].update(Panel(Text("Proxy Checker by Robot", style="bold magenta")))
    layout["footer"].update(Panel(Text("Initializing...")))

    live = Live(layout, console=console, auto_refresh=False)
    live_proxies, dead_proxies, checking_proxies = set(), set(), set()

    async with aiohttp.ClientSession() as session:
        for proxy_type, urls in PROXY_LIST_URLS.items():
            tasks = [fetch_proxy_list(session, url) for url in urls]
            lists_of_proxies = await asyncio.gather(*tasks)
            proxy_list = set().union(*lists_of_proxies)

            check_tasks = [
                asyncio.create_task(check_proxy(proxy_type, proxy, session, live_proxies, dead_proxies, checking_proxies))
                for proxy in proxy_list
            ]

            with live:
                while check_tasks:
                    done, check_tasks = await asyncio.wait(check_tasks, return_when=asyncio.FIRST_COMPLETED)
                    for task in done:
                        await update_layout(layout, live_proxies, dead_proxies, checking_proxies)
                    live.refresh()

                layout["footer"].update(Panel(Text(f"Check Completed. {len(live_proxies)} Live proxies written to live_proxies.txt\n You can check the proxies by running `curl --socks5 IP:PORT https://ifconfig.me to see if it is correctly working")))
                live.refresh()

                with open("live_proxies.txt", "w") as f:
                    for proxy in live_proxies:
                        f.write(f"{proxy}\n")

if __name__ == "__main__":
    asyncio.run(main())
