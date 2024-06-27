from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *

# Create your views here.

def firstpage(request):
    user = request.user
    if user.is_authenticated:
        try:
            total_points_obj = TotalPoints.objects.get(user=user)
            points = total_points_obj.total_points
        except TotalPoints.DoesNotExist:
            points = 0  # 如果用户没有记录，设置 points 为 0
        # 如果点数为 0，重定向到储值页面
        if points == 0:
            return redirect('savepoint')  # 这里的 'savepoint' 是储值页面的 URL 名称
    return render(request,'firstpage.html',locals())

def linelogin(request):
    return render(request,'linelogin.html',locals())

def home(request):
    return render(request, 'home.html')

#---------------------------------------------------------------------#
# 儲值區
def savepoint(request):
    return render(request, 'savepoint.html')

def savepointapi(request):
    if request.method == 'POST':
        savepoints = request.POST.get('savepoints')  # 獲取表單提交的點數
        if savepoints:
            try:
                savepoints = int(savepoints)  # 將輸入的點數轉為整數
                if savepoints > 0:
                    # 獲取當前登入用戶，假設使用了 Django 自帶的用戶模型
                    user = request.user
                    
                    # 創建 savepoints 對象並保存到資料庫
                    MovingPoints.objects.create(user=user, points=savepoints)
                    
                    # 可以根據需要發送訊息或重定向到其他頁面
                    messages.success(request, f'成功儲值 {savepoints} 點。')
                    return redirect('success_savepage')  # 重新導向到成功頁面或其他頁面
                else:
                    messages.error(request, '儲值點數必須大於0。')
            except ValueError:
                messages.error(request, '請輸入有效的數字。')
        else:
            messages.error(request, '請輸入儲值點數。')

    # 如果請求不是 POST 或出現錯誤，則傳回原始的儲值點數頁面
    return render(request, 'savepoint.html')

def success_savepage(request):
    return render(request, 'success_savepage.html')

#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
#消費區


def spendpoint(request):
    return render(request, 'spendpoint.html')

def spendpointapi(request):
    if request.method == 'POST':
        spendpoints = request.POST.get('spendpoints')  # 獲取表單提交的點數
        if spendpoints:
            try:
                spendpoints = int(spendpoints)  # 將輸入的點數轉為整數
                if spendpoints > 0:
                    # 獲取當前登入用戶，假設使用了 Django 自帶的用戶模型
                    user = request.user

                    # 從 TotalPoints 中獲取當前點數
                    total_points_obj = TotalPoints.objects.get(user=user)
                    userpoints = total_points_obj.total_points

                    if userpoints >= spendpoints:
                        # 創建消費點數的負數記錄並保存到 MovingPoints
                        MovingPoints.objects.create(user=user, points=-spendpoints)

                        # 更新 TotalPoints 中的點數
                        TotalPoints.update_total_points(user)
                        
                    
                        # 可以根據需要發送訊息或重定向到其他頁面
                        messages.success(request, f'成功消費 {spendpoints} 點。')
                        return redirect('success_spendpage')  # 重新導向到成功頁面或其他頁面
                    else:
                        messages.error(request, '您的點數不足以進行本次消費')
                else:
                    messages.error(request, '消費點數必須大於0。')
            except ValueError:
                messages.error(request, '請輸入有效的數字。')
        else:
            messages.error(request, '請輸入消費點數。')
            

    # 如果請求不是 POST 或出現錯誤，則傳回原始的儲值點數頁面
    return render(request, 'spendpoint.html')

def success_spendpage(request):
    return render(request, 'success_spendpage.html')

#---------------------------------------------------------------------#