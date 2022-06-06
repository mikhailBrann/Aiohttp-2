from aiohttp import web
import asyncpg
import bcrypt
import json
from lib.err_handler import HttpError
from lib.models import UserModel, AdvertisementModel


class UserView(web.View):
    # request лежит в self
    async def get(self):
            if 'user_id' in self.request.match_info:
                try:
                    user_id = int(self.request.match_info['user_id'])
                    new_user = await UserModel.get(user_id)

                    return web.json_response({
                        'id': new_user.id,
                        'name': new_user.username
                    })

                except AttributeError:
                    raise HttpError(text=json.dumps({'error': 'user not found'}))
            else:
                users = await UserModel.query.gino.all()
                result = dict()

                for user in users:
                    result[user.id] = {
                        "id": user.id,
                        "username": user.username,
                        "is_authorized": user.is_authorized
                    }

                return web.json_response(result)

    async def post(self):
        user_data = await self.request.json()
        user_data['password'] = bcrypt.hashpw(user_data['password'].encode(), bcrypt.gensalt()).decode()

        try:
            new_user = await UserModel.create(**user_data)

        except asyncpg.exceptions.UniqueViolationError:
            raise HttpError(text=json.dumps({'error': 'user with same name already exists'}))

        return web.json_response({
            'id': new_user.id,
            'name': new_user.username
        })

    async def patch(self):
        user_data = await self.request.json()
        try:
            current_user = await UserModel.query.where(UserModel.username == user_data['username']).gino.first()
            check_pass = bcrypt.checkpw(user_data['password'].encode(), current_user.password.encode())

            if check_pass:
                await current_user.update(is_authorized=True).apply()
                return web.json_response({'sucefull': f'user {current_user.username} autorized!'})
            else:
                raise HttpError(text=json.dumps({'error': 'password incorrect'}))

        except AttributeError:
            raise HttpError(text=json.dumps({'error': 'login incorrect'}))


class AdvertisementView(web.View):

    async def get(self):
        adv_list = await AdvertisementModel.query.gino.all()
        result = dict()

        for adv in adv_list:
            result[adv.id] = {
                'title': adv.title,
                'description': adv.description,
                'owner': adv.owner
            }

        return web.json_response(result)

    async def post(self):
        adv_data = await self.request.json()
        owner = await UserModel.query.where(UserModel.id == adv_data['owner']).gino.first()

        if owner:
            if owner.is_authorized:
                new_adv = await AdvertisementModel.create(**adv_data)
            else:
                raise HttpError(text=json.dumps({'error': f"user with id={adv_data['owner']} do not authorized!"}))
        else:
            raise HttpError(text=json.dumps({'error': f"user with id={adv_data['owner']} do not exists"}))

        return web.json_response({
            'id': new_adv.id,
            'title': new_adv.title
        })

    async def patch(self):
        adv_data = await self.request.json()
        owner = await UserModel.query.where(UserModel.id == adv_data['owner']).gino.first()
        current_adv = await AdvertisementModel.query.where(AdvertisementModel.id == adv_data['id']).gino.first()

        try:
            if owner.id == current_adv.owner:
                if 'title' in adv_data:
                    await current_adv.update(title=adv_data['title']).apply()
                if 'description' in adv_data:
                    await current_adv.update(description=adv_data['description']).apply()

                return web.json_response({'sucefull': f"ad(id={current_adv.id}) updated successfully"})

        except AttributeError:
            raise HttpError(text=json.dumps({
                'error': f"user(id={adv_data['owner']}) is not the owner of the ad(id={adv_data['id']})"
            }))

    async def delete(self):
        adv_data = await self.request.json()
        owner = await UserModel.query.where(UserModel.id == adv_data['owner']).gino.first()
        current_adv = await AdvertisementModel.query.where(AdvertisementModel.id == adv_data['id']).gino.first()

        try:
            if owner.id == current_adv.owner:
                await current_adv.delete()
                return web.json_response({'sucefull': f"ad(id={current_adv.id}) delete"})

        except AttributeError:
            raise HttpError(text=json.dumps({
                'error': f"user(id={adv_data['owner']}) is not the owner of the ad(id={adv_data['id']})"
            }))
