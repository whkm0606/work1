import random
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from app01.utils.pagintion import Pagination
from app01 import models
from django.shortcuts import render,redirect
from django import forms
from django.http import JsonResponse
from app01.modelform.form import BModelForm
def chart_list(request):
    return  render(request,"char_list.html")
def chart_bar(request):
    #图一
    legend_data1 = ['销售部', 'IT部', '清洁部', '研发部', '开发部']
    xAxis_data1 = ['1月', '2月', '3月', '4月', '5月', '6月', '7月']
    series_data1 = [
                    {
                      "name": '销售部',
                      "type": 'line',
                      "stack": 'Total',
                      "data": [120, 132, 101, 134, 90, 230, 210]
                    },
                    {
                      "name": 'IT部',
                      "type": 'line',
                      "stack": 'Total',
                      "data": [220, 182, 191, 234, 290, 330, 310]
                    },
                    {
                      "name": '清洁部',
                      "type": 'line',
                      "stack": 'Total',
                      "data": [150, 232, 201, 154, 190, 330, 410]
                    },
                    {
                      "name": '研发部',
                      "type": 'line',
                      "stack": 'Total',
                      "data": [320, 332, 301, 334, 390, 330, 320]
                    },
                    {
                      "name": '开发部',
                      "type": 'line',
                      "stack": 'Total',
                      "data": [820, 932, 901, 934, 1290, 1330, 1320]
                    }
                  ]
    #图二
    data_list_y = [
        {
            "name": '员工1',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '员工2',
            "type": 'bar',
            "data": [45, 30, 36, 15, 18, 30]
        }
    ]
    legend = ['员工1', '员工2']
    data_list_x = ['1月', '2月', '3月', '4月', '5月', '6月']
    #图三
    series_data3 =[{ "value": 1048, "name": '销售部' },
                { "value": 735, "name": 'IT部' },
                { "value": 580, "name": '清洁部' },
                { "value": 484, "name": '研发部' },
                { "value": 300, "name": '开发部' }]
    result = {
        "status":True,
        "data":{
            #图一折线图：
            "legend_data1":legend_data1,
            "xAxis_data1":xAxis_data1,
            "series_data1":series_data1,
            #图二柱状图
            "xAxis_data2": data_list_x,
            "legend_data2": legend,
            "series_data2": data_list_y,
            # 图三饼状图
            "series_data3":series_data3,

        }

    }
    return JsonResponse(result)
