from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")


async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """Validate API key and return if valid."""
    if not api_key.startswith("sk_"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


async def get_context(api_key: str = Security(api_key_header)):
    """Create GraphQL context with validated API key."""
    return {"api_key": await get_api_key(api_key)}
