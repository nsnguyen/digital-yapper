#!/bin/bash

# Connect to the SQLite database and show conversations
echo "=== CONVERSATIONS TABLE ==="
docker exec backend-dev-1 sqlite3 /app/backend/conversations.db "SELECT * FROM conversations;"

echo -e "\n=== MESSAGES TABLE ==="
docker exec backend-dev-1 sqlite3 /app/backend/conversations.db "SELECT conversation_id, role, substr(content, 1, 50) || '...' as content_preview, created_at FROM messages ORDER BY created_at;"

echo -e "\n=== LATEST CONVERSATION MESSAGES ==="
docker exec backend-dev-1 sqlite3 /app/backend/conversations.db "
SELECT role, content, created_at 
FROM messages 
WHERE conversation_id = (SELECT id FROM conversations ORDER BY created_at DESC LIMIT 1)
ORDER BY created_at;
"
