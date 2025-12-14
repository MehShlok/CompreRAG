from supabase import create_client, Client
from config import settings

if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
    raise ValueError("Supabase URL and Service Key must be set in environment variables")

# Use service_role key to bypass RLS - backend is trusted
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
