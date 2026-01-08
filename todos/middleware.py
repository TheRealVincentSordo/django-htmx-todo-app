from __future__ import annotations

from typing import Any

import jwt
from django.conf import settings
from django.http import HttpRequest, HttpResponse

SESSION_KEY = "supabase_access_token"


class SupabaseAuthMiddleware:
    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        token = request.session.get(SESSION_KEY)
        request.supabase_user = None

        if token and settings.SUPABASE_JWT_SECRET:
            try:
                payload = jwt.decode(
                    token,
                    settings.SUPABASE_JWT_SECRET,
                    algorithms=["HS256"],
                    audience=settings.SUPABASE_JWT_AUDIENCE,
                )
                request.supabase_user = {
                    "id": payload.get("sub"),
                    "email": payload.get("email"),
                }
            except jwt.PyJWTError:
                request.session.pop(SESSION_KEY, None)

        response = self.get_response(request)
        return response
