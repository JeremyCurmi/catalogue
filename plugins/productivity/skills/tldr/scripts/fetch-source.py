#!/usr/bin/env python3
"""Print the full text of an X post to stdout.

X is the case that needs code: WebFetch gets 402 from x.com, and an X Article
(long-form post) is not in the page HTML anyway. api.fxtwitter.com returns the post
and, for an Article, its full block content.

Usage: fetch-source.py <x-url>
Exit 2 = not an X post url, fetch it with WebFetch instead.
"""

import json
import re
import sys
import urllib.error
import urllib.request

X_STATUS = re.compile(r"https?://(?:www\.|mobile\.)?(?:x|twitter)\.com/([^/]+)/status/(\d+)")
MARKS = {"header-one": "# ", "header-two": "## ", "header-three": "### ",
         "unordered-list-item": "- ", "ordered-list-item": "- ", "blockquote": "> "}


def render_article(art):
    lines = [f"# {art['title']}", ""]
    for block in art["content"]["blocks"]:
        text = block.get("text", "").strip()
        if text:
            lines.append(MARKS.get(block.get("type"), "") + text)
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: fetch-source.py <x-url>")
    match = X_STATUS.match(sys.argv[1])
    if not match:
        print("not an x.com post url — fetch this one with WebFetch", file=sys.stderr)
        sys.exit(2)

    api = f"https://api.fxtwitter.com/{match.group(1)}/status/{match.group(2)}"
    try:
        req = urllib.request.Request(api, headers={"User-Agent": "curl/8"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            tweet = json.load(resp)["tweet"]
    except urllib.error.HTTPError as err:
        body = json.loads(err.read() or b"{}")
        sys.exit(f"fxtwitter {err.code}: {body.get('message', 'no detail')} — "
                 "post deleted, private, or the id is wrong")

    print(f"[@{tweet['author']['screen_name']} · {tweet['created_at']} · "
          f"{tweet['views']} views · {tweet['likes']} likes · {tweet['bookmarks']} bookmarks]\n")

    if tweet.get("article"):
        print(render_article(tweet["article"]))
        return

    # plain or long post: `text` already holds the full body, t.co links included
    print(tweet.get("text") or tweet["raw_text"]["text"])
    if "t.co/" in (tweet.get("text") or ""):
        print("\n[contains a t.co link — WebFetch it, the destination is usually the real source]",
              file=sys.stderr)


if __name__ == "__main__":
    main()
