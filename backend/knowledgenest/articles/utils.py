from typing import Dict
import requests
from bs4 import BeautifulSoup

from knowledgenest.articles.models import Article


def extract_meta_properties(url: str) -> Dict[str, str]:
    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.content

        soup = BeautifulSoup(page_content, "html.parser")

        og_properties = soup.find_all(
            "meta", attrs={"property": lambda x: x and x.startswith("og:")}
        )
        data = {meta["property"][3:]: meta["content"] for meta in og_properties}

        # If the meta description tag exists, extract the content attribute
        if "description" not in data.keys():
            meta_description = soup.find("meta", attrs={"name": "description"})
            if meta_description:
                data["description"] = meta_description["content"]

        if "title" not in data.keys():
            title = soup.find("title")
            if title:
                data["title"] = title.text

        # If any og properties were found, return them along with the meta description
        return data
    else:
        # TODO raise error properly
        return {}


# Mapping of properties to fields
def convert_properties_to_fields(property_data: Dict[str, str]) -> Dict[str, str]:
    to_ret = property_data.copy()
    extracted_keys = list(to_ret.keys())
    if "image" in extracted_keys:
        to_ret["imageUrl"] = to_ret["image"]
    for key in extracted_keys:
        if key not in Article.__table__.columns:
            to_ret.pop(key)
    return to_ret
