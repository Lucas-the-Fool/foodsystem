# -*- coding: utf-8 -*- 
# @File : content_process.py 
def front_user(request):
    login_in = request.session.get('login_in')
    content = {}
    if login_in:
        user = {
            'username': request.session.get('username'),
            'user_id': request.session.get('user_id'),
        }
        content['front_user'] = user

    return content
