"""Index products from PostgreSQL to OpenSearch."""

import sys

from opensearchpy.helpers import bulk
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.config import settings
from src.db.database import sync_engine
from src.db.models import Product
from src.search.client import client, create_index

BATCH_SIZE = 1000


def product_to_doc(product: Product) -> dict:
    """Convert a Product model to an OpenSearch document."""
    doc = {
        "_index": settings.opensearch_index,
        "_id": product.supplier_aid,
        "supplier_aid": product.supplier_aid,
        "ean": product.ean,
        "manufacturer_aid": product.manufacturer_aid,
        "manufacturer_name": product.manufacturer_name,
        "description_short": product.description_short,
        "description_long": product.description_long,
        "delivery_time": product.delivery_time,
        "order_unit": product.order_unit,
        "price_quantity": product.price_quantity,
        "quantity_min": product.quantity_min,
        "eclass_id": product.eclass_id,
        "eclass_system": product.eclass_system,
    }

    # Add first price (primary price for search/filtering)
    if product.prices:
        price = product.prices[0]
        doc["price_amount"] = float(price.amount) if price.amount else None
        doc["price_currency"] = price.currency
        doc["price_type"] = price.price_type

    # Add first image
    if product.media:
        doc["image"] = product.media[0].source

    return doc


def index_all(recreate_index: bool = True) -> int:
    """
    Index all products from PostgreSQL to OpenSearch.

    Returns the number of documents indexed.
    """
    if recreate_index:
        create_index(delete_existing=True)

    count = 0

    with Session(sync_engine) as session:
        # Query with eager loading for prices and media
        offset = 0
        while True:
            stmt = (
                select(Product)
                .options(selectinload(Product.prices), selectinload(Product.media))
                .offset(offset)
                .limit(BATCH_SIZE)
            )
            products = session.scalars(stmt).all()

            if not products:
                break

            docs = [product_to_doc(p) for p in products]
            success, _ = bulk(client, docs, raise_on_error=False)
            count += success
            offset += BATCH_SIZE

            print(f"Indexed {count:,} documents...", file=sys.stderr)

    # Refresh index to make documents searchable
    client.indices.refresh(index=settings.opensearch_index)

    return count


def main() -> None:
    print("Starting full index...", file=sys.stderr)
    count = index_all(recreate_index=True)
    print(f"Done. Indexed {count:,} products.", file=sys.stderr)


if __name__ == "__main__":
    main()
