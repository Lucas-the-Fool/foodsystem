from django.shortcuts import render, redirect
from .models import MarkModel, CommentModel, HotModel, LikeModel, FoodModel, CategoryModel, UserInfoModel
from django.http import JsonResponse
import numpy as np
import os
from django.conf import settings
from utils.image_check import check_handle
import time


def index(request):
    # 首页
    hots = HotModel.objects.all()
    categories = CategoryModel.objects.all()
    context = {
        'hots': hots,
        'categories': categories
    }
    return render(request, 'index.html', context=context)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # 用户登录
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not (username or password):
            return JsonResponse({'code': 400, 'message': 'Required parameters are missing'})
        user = UserInfoModel.objects.filter(username=username, password=password).first()
        if not user:
            return JsonResponse({'code': 400, 'message': 'Wrong account or password'})
        request.session['login_in'] = True
        request.session['username'] = user.username
        request.session['user_id'] = user.id
        return JsonResponse({'code': 200})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if not (username or password1 or password2):
            return JsonResponse({'code': 400, 'message': 'Required parameters are missing'})

        if password1 != password2:
            return JsonResponse({'code': 400, 'message': 'The password entered twice does not match!'})

        flag = UserInfoModel.objects.filter(username=username).first()
        if flag:
            return JsonResponse({'code': 400, 'message': 'The username already exists'})
        UserInfoModel.objects.create(
            username=username,
            password=password1,
            address=address,
            phone=phone
        )
        return JsonResponse({'code': 200})


def logout(request):
    # 退出登录
    flag = request.session.clear()
    return redirect('/')


def food_detail(request, food_id):
    # 食物详情
    food = FoodModel.objects.get(id=food_id)
    comments = CommentModel.objects.filter(food_id=food_id)
    user_id = request.session.get('user_id')
    if user_id:
        flag_mask = MarkModel.objects.filter(item_id=food_id, user_id=user_id).first()
    else:
        flag_mask = False
    food.view_count += 1
    food.save()
    context = {
        'food': food,
        'comments': comments,
        'flag_mask': flag_mask
    }
    return render(request, 'food_detail.html', context=context)


def food_list(request, category_id):
    if request.method == 'GET':
        # 食物列表
        foods = FoodModel.objects.filter(
            category_id=category_id
        )
        context = {
            'foods': foods
        }
        return render(request, 'food_list.html', context=context)


def add_like(request):
    # 添加收藏
    food_id = int(request.POST.get('food_id'))
    user_id = request.session.get('user_id')
    flag = LikeModel.objects.filter(
        food_id=food_id,
        user_id=user_id
    ).first()
    if flag:
        return JsonResponse({'code': 400, 'message': 'The food has been collected'})
    LikeModel.objects.create(
        user_id=user_id,
        food_id=food_id
    )
    return JsonResponse({'code': 200})


def my_like(request):
    user_id = request.session.get('user_id')
    if request.method == 'GET':
        # 我的收藏界面
        likes = LikeModel.objects.filter(
            user_id=user_id
        )
        return render(request, 'my_like.html', {'likes': likes})
    else:
        # 删除收藏
        like_id = request.POST.get('like_id')
        LikeModel.objects.filter(
            id=like_id
        ).first().delete()
        return JsonResponse({'code': 200})


def my_order(request):
    user_id = request.session.get('user_id')
    if request.method == 'GET':
        # 我的订单
        orders = OrderModel.objects.filter(
            user_id=user_id
        )
        context = {
            'orders': orders
        }
        return render(request, 'my_order.html', context=context)
    else:
        # 删除订单
        order_id = request.POST.get('order_id')
        OrderModel.objects.filter(
            id=order_id
        ).first().delete()
        return JsonResponse({'code': 200})


def my_info(request):
    user_id = request.session.get('user_id')
    if request.method == 'GET':
        # 个人信息界面
        info = UserInfoModel.objects.filter(
            id=user_id
        ).first()
        context = {
            'info': info
        }
        return render(request, 'my_info.html', context=context)
    else:
        # 更新个人信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        if not (username or password or phone or address):
            return JsonResponse({'code': 400, 'message': 'The parameter cannot be null'})

        UserInfoModel.objects.filter(
            id=user_id
        ).update(
            username=username,
            password=password,
            phone=phone,
            address=address
        )
        return JsonResponse({'code': 200})


def add_comment(request):
    # 添加评论
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'code': 400, 'message': 'Please login first'})
    content = request.POST.get('content')
    food_id = request.POST.get('food_id')
    if not content:
        return JsonResponse({'code': 400, 'message': 'The content cannot be empty'})

    CommentModel.objects.create(
        user_id=user_id,
        content=content,
        food_id=food_id
    )
    return JsonResponse({'code': 200})


def view_count(request):
    # 浏览量排行
    if request.method == 'GET':
        return render(request, 'view_count.html')
    else:
        name_list = []
        count_list = []
        foods = FoodModel.objects.order_by('-view_count')[:10]
        for food in foods:
            name_list.append(food.name)
            count_list.append(food.view_count)

        return JsonResponse({'code': 200, 'name_list': name_list, 'count_list': count_list})


def calculate_cosine_similarity(user_ratings1, user_ratings2):
    # 将用户1的食物评分存入字典，键为食物ID，值为评分
    item_ratings1 = {rating.item_id: rating.score for rating in user_ratings1}
    # 将用户2的食物评分存入字典，键为食物ID，值为评分
    item_ratings2 = {rating.item_id: rating.score for rating in user_ratings2}

    # 找出两个用户共同评价过的食物
    common_items = set(item_ratings1.keys()) & set(item_ratings2.keys())

    if len(common_items) == 0:
        return 0.0  # 无共同评价的食物，相似度为0

    # 提取共同评价食物的评分，存入NumPy数组
    user1_scores = np.array([item_ratings1[item_id] for item_id in common_items])
    user2_scores = np.array([item_ratings2[item_id] for item_id in common_items])

    # 计算余弦相似度
    cosine_similarity = np.dot(user1_scores, user2_scores) / (
            np.linalg.norm(user1_scores) * np.linalg.norm(user2_scores))
    return cosine_similarity


def user_based_recommendation(request, user_id):
    try:
        # 获取目标用户对象
        target_user = UserInfoModel.objects.get(id=user_id)
    except UserInfoModel.DoesNotExist:
        return JsonResponse({'code': 400, 'message': 'This user does not exist'})

    # 获取目标用户的食物评分记录
    target_user_ratings = MarkModel.objects.filter(user=target_user)

    # 用于存储推荐食物的字典
    recommended_items = {}

    # 遍历除目标用户外的所有其他用户
    for other_user in UserInfoModel.objects.exclude(pk=user_id):
        # 获取其他用户的食物评分记录
        other_user_ratings = MarkModel.objects.filter(user=other_user)

        # 计算目标用户与其他用户的相似度
        similarity = calculate_cosine_similarity(target_user_ratings, other_user_ratings)

        if similarity > 0:
            # 遍历其他用户评价的食物
            for item_rating in other_user_ratings:
                # 仅考虑目标用户未评价过的食物
                if item_rating.item not in target_user_ratings.values_list('item', flat=True):
                    if item_rating.item.id in recommended_items:
                        # 累积相似度加权的评分和相似度
                        recommended_items[item_rating.item.id]['score'] += similarity * item_rating.score
                        recommended_items[item_rating.item.id]['similarity'] += similarity
                    else:
                        # 创建推荐食物的记录
                        recommended_items[item_rating.item.id] = {'score': similarity * item_rating.score,
                                                                  'similarity': similarity}

    # 将推荐食物按照加权评分排序
    sorted_recommended_items = sorted(recommended_items.items(), key=lambda x: x[1]['score'], reverse=True)

    # 获取排名靠前的推荐食物的ID
    top_recommended_items = [item_id for item_id, _ in sorted_recommended_items[:5]]

    # 构建响应数据
    response_data = []
    for item_id in top_recommended_items:
        item = FoodModel.objects.get(pk=item_id)
        similarity = recommended_items[item_id]['similarity']
        response_data.append({
            'name': item.name,
            'id': item.id,
            'image': item.image,
            'similarity': similarity,
        })
    context = {
        'response_data': response_data
    }
    return render(request, 'item_recommend.html', context=context)


def input_score(request):
    # 用户对食物进行评分
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'code': 400, 'message': 'Please login first'})
    score = int(request.POST.get('score'))
    food_id = request.POST.get('food_id')
    MarkModel.objects.create(
        item_id=food_id,
        score=score,
        user_id=user_id
    )
    return JsonResponse({'code': 200})


def check_page(request):
    return render(request, 'check_page.html')


def img_upload(request):
    # 图片上传
    file = request.FILES.get('file')
    old_name = file.name
    file_name = '{}.{}'.format(int(time.time()), str(old_name).rsplit('.')[-1])
    with open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    upload_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)
    return JsonResponse({'code': 200, 'image_url': upload_url})


def food_check(request):
    #  图像识别
    img_url = request.POST.get('image_url')
    img_name = str(img_url).rsplit('/')[-1]
    image_path = os.path.join(settings.MEDIA_ROOT, img_name)
    pred_name = check_handle(image_path)
    # pred_name = '测试'
    return JsonResponse({'code': 200, 'pred_name': pred_name})
