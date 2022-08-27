"""
Handlers utils.

This file contains commonly used utils.
"""
import abc
import os
import re
import mimetypes
import requests


def create_resource_folder(path: str) -> None:
    """
    Create the resource folder.

    :param path: a str containing the file path.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def extract_filename(url: str, headers: dict, extension: str = None) -> str:
    """
    Extract the filename from a url or request headers.

    :param url: a str containing a valid url.
    :param headers: a request headers dictionary.
    :param extension: an optional extension to remove from the filename.
    :return: a str containing the filename.
    """
    filename = (
        re.findall("filename=(.+)", headers.get("Content-Disposition"))[0]
        if "Content-Disposition" in headers
        else url.split("/")[-1]
    )

    if extension and filename.endswith(extension):
        filename = filename[: -len(extension)]

    return filename


def extract_file_extension(headers: dict) -> str:
    """
    Extract the file extension from a request headers.

    :param headers: a request headers dictionary.
    :return: a str containing the file extension.
    """
    content_type = headers.get("Content-Type").split(";")[0] if "Content-Type" in headers else ""
    file_extension = mimetypes.guess_extension(content_type)

    if file_extension == ".htm":
        file_extension = ".html"
    elif file_extension == ".jpe":
        file_extension = ".jpg"
    elif ".jpeg" in file_extension:
        file_extension = ".jpeg"

    return file_extension


@abc.abstractmethod
def _progress_cb(self, progress: int) -> None:
    pass


def download_request(url: str, path: str, filename: str, extension: str, progress_cb: _progress_cb = None) -> dict:
    """
    :param url: a url to download from.
    :param path: the path to store the file in.
    :param filename: the filename of the resource.
    :param extension: the extension of the resource.
    :param progress_cb: callback to post progress towards.
    :return: a dict containing the download results.
    """
    try:
        r = requests.get(url, stream=True)
        total = r.headers.get("content-length")
        chunk_size = 1024  # 1 MB
        chunks = 1
        dl = 0

        with open(f"{path}/{filename}{extension}", "wb+") as f:
            for chunk in r.iter_content(chunk_size):
                f.write(chunk)
                chunks += 1

                if total is not None and progress_cb:
                    progress_cb(int((dl / int(total)) * 100))
                    dl += chunk_size

        return {
            "success": True,
            "url": r.url,
            "total_size": total,
            "chunk_size": chunk_size,
            "chunks": chunks,
            "downloaded": dl,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
