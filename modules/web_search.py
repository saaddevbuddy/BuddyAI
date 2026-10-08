# ==========================================================
# Buddy AI - Web Search
# Internet Search Helper
# ==========================================================

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse, parse_qs


# ==========================================================
# SEARCH ENGINE
# ==========================================================

SEARCH_URL = "https://html.duckduckgo.com/html/?q="

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


# ==========================================================
# CLEAN LINK
# ==========================================================

def clean_link(link):

    if not link:
        return ""

    link = str(link).strip()

    # DuckDuckGo redirect URL
    if "uddg=" in link:

        try:

            parsed = urlparse(link)

            query = parse_qs(
                parsed.query
            )

            if "uddg" in query:
                return query["uddg"][0]

        except Exception:
            pass

    return link


# ==========================================================
# SEARCH
# ==========================================================

def web_search(query, max_results=5):

    if not query:
        return None

    query = str(query).strip()

    if not query:
        return None

    print(
        "\n[Web Search] Searching:",
        query
    )

    try:

        url = SEARCH_URL + quote(query)

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        print(
            "[Web Search] HTTP:",
            response.status_code
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        # ==================================================
        # METHOD 1
        # Normal DuckDuckGo HTML results
        # ==================================================

        blocks = soup.select(
            ".result"
        )

        # ==================================================
        # METHOD 2
        # Alternate result containers
        # ==================================================

        if not blocks:

            blocks = soup.select(
                ".results .result"
            )

        # ==================================================
        # PARSE RESULTS
        # ==================================================

        for block in blocks:

            title_tag = (
                block.select_one(".result__title")
                or block.select_one("h2")
                or block.select_one("h3")
            )

            link_tag = (
                block.select_one(".result__a")
                or block.select_one("a[href]")
            )

            if not title_tag or not link_tag:
                continue

            title = title_tag.get_text(
                " ",
                strip=True
            )

            link = link_tag.get(
                "href",
                ""
            )

            link = clean_link(link)

            snippet_tag = (
                block.select_one(".result__snippet")
                or block.select_one(".result__body")
                or block.select_one(".snippet")
            )

            snippet = ""

            if snippet_tag:

                snippet = snippet_tag.get_text(
                    " ",
                    strip=True
                )

            if not title:
                continue

            results.append({
                "title": title,
                "snippet": snippet,
                "link": link
            })

            if len(results) >= max_results:
                break

        # ==================================================
        # DEBUG
        # ==================================================

        print(
            "[Web Search] Parsed results:",
            len(results)
        )

        # ==================================================
        # NO RESULTS
        # ==================================================

        if not results:

            print(
                "[Web Search] No usable results found."
            )

            return None

        print(
            "[Web Search] Results:",
            len(results)
        )

        return results

    except requests.exceptions.Timeout:

        print(
            "[Web Search] Request timed out."
        )

        return None

    except requests.exceptions.RequestException as e:

        print(
            "[Web Search] Network error:",
            repr(e)
        )

        return None

    except Exception as e:

        print(
            "[Web Search] Error:",
            repr(e)
        )

        return None


# ==========================================================
# FORMAT RESULTS FOR AI
# ==========================================================

def format_search_results(results):

    if not results:
        return ""

    lines = []

    for index, result in enumerate(
        results,
        start=1
    ):

        title = result.get(
            "title",
            ""
        )

        snippet = result.get(
            "snippet",
            ""
        )

        link = result.get(
            "link",
            ""
        )

        lines.append(
            f"{index}. {title}\n"
            f"Info: {snippet}\n"
            f"Link: {link}"
        )

    return "\n\n".join(lines)


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    print(
        "\n========== BUDDY WEB SEARCH TEST ==========\n"
    )

    query = input(
        "Search: "
    ).strip()

    if not query:

        print(
            "\nNo search query entered."
        )

        raise SystemExit

    results = web_search(
        query,
        max_results=5
    )

    if results:

        print(
            "\n========== RESULTS ==========\n"
        )

        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"[{index}] {result['title']}"
            )

            print(
                "INFO:",
                result["snippet"]
            )

            print(
                "LINK:",
                result["link"]
            )

            print(
                "-" * 60
            )

    else:

        print(
            "\nNo search results."
        )