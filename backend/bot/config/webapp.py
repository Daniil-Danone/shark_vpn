from aiohttp import web
from prometheus_client import generate_latest


def metric_view(request):
    data = generate_latest()
    if isinstance(data, str):
        data = data.encode("utf-8")

    return web.Response(body=data, content_type="text/plain")


async def start_server():
    app = web.Application()
    app.router.add_get("/metrics/", metric_view)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host="0.0.0.0", port=8080)
    await site.start()
