"""Pydantic schemas for API requests and responses."""

from pydantic import BaseModel, Field


class ProductResult(BaseModel):
    """Product in search results."""

    supplier_aid: str
    ean: str | None = None
    manufacturer_aid: str | None = None
    manufacturer_name: str | None = None
    description_short: str | None = None
    description_long: str | None = None
    eclass_id: str | None = None
    price_amount: float | None = None
    price_currency: str | None = None
    image: str | None = None


class FacetBucket(BaseModel):
    """A single facet value with count."""

    value: str
    count: int


class Facets(BaseModel):
    """Available facet values."""

    manufacturers: list[FacetBucket] = []
    eclass_ids: list[FacetBucket] = []


class SearchResponse(BaseModel):
    """Search results response."""

    total: int
    page: int
    size: int
    results: list[ProductResult]
    facets: Facets


class AutocompleteResponse(BaseModel):
    """Autocomplete suggestions."""

    suggestions: list[str]


class SearchRequest(BaseModel):
    """Search query parameters."""

    q: str | None = Field(None, description="Search query text")
    manufacturer: str | None = Field(None, description="Filter by manufacturer name")
    eclass_id: str | None = Field(None, description="Filter by ECLASS ID")
    price_min: float | None = Field(None, ge=0, description="Minimum price filter")
    price_max: float | None = Field(None, ge=0, description="Maximum price filter")
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Results per page")
