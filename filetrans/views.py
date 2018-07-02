#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload_accept(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        task = request.POST.get('task_id')  # 获取文件唯一标识符
        chunk = request.POST.get('chunk', 0)  # 获取该分片在所有分片中的序号
        filename = '%s%s' % (task, chunk)  # 构成该分片唯一标识符
        file_full_name = 'media/filetrans/upload/%s' % filename
        try:
            os.makedirs(os.path.dirname(file_full_name))
        except OSError:
            pass
        with open(file_full_name, 'wb') as f:
            for chunk in upload_file.chunks():
                f.write(chunk)  # 保存分片到本地
    context = {}
    return render(request, 'filetrans/index.html', context=context)


# @csrf_exempt
def upload_complete(request):  # 所有分片均上传完后被调用
    target_filename = request.GET.get('filename')  # 获取上传文件的文件名
    task = request.GET.get('task_id')  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open('media/filetrans/upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = 'media/filetrans/upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    context = {}
    return render(request, 'filetrans/index.html', context=context)
