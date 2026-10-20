"""Read Drive folders shared as "Anyone with the link can view", without an API key."""
import html
import re
import subprocess

ENTRY = re.compile(r'id="entry-([\w-]+)".*?<a href="([^"]+)".*?flip-entry-title">(.*?)</div>'
                   r'.*?flip-entry-last-modified"><div>(.*?)</div>', re.S)


def walk(folder_id, path=""):
    """Yield (file_id, path/name, last_modified) for every file under folder_id, subfolders included."""
    page = subprocess.run(["curl", "-sSL", f"https://drive.google.com/embeddedfolderview?id={folder_id}"],
                          capture_output=True, text=True, check=True).stdout
    for fid, href, title, modified in ENTRY.findall(page):
        title = html.unescape(title)
        if "/folders/" in href:
            yield from walk(fid, f"{path}{title}/")
        else:
            yield fid, path + title, html.unescape(modified)


def download(file_id, dest):
    subprocess.run(["curl", "-sSL", "--fail", "-o", dest,
                    f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"],
                   check=True)
