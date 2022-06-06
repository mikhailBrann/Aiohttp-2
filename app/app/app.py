from aiohttp import web
from lib.settings import app, db, DB_URL
from lib.views import UserView, AdvertisementView


# функция отслеживает этапы состояния приложения
async def orm_context(app):
    print('app start')
    # подключаемся к БД
    await db.set_bind(DB_URL)
    # делаем миграцию
    await db.gino.create_all()
    yield
    # закрываем подключение к бд
    await db.pop_bind().close()
    print('app close')


# route
app.router.add_routes(
    [
        web.get('/users/{user_id:\d+}', UserView),
        web.get('/users/', UserView),
        web.post('/users/', UserView),
        web.patch('/users/', UserView),
        web.delete('/users/{user_id:\d+}', UserView),
        web.get('/advertisement/', AdvertisementView),
        web.post('/advertisement/', AdvertisementView),
        web.patch('/advertisement/', AdvertisementView),
        web.delete('/advertisement/', AdvertisementView)
    ]
)

# запускаем приложение
app.cleanup_ctx.append(orm_context)
web.run_app(app)

