#!/bin/bash
#!/bin/bash
echo "🚀 Starting ProjectGuard backend..."
uvicorn backend.main:app --host 0.0.0.0 --port 10000
