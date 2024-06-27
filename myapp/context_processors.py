# 上下文處理器
# context_processors.py

from .models import TotalPoints, MovingPoints

def auth_status(request):
    user = request.user
    points = 0  # 默认为0点，以防用户未登录或没有点数记录
    newsavepoints = 0 # 默认为0点，以防用户未登录或没有点数记录

    if user.is_authenticated:
        try:
            # 尝试从数据库中获取用户的点数信息
            points_obj = TotalPoints.objects.get(user=user)
            points = points_obj.total_points
        except TotalPoints.DoesNotExist:
            pass  # 如果用户没有点数记录，则保持默认值
        try:
            savepoints = MovingPoints.objects.filter(user=user).order_by('-timestamp').first()
            if savepoints is not None:
                newsavepoints = savepoints.points
                if newsavepoints < 0:
                    newsavepoints = -newsavepoints
        except MovingPoints.DoesNotExist:
            newsavepoints = 0
    # 返回包含用户和点数信息的字典
    return {'user': user, 'points': points, 'newsavepoints':newsavepoints}

