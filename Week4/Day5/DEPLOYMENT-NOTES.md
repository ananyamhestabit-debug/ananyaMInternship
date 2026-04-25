# Deployment Notes

1. Install dependencies
npm install

2. Setup environment
cp .env.example .env.local

3. Start Redis
redis-server

4. Start API
node server.js

5. Start Worker (separate terminal)
node src/jobs/email.worker.js

6. For production:
pm2 start prod/ecosystem.config.js