import aiohttp_jinja2

from dnscockpit.auth import login_required


@login_required
@aiohttp_jinja2.template('index.html')
async def index(request):
    return {'date': '2018-08-03'}


@aiohttp_jinja2.template('login.html')
async def login(request):
    return {'date': '2018-08-03'}
