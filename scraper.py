# deploying web scraper

import json
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import datetime

load_dotenv()

# define a pydantic class outlining details we want to scrap from each product

# The Field description is crucial in telling LLM on what exactly to look for
# This LLM approach reduces development time as you do not have to manually inspect
# HTML structures; also providing long-lasting resilience against HTML changes


class Product(BaseModel):
    name: str = Field(description="The name of the product")
    description: str = Field(description="A short description of the product")
    url: str = Field(description="The URL of the product")

    topics: list[str] = Field(
        description="A list of topics the product belongs to. Can be found below the product description."
    )

    n_upvotes: int = Field(description="The number of upvotes the product has")
    n_comments: int = Field(description="The number of comments the product has")

    rank: int = Field(
        description="The rank of the product on Product Hunt's Yesterday's Top Products section."
    )
    logo_url: str = Field(description="The URL of the product's logo.")

# a pydantic class for crawling a collection of Products from Yesterday's Top 
# Product list

class YesterdayTopProducts(BaseModel):
    products: list[Product] = Field(
        description="A list of top products from yesterday on Product Hunt."
    )

# Define a function that scrapes ProductHunt based on the schema above
# the function initializes Firecrawlapp which reads your Firecrawl API key

BASE_URL = "https://www.producthunt.com"


def get_yesterday_top_products():
    app = FirecrawlApp()

    data = app.scrape_url(
        BASE_URL,
        params={
            "formats": ["extract"],
            "extract": {
                "schema": YesterdayTopProducts.model_json_schema(),

                "prompt": "Extract the top products listed under the 'Yesterday's Top Products' section. There will be exactly 5 products.",
            },
        },
    )

    return data["extract"]["products"]

# formats specify how the data should be scraped and extracted
# schema is the JSON schema produced by pydantic class
# promt guides LLM on what to do

# finally write a function to save the JSON file

def save_yesterday_top_products():
    products = get_yesterday_top_products()

    date_str = datetime.now().strftime("%Y_%m_%d")
    filename = f"ph_top_products_{date_str}.json"

    with open(filename, "w") as f:
        json.dump(products, f)

if __name__ == "__main__":
    save_yesterday_top_products()