"""
URL Extraction & Heuristic Checks (Day 5)

Two-path design, same pattern as Day 4's header parser:

1. extract_urls_from_text() - for plain-text bodies (what our labeled
   datasets - CEAS_08, SpamAssassin - actually contain; confirmed by
   inspection that `body` holds URLs as plain text, not HTML markup).

2. extract_links_from_html() - for real HTML email bodies (production
   .eml input), where the visible anchor text and the actual destination
   (href) can differ - the "mismatched link" spoofing technique.

Known limitation (documented, not hidden): our labeled datasets are
plain-text, so the anchor-text-vs-href mismatch check can only be
validated on synthetic HTML examples, not evaluated at scale on the
labeled data. This mirrors the Day 4 Received-chain limitation.

VirusTotal reputation lookup is intentionally kept in a SEPARATE function
(check_url_reputation) since it requires network access and an API key -
the heuristic checks below work standalone, with no external dependency.
"""
import re
from urllib.parse import urlparse

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

# Matches http(s):// URLs in plain text
URL_REGEX = re.compile(r'https?://[^\s<>"\')\]]+')

KNOWN_SHORTENERS = {
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly",
    "is.gd", "buff.ly", "adf.ly", "shorte.st",
}

IP_LITERAL_REGEX = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')


def extract_urls_from_text(text: str) -> list:
    """Extract raw URLs from plain-text email body via regex."""
    if not isinstance(text, str):
        return []
    return URL_REGEX.findall(text)


def extract_links_from_html(html: str) -> list:
    """
    Extract (visible_text, href) pairs from real HTML email content.
    Requires beautifulsoup4 (pip install beautifulsoup4).
    """
    if not HAS_BS4:
        raise ImportError("beautifulsoup4 is required for HTML parsing. Run: pip install beautifulsoup4")
    soup = BeautifulSoup(html or "", "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        visible_text = a.get_text(strip=True)
        links.append({"visible_text": visible_text, "href": a["href"]})
    return links


def _get_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


# A real domain contains only letters, digits, hyphens, and dots.
# If urlparse's netloc contains anything else, it likely swallowed
# stray characters from a malformed URL (e.g. a missing '?' before
# query parameters causes '&param=x' to be glued onto the domain).
VALID_DOMAIN_CHARS_REGEX = re.compile(r'^[a-z0-9.\-]+$')


def analyze_url(url: str) -> dict:
    """Run standalone heuristic checks on a single URL (no network needed).

    Design note (Day 5 finding): a malformed URL structure (e.g. a missing
    '?' before '&param=x') is common in legitimate bulk/marketing email
    tracking links, and is NOT on its own good evidence of phishing.
    It is recorded as a flag (a useful feature for the Week 3 classifier
    to weigh) but does NOT set `suspicious=True` by itself - only the
    stronger, more specific signals below do that.
    """
    domain = _get_domain(url)
    domain_no_port = domain.split(":")[0]

    flags = []
    strong_signal = False  # only these drive `suspicious=True`

    if domain_no_port and not VALID_DOMAIN_CHARS_REGEX.match(domain_no_port):
        flags.append("malformed_url_structure")
        # Weak signal only - salvage the part before the first invalid
        # character so IP/shortener/length checks can still run on it.
        domain_no_port = re.split(r'[^a-z0-9.\-]', domain_no_port)[0]

    if IP_LITERAL_REGEX.match(domain_no_port):
        flags.append("ip_literal_domain")
        strong_signal = True

    if domain_no_port in KNOWN_SHORTENERS:
        flags.append("known_url_shortener")
        # intentionally weak - shorteners appear in both classes (Day 5 finding)

    if len(domain_no_port) > 40:
        flags.append("unusually_long_domain")
        strong_signal = True

    if domain_no_port.count("-") >= 3:
        flags.append("excessive_hyphens_in_domain")
        strong_signal = True

    return {"url": url, "domain": domain_no_port, "flags": flags, "suspicious": strong_signal}

def analyze_anchor_mismatch(visible_text: str, href: str) -> dict:
    """
    Compares visible link text to actual destination - the classic
    'says paypal.com, goes elsewhere' spoofing technique from Day 5's
    opening discussion. Only meaningful when visible_text itself looks
    like a URL/domain claim.
    """
    text_urls = URL_REGEX.findall(visible_text) or (
        [visible_text] if re.match(r'^(www\.)?[\w-]+\.\w+', visible_text.strip()) else []
    )
    if not text_urls:
        return {"mismatch": False, "reason": "visible text is not a URL/domain claim"}

    visible_domain = _get_domain(text_urls[0]) or text_urls[0].split("/")[0]
    actual_domain = _get_domain(href)

    mismatch = visible_domain.lower().lstrip("www.") != actual_domain.lower().lstrip("www.")
    return {
        "mismatch": mismatch,
        "visible_domain": visible_domain,
        "actual_domain": actual_domain,
    }


def analyze_email_urls(text_body: str) -> dict:
    """Full analysis of all URLs found in a plain-text email body."""
    urls = extract_urls_from_text(text_body)
    results = [analyze_url(u) for u in urls]
    return {
        "url_count": len(urls),
        "suspicious_count": sum(1 for r in results if r["suspicious"]),
        "details": results,
    }


if __name__ == "__main__":
    # Sanity tests before running on real data
    print("--- Plain text extraction ---")
    sample_body = "Buck up! Visit http://whitedone.com/ now or http://192.168.1.5/login"
    print(analyze_email_urls(sample_body))

    print()
    print("--- HTML anchor mismatch (synthetic) ---")
    if HAS_BS4:
        html = '<a href="http://totally-fake-bank.ru/steal">www.paypal.com</a>'
        links = extract_links_from_html(html)
        for link in links:
            print(link, "->", analyze_anchor_mismatch(link["visible_text"], link["href"]))
    else:
        print("beautifulsoup4 not installed yet - run: pip install beautifulsoup4")