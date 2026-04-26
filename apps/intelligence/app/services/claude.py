import anthropic
from app.config import settings
from app.services.concurrency import ai_semaphore

# Use AsyncAnthropic for non-blocking I/O in FastAPI
client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

async def get_claude_response(*args, **kwargs):
    """
    Wrapper around Anthropic client to enforce global concurrency limits.
    """
    async with ai_semaphore:
        return await client.messages.create(*args, **kwargs)

async def get_claude_stream(*args, **kwargs):
    """
    Wrapper around Anthropic stream to enforce global concurrency limits.
    """
    async with ai_semaphore:
        async with client.messages.stream(*args, **kwargs) as stream:
            async for event in stream:
                yield event
