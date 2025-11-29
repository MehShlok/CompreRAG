# Deployment Guide

## 1. Backend (Render)

1.  **Push to GitHub**: Ensure your code is pushed to a GitHub repository.
2.  **Create Web Service**:
    *   Go to [Render Dashboard](https://dashboard.render.com/).
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub repository.
    *   Select the `backend` directory as the **Root Directory**.
3.  **Environment Variables**:
    *   Add the following variables in the Render dashboard (under "Environment"):
        *   `SUPABASE_URL`: Your Supabase Project URL.
        *   `SUPABASE_KEY`: Your Supabase Anon Key.
        *   `SUPABASE_JWT_SECRET`: Your Supabase JWT Secret.
        *   `PINECONE_API_KEY`: Your Pinecone API Key.
        *   `PINECONE_ENVIRONMENT`: Your Pinecone Environment (e.g., `gcp-starter`).
        *   `PINECONE_INDEX_NAME`: Your Pinecone Index Name.
        *   `R2_ACCOUNT_ID`: Cloudflare Account ID.
        *   `R2_ACCESS_KEY_ID`: Cloudflare R2 Access Key ID.
        *   `R2_SECRET_ACCESS_KEY`: Cloudflare R2 Secret Access Key.
        *   `R2_BUCKET_NAME`: Your R2 Bucket Name.
4.  **Deploy**: Click **Create Web Service**.

## 2. Frontend (Vercel)

1.  **Import Project**:
    *   Go to [Vercel Dashboard](https://vercel.com/dashboard).
    *   Click **Add New...** -> **Project**.
    *   Import the same GitHub repository.
2.  **Configure Project**:
    *   **Framework Preset**: Next.js
    *   **Root Directory**: Edit and select `frontend`.
3.  **Environment Variables**:
    *   Add the following variables:
        *   `NEXT_PUBLIC_SUPABASE_URL`: Your Supabase Project URL.
        *   `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Your Supabase Anon Key.
        *   `NEXT_PUBLIC_API_URL`: The URL of your deployed Render backend (e.g., `https://rag-agent-backend.onrender.com`).
4.  **Deploy**: Click **Deploy**.

## 3. Supabase Setup

1.  **Database**: Run the following SQL in Supabase SQL Editor:
    ```sql
    create table documents (
      id uuid primary key,
      user_id uuid not null,
      filename text not null,
      storage_path text not null,
      status text not null,
      progress int default 0,
      chunk_count int default 0,
      created_at timestamptz default now()
    );

    alter table documents enable row level security;

    create policy "Users can see their own documents"
    on documents for select
    using (auth.uid() = user_id);

    create policy "Users can insert their own documents"
    on documents for insert
    with check (auth.uid() = user_id);

    create policy "Users can update their own documents"
    on documents for update
    using (auth.uid() = user_id);

    create policy "Users can delete their own documents"
    on documents for delete
    using (auth.uid() = user_id);
    ```
2.  **Realtime**: Go to **Database** -> **Replication** and enable replication for the `documents` table.

## 4. Cron Job (Keep-Alive)

1.  Go to [cron-job.org](https://cron-job.org/).
2.  Create a new cron job.
3.  **URL**: `https://<your-render-backend-url>/health`
4.  **Schedule**: Every 14 minutes.
