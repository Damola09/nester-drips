import asyncio

# Global concurrency control for AI calls
# Limit to 10 concurrent requests to prevent overwhelming the AI provider and manage costs
ai_semaphore = asyncio.Semaphore(10)
