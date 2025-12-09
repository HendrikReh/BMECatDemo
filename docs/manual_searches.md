# Manual Search Tests

curl commands to verify OpenSearch functionality. Run these against `http://localhost:9019`.

> **Note:** For queries with German umlauts, use `-G --data-urlencode` to properly encode the URL.

## Basic Searches

### 1. Empty search (all products)

```bash
curl -s "http://localhost:9019/api/v1/search" | jq '.total, .results[:2]'
```

### 2. Simple text search

```bash
curl -s "http://localhost:9019/api/v1/search?q=Kabel" | jq '.total, .results[:3]'
```

### 3. German compound word search

```bash
curl -s -G "http://localhost:9019/api/v1/search" --data-urlencode "q=Trägerklammer" | jq '.total, .results[:3]'
```

### 4. Search with special characters

```bash
curl -s "http://localhost:9019/api/v1/search?q=M6x9" | jq '.total, .results[:3]'
```

### 5. Multi-word search

```bash
curl -s "http://localhost:9019/api/v1/search?q=Federstahl%20Klammer" | jq '.total, .results[:3]'
```

## Filtered Searches

### 6. Filter by manufacturer

```bash
curl -s "http://localhost:9019/api/v1/search?manufacturer=Walraven%20GmbH" | jq '.total, .results[:3]'
```

### 7. Filter by ECLASS ID

```bash
curl -s "http://localhost:9019/api/v1/search?eclass_id=23140307" | jq '.total, .results[:3]'
```

### 8. Filter by price range (low)

```bash
curl -s "http://localhost:9019/api/v1/search?price_min=0&price_max=100" | jq '.total, .results[:3]'
```

### 9. Filter by price range (mid)

```bash
curl -s "http://localhost:9019/api/v1/search?price_min=100&price_max=500" | jq '.total, .results[:3]'
```

### 10. Filter by price range (high)

```bash
curl -s "http://localhost:9019/api/v1/search?price_min=500" | jq '.total, .results[:3]'
```

## Combined Searches

### 11. Text search + manufacturer filter

```bash
curl -s "http://localhost:9019/api/v1/search?q=Klammer&manufacturer=Walraven%20GmbH" | jq '.total, .results[:3]'
```

### 12. Text search + price range

```bash
curl -s "http://localhost:9019/api/v1/search?q=Kabel&price_min=50&price_max=200" | jq '.total, .results[:3]'
```

### 13. Text search + ECLASS filter

```bash
curl -s "http://localhost:9019/api/v1/search?q=Stahl&eclass_id=23140307" | jq '.total, .results[:3]'
```

### 14. Multiple filters (no text)

```bash
curl -s "http://localhost:9019/api/v1/search?manufacturer=Walraven%20GmbH&price_min=300&price_max=400" | jq '.total, .results[:3]'
```

### 15. All filters combined

```bash
curl -s "http://localhost:9019/api/v1/search?q=Klammer&manufacturer=Walraven%20GmbH&eclass_id=23140307&price_min=100&price_max=500" | jq '.total, .results[:3]'
```

## Pagination

### 16. First page (default)

```bash
curl -s "http://localhost:9019/api/v1/search?size=5" | jq '.page, .size, .total, (.results | length)'
```

### 17. Second page

```bash
curl -s "http://localhost:9019/api/v1/search?page=2&size=5" | jq '.page, .size, .total, (.results | length)'
```

### 18. Large page size

```bash
curl -s "http://localhost:9019/api/v1/search?size=100" | jq '.page, .size, .total, (.results | length)'
```

## Autocomplete

### 19. Autocomplete short query

```bash
curl -s "http://localhost:9019/api/v1/search/autocomplete?q=Kab" | jq '.suggestions[:5]'
```

### 20. Autocomplete longer query

```bash
curl -s -G "http://localhost:9019/api/v1/search/autocomplete" --data-urlencode "q=Träger" | jq '.suggestions[:5]'
```

## Other Endpoints

### Get single product by ID

```bash
curl -s "http://localhost:9019/api/v1/products/1000864" | jq '.'
```

### Get all facets

```bash
curl -s "http://localhost:9019/api/v1/facets" | jq '.manufacturers[:10], .eclass_ids[:10]'
```

### Check facets in search response

```bash
curl -s "http://localhost:9019/api/v1/search?q=Kabel" | jq '.facets'
```

## Verification Checklist

- [ ] Empty search returns products
- [ ] Text search returns relevant results
- [ ] German words are matched correctly
- [ ] Filters reduce result count
- [ ] Combined filters work together
- [ ] Pagination returns correct pages
- [ ] Autocomplete returns suggestions
- [ ] Facets show aggregated counts
