from supabase import create_client, Client
from config import settings

if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in environment variables")

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
