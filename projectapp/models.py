from django.db import models


# Create your models here.
#회원 정보 테이블
class Members(models.Model):
    userid = models.CharField(max_length=20, verbose_name="회원 아이디")
    password = models.CharField(max_length=20, verbose_name="비밀 번호")
    username = models.CharField(max_length=12, verbose_name="회원 이름")
    class_type = models.IntegerField(verbose_name="반 유형 - 1:빅데이터, 2:AI, 3:Cloud, 4:IoT")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="가입일")
    state = models.IntegerField(verbose_name="회원 상태 - 0:회원, 1:탈퇴")

    def __str__(self):
        return f"[{self.__class__.__name__}] 아이디 : {self.userid}, 비번 : {self.password}," \
               f"이름 : {self.username}, 상태 : {self.state}, 반 유형 : {self.class_type}"


# 식당 정보 테이블
class Resinfo(models.Model):
    res_name = models.CharField(max_length=30, verbose_name="식당 이름")
    res_type = models.CharField(max_length=4, verbose_name="식당 종류") # kor, chn, jpn, wes, etc
    res_addr = models.TextField(verbose_name="식당 주소")
    res_info = models.TextField(verbose_name="식당 소개", null=True)
    res_price = models.IntegerField(verbose_name="가격대") # 6000, 8000, 10000, 12000
    res_image = models.CharField(max_length=40, verbose_name="이미지 경로", null=True)
    locate_x = models.FloatField(verbose_name="식당 x좌표") # 37.00000
    locate_y = models.FloatField(verbose_name="식당 y좌표") # 127.00000
    tag_tout = models.IntegerField(verbose_name="1:TakeOut, 0:불가", null=True)
    tag_solo = models.IntegerField(verbose_name="1:1인석제공, 0:불가", null=True)
    tag_special = models.IntegerField(verbose_name="1:점심특선, 0:없음", null=True)
    tag_free = models.IntegerField(verbose_name="1:자율배식, 0:불가", null=True)
    star_avg = models.FloatField(verbose_name="리뷰 별점의 평균 = 총 별점", default=0, null=True)
    rev_cnt = models.IntegerField(verbose_name="총 리뷰수", default=0, null=True)

    def __str__(self):
        return f"[{self.__class__.__name__}] 이름 : {self.res_name}, 종류 : {self.res_type}, " \
               f"주소 : {self.res_addr}, 가격대 : {self.res_price}, x : {self.locate_x}, y : {self.locate_y}," \
               f"별점 : {self.star_avg}, 리뷰수 : {self.rev_cnt}, 이미지 경로 : {self.res_image}"


# 메뉴 리스트 테이블
class Menulist(models.Model):
    menu_name = models.CharField(max_length=30, verbose_name="메뉴 이름")
    menu_price = models.IntegerField(verbose_name="가격")
    res_id = models.ForeignKey(Resinfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.__class__.__name__}] 메뉴명 : {self.menu_name}, 가격 : {self.menu_price}, 가게id : {self.res_id}"


#게시판 테이블
class Bbs(models.Model):
    bbs_writer = models.CharField(max_length=20, verbose_name="작성자")
    bbs_title = models.TextField(verbose_name="글 제목")
    bbs_content = models.TextField(verbose_name="글 내용")
    bbs_date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    bbs_cnt = models.IntegerField(verbose_name="조회수")
    bbs_type = models.CharField(max_length=10, null=True, verbose_name="게시글종류")

    def __str__(self):
        return f"[{self.__class__.__name__}] 작성자 : {self.bbs_writer}, 제목 : {self.bbs_title}," \
               f"내용 : {self.bbs_content}"


#리뷰 테이블
class Review(models.Model):
    res_id = models.IntegerField(verbose_name="가게id")
    rev_writer = models.CharField(max_length=10, null=True, default="", verbose_name="작성자")
    rev_star = models.IntegerField(verbose_name="리뷰 별점")
    rev_content = models.TextField(verbose_name="리뷰 내용")
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    deleted = models.BooleanField(default=False, verbose_name='삭제여부')


    def __str__(self):
        return f"[{self.__class__.__name__}] 작성자id : {self.rev_writer}, 가게id : {self.res_id}," \
               f"리뷰 별점 : {self.rev_star}, 리뷰 내용 : {self.rev_content}, 삭제여부 : {self.deleted}"


# class test_table(models.Model):
#     tres_name = models.CharField(max_length=30, verbose_name="식당 이름")
#     tres_type = models.IntegerField(verbose_name="식당 종류")
#     tres_addr = models.TextField(verbose_name="식당 주소")
#     tres_short_info = models.TextField(verbose_name="간단 소개")
#     tres_long_info = models.TextField(verbose_name="상세 소개")
#     tres_price = models.IntegerField(verbose_name="가격대")
#     tres_image = models.CharField(max_length=40, verbose_name="이미지 경로")
#     tlocate_x = models.FloatField(verbose_name="식당 x좌표")
#     tlocate_y = models.FloatField(verbose_name="식당 y좌표")
#     ttag_tout = models.IntegerField(verbose_name="1:T/O가능, 0:불가")
#     ttag_solo = models.IntegerField(verbose_name="1:혼밥가능, 0:불가")
#     ttag_special = models.IntegerField(verbose_name="1:점심특선있음, 0:없음")
#     ttag_free = models.IntegerField(verbose_name="1:자율배식가능, 0:불가")
#     tstar_avg = models.FloatField(verbose_name="리뷰 별점의 평균 = 총 별점")
#     trev_cnt = models.IntegerField(verbose_name="총 리뷰수")
#
#     def __str__(self):
#         return f"[{self.__class__.__name__}] 이름 : {self.tres_name}, 종류 : {self.tres_type}, " \
#                f"주소 : {self.tres_addr}, 가격대 : {self.tres_price}, x : {self.tlocate_x}, y : {self.tlocate_y}," \
#                f"별점 : {self.tstar_avg}, 리뷰수 : {self.trev_cnt}, 이미지 경로 : {self.tres_image}"
