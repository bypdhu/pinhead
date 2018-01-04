# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import Bucket, DownloadUrlHistory
from .lib.ess_tools import get_bucket_from_url, get_file_from_ess, get_filekey_from_url


def index(request):
    return render(request, 'ess/index.html', {})


def download(request):
    return render(request, 'ess/download.html', {})


def get_download_url_history(request):
    # body = json.loads(request.body)
    download_urls = DownloadUrlHistory.objects.all()
    urls = []
    for d in download_urls:
        one = dict(id=d.id, url=d.url, create_time=str(d.create_time), update_time=str(d.update_time), times=d.times,
                   check_md5=d.check_md5, md5=d.md5, modified=d.modified)
        urls.append(one)
    print(urls)
    urls_del_multi = {}
    for u in urls:
        print(urls_del_multi)
        url = u.get('url')
        if url in urls_del_multi.keys():
            if urls_del_multi.get(url).get("times") < u.get('times'):
                urls_del_multi[url] = u
        else:
            urls_del_multi.update({url: u})
    print(urls_del_multi)

    return HttpResponse(json.dumps({'histories': urls_del_multi.values()}), content_type="application/json")


def get_one_download_url_history(request, url):
    body = json.loads(request.body)
    header = request.header
    print(body)
    print(header)
    download_urls = DownloadUrlHistory.objects.filter(url=url)
    return HttpResponse(json.dumps({'histories': download_urls}), content_type="application/json")


@csrf_exempt
def get_file_content_from_url(request):
    print("-=-==============================================")
    print(request.body)
    body = json.loads(request.body)
    url = body.get('url').strip()

    bucket_name = get_bucket_from_url(url)
    file_key = get_filekey_from_url(url)

    bucket_store = Bucket.objects.get(name=bucket_name)
    print("bucket stored: " + bucket_store.name)

    bucket = {
        'name': bucket_store.name,
        'key': bucket_store.access_key,
        'pass': bucket_store.access_secret,
    }

    file_pn = os.path.join(settings.MEDIA_ROOT, 'ess', 'download', file_key)
    if not os.path.exists(os.path.dirname(file_pn)):
        os.makedirs(os.path.dirname(file_pn))
    rr = get_file_from_ess(url, saveas=file_pn, **bucket)

    with open(file_pn, 'rb') as content:
        file_content = content.read()
    # print(file_content)
    resp = {'status': 0, 'content': file_content, 'request_origin': request.body}
    response = HttpResponse(json.dumps(resp), content_type='application/json')

    # when success, record this url. TODO. record success/fail
    history = {
        'url': url,
    }
    old_histories = _filter_from_database(DownloadUrlHistory, **history)
    if old_histories:
        print(old_histories)
        times = max([h.times for h in old_histories]) + 1
    else:
        times = 1
    history.update({'times': times})
    _record_to_database(DownloadUrlHistory, **history)

    return response


def _record_to_database(db, **kwargs):
    if _filter_from_database(db, **kwargs):
        pass
    else:
        DownloadUrlHistory.objects.create(**kwargs)


def _filter_from_database(db, **kwargs):
    return db.objects.filter(**kwargs)


def upload(request):
    return render(request, 'ess/upload.html', {})


def list_bucket(request):
    buckets = Bucket.objects.all()
    return render(request, 'ess/list_bucket.html', {'buckets': buckets})


@csrf_exempt
def create_bucket(request):
    body = json.loads(request.body)
    bucket_name = body.get('name')
    try:
        Bucket.objects.get(name=bucket_name)
        return HttpResponse(json.dumps({'status': 1, 'msg': 'bucket already created!!'}),
                            content_type='application/json')
    except ObjectDoesNotExist:
        pass

    bucket = {
        'name': bucket_name,
        'access_key': body.get('key'),
        'access_secret': body.get('pass')
    }
    try:
        Bucket.objects.create(**bucket)
    except:
        return HttpResponse(json.dumps({'status': 2, 'msg': 'fail to create bucket!!'}),
                            content_type='application/json')

    response = HttpResponse(json.dumps({'status': 0, 'msg': 'success', 'request_origin': request.body}),
                            content_type='application/json')
    return response


