from __future__ import annotations

from supabase import Client, create_client
from django.conf import settings


def get_supabase_client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise RuntimeError("Supabase configuration is missing.")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
