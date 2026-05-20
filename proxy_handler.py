# proxy_handler.py
# NEUTRONNNN_KILLER - ULTRA FAST PROXY HANDLER
# CHUMT KE PYASA, yeh proxy check karega aur live filter karega!

import asyncio
import aiohttp
import random
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import aiofiles

# Import config
try:
    from config import ProxyConfig, AttackConfig, FileConfig, logger_setup
except ImportError:
    # Fallback config if config.py not found
    class ProxyConfig:
        CHECK_TIMEOUT = 3
        CHECK_CONCURRENT = 200
        CHECK_URL = "https://httpbin.org/ip"
        CHECK_MAX_PROXIES = 500
        ROTATE_ON_FAIL = True
        ROTATE_AFTER_REQUESTS = 10
        MAX_PROXIES_TO_USE = 100
        PROXY_INPUT_FILE = "proxies.txt"
        PROXY_OUTPUT_LIVE = "live_proxies.txt"
        VALIDATE_SSL = False
    
    class AttackConfig:
        REQUEST_TIMEOUT = 2
    
    class FileConfig:
        LIVE_PROXIES_FILE = "live_proxies.txt"
        DEAD_PROXIES_FILE = "dead_proxies.txt"

import logging
logger = logging.getLogger(__name__)

# ============================================
# ULTRA FAST PROXY CHECKER
# ============================================

class ProxyHandler:
    """
    Handles all proxy operations:
    - Check if proxy is alive
    - Format proxy strings
    - Bulk proxy checking
    - Proxy rotation
    - Save/Load proxies
    """
    
    def __init__(self):
        self.live_proxies = []
        self.dead_proxies = []
        self.current_proxy_index = 0
        self.request_count = 0
    
    @staticmethod
    def format_proxy(proxy_string: str) -> Optional[str]:
        """
        Format proxy string for aiohttp
        Supported formats:
        - ip:port
        - protocol://ip:port
        - protocol://user:pass@ip:port
        """
        try:
            proxy_string = proxy_string.strip()
            
            # Remove any whitespace
            proxy_string = re.sub(r'\s+', '', proxy_string)
            
            # Add protocol if missing
            if '://' not in proxy_string:
                proxy_string = 'http://' + proxy_string
            
            # Validate format
            if re.match(r'^[a-z]+://.*', proxy_string, re.IGNORECASE):
                return proxy_string
            
            return None
        except Exception:
            return None
    
    @staticmethod
    async def check_single_proxy(proxy: str, session: aiohttp.ClientSession) -> bool:
        """
        Check if a single proxy is alive
        Returns True if proxy works, False otherwise
        """
        try:
            proxy_url = ProxyHandler.format_proxy(proxy)
            if not proxy_url:
                return False
            
            # Use a timeout to avoid hanging
            timeout = aiohttp.ClientTimeout(total=ProxyConfig.CHECK_TIMEOUT)
            
            # Test the proxy
            async with session.get(
                ProxyConfig.CHECK_URL,
                proxy=proxy_url,
                timeout=timeout,
                ssl=False if not ProxyConfig.VALIDATE_SSL else None
            ) as response:
                return response.status == 200
                
        except asyncio.TimeoutError:
            logger.debug(f"Proxy {proxy[:20]}... timeout")
            return False
        except aiohttp.ClientError as e:
            logger.debug(f"Proxy {proxy[:20]}... client error: {e}")
            return False
        except Exception as e:
            logger.debug(f"Proxy {proxy[:20]}... error: {e}")
            return False
    
    @staticmethod
    async def check_proxies_bulk(proxies: List[str], progress_callback=None) -> List[str]:
        """
        Check multiple proxies in parallel - ULTRA FAST
        Returns list of live proxies
        """
        if not proxies:
            return []
        
        # Limit number of proxies to check
        proxies_to_check = proxies[:ProxyConfig.CHECK_MAX_PROXIES]
        total = len(proxies_to_check)
        live = []
        
        # Create connection pool
        connector = aiohttp.TCPConnector(
            limit=ProxyConfig.CHECK_CONCURRENT,
            limit_per_host=50,
            ttl_dns_cache=300,
            ssl=False if not ProxyConfig.VALIDATE_SSL else None
        )
        
        timeout = aiohttp.ClientTimeout(total=ProxyConfig.CHECK_TIMEOUT)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Create tasks for all proxies
            tasks = []
            for proxy in proxies_to_check:
                task = ProxyHandler.check_single_proxy(proxy, session)
                tasks.append(task)
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Collect live proxies
            for proxy, is_live in zip(proxies_to_check, results):
                if is_live is True:
                    live.append(proxy)
                elif isinstance(is_live, Exception):
                    logger.debug(f"Proxy check exception: {is_live}")
            
            # Progress callback
            if progress_callback:
                await progress_callback(total, len(live))
        
        return live
    
    @staticmethod
    async def check_proxies_sequential(proxies: List[str], progress_callback=None) -> List[str]:
        """
        Check proxies one by one (slower but more reliable)
        """
        if not proxies:
            return []
        
        live = []
        total = len(proxies)
        
        connector = aiohttp.TCPConnector(limit=10, ssl=False if not ProxyConfig.VALIDATE_SSL else None)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            for idx, proxy in enumerate(proxies[:ProxyConfig.CHECK_MAX_PROXIES]):
                if await ProxyHandler.check_single_proxy(proxy, session):
                    live.append(proxy)
                
                if progress_callback and idx % 10 == 0:
                    await progress_callback(idx + 1, total, len(live))
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.05)
        
        return live
    
    # Alias for compatibility
    check_bulk = check_proxies_bulk
    
    @staticmethod
    async def load_proxies_from_file(file_path: str) -> List[str]:
        """
        Load proxies from a text file
        Each line should contain one proxy
        """
        try:
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
                proxies = []
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        proxies.append(line)
                return proxies
        except FileNotFoundError:
            logger.warning(f"Proxy file not found: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading proxies: {e}")
            return []
    
    @staticmethod
    async def save_proxies_to_file(file_path: str, proxies: List[str]):
        """
        Save proxies to a text file
        """
        try:
            async with aiofiles.open(file_path, 'w') as f:
                await f.write('\n'.join(proxies))
            logger.info(f"Saved {len(proxies)} proxies to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving proxies: {e}")
            return False
    
    @staticmethod
    def parse_proxy_file_content(content: str) -> List[str]:
        """
        Parse proxy file content and extract valid proxies
        """
        proxies = []
        for line in content.split('\n'):
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Basic validation
            if re.match(r'^[a-z]*://.*:\d+$', line, re.IGNORECASE) or \
               re.match(r'^\d+\.\d+\.\d+\.\d+:\d+$', line):
                proxies.append(line)
            elif re.match(r'^[a-z]*://.*:.*@.*:\d+$', line, re.IGNORECASE):
                proxies.append(line)
        
        return proxies
    
    @staticmethod
    def get_proxy_stats(proxies: List[str]) -> Dict:
        """
        Get statistics about proxies
        """
        stats = {
            'total': len(proxies),
            'http': 0,
            'https': 0,
            'socks4': 0,
            'socks5': 0,
            'authenticated': 0,
            'anonymous': 0
        }
        
        for proxy in proxies:
            if 'http://' in proxy.lower():
                stats['http'] += 1
            elif 'https://' in proxy.lower():
                stats['https'] += 1
            elif 'socks4://' in proxy.lower():
                stats['socks4'] += 1
            elif 'socks5://' in proxy.lower():
                stats['socks5'] += 1
            else:
                stats['http'] += 1
            
            if '@' in proxy:
                stats['authenticated'] += 1
            else:
                stats['anonymous'] += 1
        
        return stats

# ============================================
# PROXY ROTATOR - FOR ATTACKS
# ============================================

class ProxyRotator:
    """
    Handles proxy rotation during attacks
    """
    
    def __init__(self, proxies: List[str]):
        self.proxies = proxies.copy()
        self.current_index = 0
        self.request_count = 0
        self.failed_proxies = []
        
        # Shuffle proxies for random distribution
        random.shuffle(self.proxies)
    
    def get_next_proxy(self) -> Optional[str]:
        """
        Get next proxy in rotation
        """
        if not self.proxies:
            return None
        
        # Check if we need to rotate
        if self.request_count >= ProxyConfig.ROTATE_AFTER_REQUESTS:
            self.rotate()
        
        proxy = self.proxies[self.current_index % len(self.proxies)]
        self.request_count += 1
        
        return proxy
    
    def rotate(self) -> None:
        """
        Rotate to next proxy
        """
        self.current_index += 1
        self.request_count = 0
        logger.debug(f"Rotated to proxy index {self.current_index}")
    
    def mark_failed(self, proxy: str) -> None:
        """
        Mark a proxy as failed and remove it from rotation
        """
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            self.failed_proxies.append(proxy)
            logger.debug(f"Proxy failed: {proxy[:30]}... Remaining: {len(self.proxies)}")
    
    def get_live_count(self) -> int:
        """
        Get number of live proxies remaining
        """
        return len(self.proxies)
    
    def reset(self, new_proxies: List[str] = None) -> None:
        """
        Reset the rotator with new proxies
        """
        if new_proxies:
            self.proxies = new_proxies.copy()
        else:
            self.proxies = []
        
        self.current_index = 0
        self.request_count = 0
        self.failed_proxies = []
        random.shuffle(self.proxies)

# ============================================
# PROXY VALIDATOR - DEEP CHECK
# ============================================

class ProxyValidator:
    """
    Deep proxy validation with multiple test points
    """
    
    TEST_URLS = [
        "https://httpbin.org/ip",
        "https://api.ipify.org?format=json",
        "https://httpbin.org/get",
        "https://httpbin.org/headers"
    ]
    
    @staticmethod
    async def validate_proxy_deep(proxy: str) -> Tuple[bool, Dict]:
        """
        Deep validation of a proxy
        Returns (is_valid, details)
        """
        details = {
            'proxy': proxy,
            'response_time': None,
            'ip': None,
            'country': None,
            'supports_https': False,
            'error': None
        }
        
        try:
            proxy_url = ProxyHandler.format_proxy(proxy)
            if not proxy_url:
                return False, details
            
            start_time = asyncio.get_event_loop().time()
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    "https://httpbin.org/ip",
                    proxy=proxy_url,
                    ssl=False
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        details['ip'] = data.get('origin', 'unknown')
                        details['response_time'] = asyncio.get_event_loop().time() - start_time
                        details['supports_https'] = True
                        return True, details
            
            return False, details
            
        except asyncio.TimeoutError:
            details['error'] = "Timeout"
            return False, details
        except Exception as e:
            details['error'] = str(e)[:100]
            return False, details
    
    @staticmethod
    async def validate_batch(proxies: List[str], progress_callback=None) -> List[Tuple[str, bool, Dict]]:
        """
        Validate multiple proxies
        """
        results = []
        total = len(proxies)
        
        for idx, proxy in enumerate(proxies[:50]):  # Limit deep check to 50
            is_valid, details = await ProxyValidator.validate_proxy_deep(proxy)
            results.append((proxy, is_valid, details))
            
            if progress_callback and idx % 5 == 0:
                await progress_callback(idx + 1, total)
            
            await asyncio.sleep(0.1)
        
        return results

# ============================================
# MAIN FUNCTION - TESTING
# ============================================

async def test_proxy_handler():
    """
    Test function to verify proxy handler works
    """
    print("\n🧪 Testing Proxy Handler...")
    print("=" * 50)
    
    # Test 1: Format proxy
    test_proxies = [
        "192.168.1.1:8080",
        "http://user:pass@192.168.1.1:8080",
        "https://192.168.1.1:443",
        "invalid_proxy"
    ]
    
    print("\n📝 Test 1: Format Proxy")
    for proxy in test_proxies:
        formatted = ProxyHandler.format_proxy(proxy)
        print(f"  Input: {proxy}")
        print(f"  Output: {formatted}\n")
    
    # Test 2: Parse proxy file content
    test_content = """
    # This is a comment
    192.168.1.1:8080
    192.168.1.2:8080
    
    http://user:pass@192.168.1.3:8080
    invalid_line
    """
    
    print("📝 Test 2: Parse Proxy Content")
    parsed = ProxyHandler.parse_proxy_file_content(test_content)
    print(f"  Parsed {len(parsed)} proxies:")
    for p in parsed:
        print(f"    - {p}")
    
    print("\n✅ Proxy Handler tests completed!\n")

if __name__ == "__main__":
    asyncio.run(test_proxy_handler())