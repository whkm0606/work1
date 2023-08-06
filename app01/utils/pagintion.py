from django.utils.safestring import mark_safe
from django.http.request import QueryDict
import copy

from django.views.decorators.csrf import csrf_exempt

"""
        在视图函数中:
        def pretty_list(request):
        #1.根据自己的情况去筛选自己的数据
        queryset = models.PrettgNum.objects.allO
        #2.实例化分页对象
        page_object = Pagination(request,queryset)
        context = {
        "queryset" : page_object.page_queryset,#分完页的数据
        "page_string": page_object.html,#生成页码
        }
        return render(request, 'pretty_list.html', context)
        在HTML页面中
        {%for obj in queryset%}{obj.xx}
        {%endfor%}
        <ul class="pagination">
        {{page_string }}
        </ul>
"""
@csrf_exempt
class Pagination(object):
    """
    :param reguest:请求的对象
    :param queryset:符合条件的数据(根据这个数据给他进行分页处理)
    :param page_size:每页显示多少条数据
    :param page_param:在URL中传递的获取分页的参数，例如:/etty/list/ ?page=12
    :param plus:显示当前页的前或后几页(页码)
    """

    @csrf_exempt
    def __init__(self,request,queryset,puls = 4,page_size = 10,page_param="page"):

        #这样做是因为在搜索之后，进行下一页，request.get里面的值会被重置
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True#这样就可以对request.GET里面的数据进行更改
        self.query_dict = query_dict
        # 数据总条数
        self.total_count = queryset.count()
        # 每页几个数据
        self.page_size = page_size
        # 根据访问的页码，计算起止位置
        # 页码跳转
        total_page_count, div = divmod(self.total_count, self.page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        xx = request.GET.get(page_param, "1")
        if xx:
            if 0 < int(xx) and int(xx) <= self.total_page_count:
                page = int(xx)
            elif int(xx)>self.total_page_count:
                page = self.total_page_count
            else:
                page = 1
        else:
            page = 1
        self.page = page
        self.start = page_size * (self.page - 1)
        self.end = page * page_size
        self.puls = puls
        self.page_param = page_param
        self.page_queryset = queryset[self.start:self.end]
    @csrf_exempt
    def html(self):
        if self.total_page_count <= 2 * self.puls + 1:  # 数据量少
            start_page = 1
            end_page = self.total_page_count + 1
        else:  # 数据量多 页码多>2*puls
            if self.page <= self.puls:  # 当前页少于plus
                start_page = 1
                end_page = 2 * self.puls + 1
            else:
                if self.page > self.total_page_count - self.puls:  # 当前页离最后页少于puls
                    start_page = self.total_page_count - 2 * self.puls
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.puls
                    end_page = self.page + self.puls
        # 页码（把所有页码加到page_str_list）
        page_str_list = []
        # 首页
        self.query_dict.setlist(self.page_param,[1])
        page_str_list.append(
            '<li><a href="?{0}" aria-label="Previous"><span aria-hidden="true"><<首页</span></a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            pre_page = '<li><a href="?{0}" aria-label="Previous"><span aria-hidden="true"><</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            pre_page = '<li><a href="?{0}" aria-label="Previous"><span aria-hidden="true"><</span></a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(pre_page)
        # 存放所有页
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{0}">{1}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{0}">{1}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            aft_page = '<li><a href="?{0}" aria-label="Next"><span aria-hidden="true">></span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            aft_page = '<li><a href="?{0}" aria-label="Next"><span aria-hidden="true">></span></a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(aft_page)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append(
            '<li><a href="?{0}" aria-label="Previous"><span aria-hidden="true">尾页>></span></a></li>'.format(
                self.query_dict.urlencode()))
        #跳转页
        page_turn = '''<div class="col-lg-6" style="float: right; width: 200px">
        <form method="post">
            <div class="input-group">
              <input type="text" class="form-control" placeholder="页码" name="page">
              <span class="input-group-btn">
                <button class="btn btn-default" type="submit">跳转</button>
              </span>
        </div>
        </form>
        '''
        page_str_list.append(page_turn)
        page_string = mark_safe("".join(page_str_list))  # 将‘<li>’安全化，可在网址html化
        return page_string