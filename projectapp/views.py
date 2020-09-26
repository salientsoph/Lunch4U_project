from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import Resinfo, Menulist, Review, Members, Bbs
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from django.core.serializers.json import DjangoJSONEncoder

import json


# Create your views here.

def index(request):
    if 'user' in request.session :
        context = {'userid' : request.session.get('user')}
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")

def search(request):
    page = request.GET.get ('page', 1) # 템플릿에서 받은 페이지가 있으면 그 페이지를 page변수에 넣음
    # 그렇지 않으면 1을 할당

    # 1. 검색을 위해 템플릿에서 selected된 값들을 가져옴
    selected_restype = request.GET.get('res_type', '')
    selected_pricetype = request.GET.get('price_type', '')
    tag_tout = request.GET.get('tout', '')
    tag_solo = request.GET.get('solo', '')
    tag_free = request.GET.get('free', '')
    tag_spec = request.GET.get('spec', '')
    sort = request.GET.get('sort', '')

    # 2. 해당 값들로 퀴리문 검색 후 객체에 넣음
    # 2-1. 식당 타입으로 검색
    if selected_restype : #
        if selected_restype == 'all': # 선택된 값이 '전체'일때
            reslist = Resinfo.objects.all()
        else: # 식당 종류 값에 해당되는 db 가져옴
            reslist = Resinfo.objects.filter(res_type = selected_restype)

    # 2-2. 가격대로 검색
    if selected_pricetype :
        if selected_pricetype == 'allcost': # 선택된 값이 '전체'일때
            reslist = reslist
        elif selected_pricetype == '6000': # 선택된 값이 '6000'일때
            reslist = reslist.filter(res_price__range = (0, 6000)) # 0 ~ 6천 사이의 db값 가져옴
        else: # 그외에는 6~8, 8~10, 10~12 사이의 db값을 가져옴
            reslist = reslist.filter(res_price__range = (int(selected_pricetype)-2000, int(selected_pricetype)))

    # 2-3. 태그별 검색
    if tag_solo :
        if tag_solo == "1":
            reslist = reslist.filter(tag_solo = "1")
    if tag_tout :
        if tag_tout == "1":
            reslist = reslist.filter(tag_tout = "1")
    if tag_free :
        if tag_free == "1":
            reslist = reslist.filter(tag_free = "1")
    if tag_spec :
        if tag_spec == "1":
            reslist = reslist.filter(tag_special = "1")

    # 3. sort 값 가져옴(모든 검색 필터를 다 거친 후 마지막에 정렬해줌)

    if sort == 'by_s': # 별점순 정렬
        reslist = reslist.order_by('-star_avg') # 내림차순정렬
    elif sort == 'by_r': # 리뷰수 정렬
        reslist = reslist.order_by('-rev_cnt') # 내림차순정렬

    # 페이징
    paginator = Paginator(reslist, 4) # 페이지당 4개씩 보여주도록 설정
    rlistpage = paginator.get_page(page) # page변수에 해당하는 글들을 rlistpage에 담음

    page_numbers_range = 5 # 페이지 범위를 1~5 6~10 처럼 하기위해 5로 설정

    max_index = paginator.num_pages
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    paginator_range = paginator.page_range[start_index:end_index]
    # 페이징 끝

    # 템플릿의 select option 값 유지를 위해 템플릿으로 보낼 객체
    selected_values = {"sort" : sort, "type":selected_restype, "price":selected_pricetype, "tout" : tag_tout, "solo" : tag_solo, "free" : tag_free, "special" : tag_spec}


    context = {
        "reslist" : rlistpage,
        "paginator_range" : paginator_range,
        "selected_values" : selected_values,
    }

    if 'user' in request.session :
        userid = request.session.get('user')
        context['userid'] = userid

    return render(request, 'search.html', context)

def list(request):
    page = request.GET.get ('page', 1) # 템플릿에서 받은 페이지가 있으면 그 페이지를 page변수에 넣음
    # 그렇지 않으면 1을 할당
    reslist = Resinfo.objects.all()
    paginator = Paginator(reslist, 4) # 페이지당 4개씩 보여주도록 설정
    rlistpage = paginator.get_page(page) # page변수에 해당하는 글들을 rlistpage에 담음

    page_numbers_range = 5 # 페이지 범위를 1~5 6~10 처럼 하기위해 5로 설정

    max_index = paginator.num_pages
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    paginator_range = paginator.page_range[start_index:end_index]

    context = {
        "reslist" : rlistpage,
        "paginator_range" : paginator_range,
    }
    if 'user' in request.session :
        userid = request.session.get('user')
        context['userid'] = userid

    return render(request, 'list.html', context)

def resinfo(request):
    pk = request.GET.get("pk")
    info = Resinfo.objects.get(pk=pk)
    menulist = Menulist.objects.filter(res_id=pk)
    reviewlist = Review.objects.filter(res_id=pk).order_by('created')

    context = {
        "r_info" : info,
        "menulist" : menulist,
        "reviewlist" : reviewlist,
    }

    if 'user' in request.session :
        userid = request.session.get('user')
        context['userid'] = userid

    return render(request, 'resinfo.html', context)

def review_write(request):
    if request.method == 'POST':
        res_id = request.POST.get('res_id')
        writer = request.POST.get('r_writer')
        content = request.POST.get('r_content')
        star = request.POST.get('rev_star')
        print("식당번호:",res_id,"작성자", writer,"내용",content, "별점 ",star)

        if not content :
            error = "댓글을 입력하세요."
        else:
            review = Review(res_id=int(res_id), rev_writer=writer, rev_content=content, rev_star=star)
            review.save()
            resinfo = Resinfo.objects.get(pk=res_id)
            if resinfo.star_avg == 0:
                resinfo.star_avg = float(star)
            else:
                resinfo.star_avg = float((resinfo.star_avg+float(star))/2)

            resinfo.rev_cnt += 1
            resinfo.save()
            redirect_url = "../../resinfo/?pk=" + res_id
            return redirect(redirect_url)
    return render(request, "resinfo.html", {'error' : error})

def review_delete(request):
    pk = request.GET.get('pk')
    res_id = request.GET.get('res_id')
    review = Review.objects.get(pk=pk)
    review.deleted = True
    review.save()
    redirect_url = "../../resinfo/?pk=" + res_id
    return redirect(redirect_url)

def register(request):
    if request.method =='GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        userid = request.POST.get('userid', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password',None)
        class_type = request.POST.get('class_type', None)
        res_data = {}
        if not (username and password and re_password and userid and class_type):
            res_data['error']='아이디 또는 패스워드를 입력해주세요.'
            return render(request, 'register.html', res_data)
        elif password != re_password:
            res_data['error']='비밀번호가 다릅니다.'
            return render(request, 'register.html', res_data)
        else:
            users = Members(
                userid=userid,
                username=username,
                password=make_password(password),
                class_type=class_type,
                state=0,
            )
            users.save()
        return render(request, 'login.html')


def login(request):
    context = None
    if request.method == "POST":
        userid = request.POST.get('userid', None)
        password = request.POST.get('password', None)
        try :
            user = Members.objects.get(userid=userid)
        except Members.DoesNotExist :
            context = {'error': '계정을 확인하세요'}
        else :
            print(password, user.password)
            if check_password(password, user.password):
                request.session['user'] = user.userid
                return redirect('index')
            else :
                context = { 'error' : '패스워드를 확인하세요'}
    return render(request, 'login.html', context)

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('index')

def map(request) :
    reslist = Resinfo.objects.all()

    context = {
        'reslist' : reslist,
    }
    if 'user' in request.session :
        userid = request.session.get('user')
        context['userid'] = userid

    return render(request, "map.html", context)

def mapsearch(request) :
    selected_restype = request.GET.get('res_type', '')
    findword = request.GET.get('findword', '')
    if findword:
        reslist = Resinfo.objects.filter(res_name__contains=findword)
    else:
        reslist = Resinfo.objects.all()

    if selected_restype : #
        if selected_restype == 'all': # 선택된 값이 '전체'일때
            reslist = reslist
        else: # 식당 종류 값에 해당되는 db 가져옴
            reslist = reslist.filter(res_type = selected_restype)

    selected_values = {"findword": findword, "type": selected_restype}

    context = {
        'reslist' : reslist,
        'selected_values' : selected_values,
    }

    if 'user' in request.session :
        userid = request.session.get('user')
        context['userid'] = userid

    return render(request, "mapsearch.html", context)

def bbslistview(request):
    page = request.GET.get('page', 1)  # 템플릿에서 받은 페이지가 있으면 그 페이지를 page변수에 넣음
    # 그렇지 않으면 1을 할당
    bbslist = Bbs.objects.all().order_by('-bbs_date')
    paginator = Paginator(bbslist, 10)  # 페이지당 4개씩 보여주도록 설정
    rlistpage = paginator.get_page(page)  # page변수에 해당하는 글들을 rlistpage에 담음

    page_numbers_range = 5  # 페이지 범위를 1~5 6~10 처럼 하기위해 5로 설정

    max_index = paginator.num_pages
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    paginator_range = paginator.page_range[start_index:end_index]

    context = {
        "bbslist": rlistpage,
        "paginator_range": paginator_range,
    }
    if 'user' in request.session:
        userid = request.session.get('user')
        context['userid'] = userid

    return render(request, 'bbs.html', context)

def bbswrite(request):
    if request.method == 'POST':
        bbs_writer = request.POST.get('writer')
        bbs_title = request.POST.get('title')
        bbs_content = request.POST.get('content')
        bbs_cnt = 0
        bbs_type = request.POST.get('bbstype')
        if bbs_title == "":
            bbs_title = "제목을 입력해주세요"
        if bbs_content == "":
            bbs_content = "작성한 내용이 없습니다."
        bbsdata = Bbs(bbs_writer=bbs_writer, bbs_title=bbs_title, bbs_content=bbs_content,
                      bbs_cnt=bbs_cnt, bbs_type=bbs_type)
        bbsdata.save()

        return redirect("bbs")
    else:
        if 'user' in request.session:
            userid = request.session.get('user')
            context = {
                'userid' : userid
            }
        return render(request, "bbswrite.html", context)

def bbsdetail(request):
    pk = request.GET.get("pk")
    bbsinfo = Bbs.objects.get(pk=pk)
    bbsinfo.bbs_cnt += 1
    bbsinfo.save()

    context = {
        "bbsinfo": bbsinfo,
    }

    if 'user' in request.session:
        userid = request.session.get('user')
        context['userid'] = userid

    return render(request, 'bbsdetail.html', context)

def bbsupdate(request):
    if request.method == 'POST':
        pk = request.GET.get("pk")
        bbsinfo = Bbs.objects.get(pk=pk)
        title = request.POST.get('title')
        content = request.POST.get('content')
        bbsinfo.bbs_type = request.POST.get('bbstype')

        if title == "":
            bbsinfo.bbs_title = "제목을 입력해주세요"
        else:
            bbsinfo.bbs_title = title

        if content == "":
            bbsinfo.bbs_content = "작성한 내용이 없습니다."
        else:
            bbsinfo.bbs_content = content

        bbsinfo.save()
        redirect_url = "../bbsdetail/?pk=" + pk
        return redirect(redirect_url)

    else:
        pk = request.GET.get("pk")
        bbsinfo = Bbs.objects.get(pk=pk)

        context = {
            'bbsinfo' : bbsinfo
        }
        return render(request, "bbsupdate.html", context)

def bbsdelete(request):
    pk = request.GET.get('pk')
    bbsinfo = Bbs.objects.get(pk=pk)
    bbsinfo.delete()
    return redirect("bbs")