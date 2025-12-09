"""OpenSearch index mapping for products."""

INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "autocomplete_tokenizer",
                    "filter": ["lowercase"],
                },
                "autocomplete_search": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase"],
                },
            },
            "tokenizer": {
                "autocomplete_tokenizer": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 20,
                    "token_chars": ["letter", "digit"],
                }
            },
        },
    },
    "mappings": {
        "properties": {
            "supplier_aid": {"type": "keyword"},
            "ean": {"type": "keyword"},
            "manufacturer_aid": {"type": "keyword"},
            "manufacturer_name": {
                "type": "text",
                "analyzer": "german",
                "fields": {"keyword": {"type": "keyword"}},
            },
            "description_short": {
                "type": "text",
                "analyzer": "german",
                "fields": {
                    "autocomplete": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "search_analyzer": "autocomplete_search",
                    }
                },
            },
            "description_long": {"type": "text", "analyzer": "german"},
            "delivery_time": {"type": "integer"},
            "order_unit": {"type": "keyword"},
            "price_quantity": {"type": "integer"},
            "quantity_min": {"type": "integer"},
            "eclass_id": {"type": "keyword"},
            "eclass_system": {"type": "keyword"},
            "price_amount": {"type": "float"},
            "price_currency": {"type": "keyword"},
            "price_type": {"type": "keyword"},
            "image": {"type": "keyword"},
        }
    },
}
