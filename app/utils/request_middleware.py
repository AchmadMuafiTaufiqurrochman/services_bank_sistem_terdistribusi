from fastapi import HTTPException, status
import httpx
from urllib.parse import urljoin

from app.core.config import settings


async def send_to_middleware(
	payload: dict,
	*,
	path: str | None = None,
	timeout: float = 10.0,
) -> dict:
	"""Kirim payload ke middleware dengan header secret key dan dukungan path dinamis."""
	base_url = settings.ENDPOINT_API_MIDDLEWARE
	if not base_url:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="URL middleware belum dikonfigurasi"
		)

	target_url = base_url
	if path:
		base = base_url if base_url.endswith("/") else f"{base_url}/"
		target_url = urljoin(base, path.lstrip("/"))

	secret = settings.MIDDLEWARE_SECRET_KEY
	if not secret:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Secret key middleware belum dikonfigurasi"
		)

	headers = {"Authorization": f"Bearer {secret}"}

	try:
		async with httpx.AsyncClient(timeout=timeout) as client:
			response = await client.post(target_url, json=payload, headers=headers)
			response.raise_for_status()
			return response.json()
	except httpx.HTTPStatusError as exc:
		error_detail = "Middleware menolak permintaan"
		try:
			error_json = exc.response.json()
			if "detail" in error_json:
				error_detail = f"Middleware: {error_json['detail']}"
		except:
			error_detail = f"Middleware error: {exc.response.text}"
			
		raise HTTPException(
			status_code=exc.response.status_code,
			detail=error_detail
		) from exc
	except httpx.HTTPError as exc:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail="Gagal menghubungi middleware"
		) from exc
