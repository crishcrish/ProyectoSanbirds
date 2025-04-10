import psycopg2

try:
    conn = psycopg2.connect("postgresql://postgres.bzvktbhtlngjodfdpyqs:XwE56J0CjqMDstvY@aws-0-us-east-2.pooler.supabase.com:6543/postgres")
    print("✅ Conectado correctamente")
    conn.close()
except Exception as e:
    print(f"❌ Error al conectar: {e}")
