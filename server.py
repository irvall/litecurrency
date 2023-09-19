from fastapi import Depends, FastAPI, HTTPException, Security
from decimal import Decimal
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Dict, List
from starlette import status
from requests import get

CURRENCY_API_VERSION = "v3"
CURRENCY_API_URI = "https://api.currencyapi.com"
CURRENCIES = "currencies"
LATEST = "latest"

X_API_KEY = APIKeyHeader(name='X-API-Key')
app = FastAPI(
    title="LiteCurrencyAPI",
    description="A small REST API for fetching currencies, and converting between them."
)


class ExchangeRate(BaseModel):
    code: str
    value: Decimal


class CurrencyInfo(BaseModel):
    symbol: str
    name: str
    symbol_native: str
    decimal_digits: int
    rounding: int
    code: str
    name_plural: str


class LatestResponse(BaseModel):
    meta: object
    data: Dict[str, ExchangeRate]


class CurrencyResponse(BaseModel):
    data: Dict[str, CurrencyInfo]


ENDPOINTS = {
    CURRENCIES: CurrencyResponse,
    LATEST: LatestResponse
}


def fetch_response(endpoint: str, api_key=Security(X_API_KEY)):
    if endpoint not in ENDPOINTS:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unsupported endpoint '/{endpoint}'")
    response_model = ENDPOINTS[endpoint]
    request_url = f"{CURRENCY_API_URI}/{CURRENCY_API_VERSION{endpoint}"
    response = get(request_url, headers={'Accept': 'application/json', 'apikey': api_key})
    if response.status_code == status.HTTP_200_OK:
        response_json = response.json()
        return response_model(**response_json)
    raise HTTPException(status_code=response.status_code, detail=response.content)


def get_currencies(api_key=Security(X_API_KEY)):
    return fetch_response(CURRENCIES, api_key)


def get_latest(api_key=Security(X_API_KEY)):
    return fetch_response(LATEST, api_key)


@app.get("/currencies")
def currencies(currency_response: CurrencyResponse = Depends(get_currencies)) -> List[CurrencyInfo]:
    """
    Retrieve a list of currencies.
    """
    currency_codes = list(currency_response.data.values())
    return currency_codes


@app.get("/convert")
def convert(source: str, target: str, amount: Decimal = Decimal(1),
            latest_rates: LatestResponse = Depends(get_latest),
            currency_data: CurrencyResponse = Depends(get_currencies)) -> str:
    """
    Convert amount (in source currency) to target currency.
    """
    source_key = source.upper().strip()
    target_key = target.upper().strip()
    if source_key not in latest_rates.data:
        raise HTTPException(status_code=404, detail=f"Source currency '{source_key}' was not found")
    if target_key not in latest_rates.data:
        raise HTTPException(status_code=404, detail=f"Target currency '{target_key}' was not found")

    source_rate = latest_rates.data[source_key]
    target_rate = latest_rates.data[target_key]
    target_info = currency_data.data[target_key]
    result = (target_rate.value / source_rate.value) * amount

    return f"{result:.10f} {target_info.symbol_native} ({target_info.name})"
