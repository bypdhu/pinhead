#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
This is user library.

@editor: bianbian,
@email : bianyunpeng@ehousechina.com,
"""
import ast
import base64
import hashlib
import hmac
import os
import random
import time

import logging
import requests
import yaml
# import magic
import mimetypes

VERSION = '1.0.0'


def init_logger(path):
    log_formatter = "%(asctime)s | %(levelname)s - %(message)s"
    date_formatter = "%Y-%m-%d %H:%M:%S"
    if isinstance(path, str) and os.path.exists(os.path.dirname(path)):
        log = logging.getLogger('esstools-%s' % VERSION)
        logHandler = logging.handlers.TimedRotatingFileHandler(path, when='midnight')
        logFormatter = logging.Formatter(fmt=log_formatter, datefmt=date_formatter)
        logHandler.setFormatter(logFormatter)
        log.addHandler(logHandler)
        log.setLevel(logging.DEBUG)
        log.propagate = False  # disable console output
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format=log_formatter, datefmt=date_formatter)
        log = logging.getLogger('esstools-%s' % VERSION)
    return log


LOGGER_PATH = "/data/logs/esstools/logs"
LOGGER = init_logger(LOGGER_PATH)


class Tools(object):
    def __init__(self):
        pass

    def write_to_file(self, filenp, content):
        """
        :param filenp: file path and name to write content to.
        :param content: binary content.. wirte as binary file
        :return:
        """
        if filenp:
            path = os.path.dirname(filenp)
            if path and not os.path.exists(path):
                os.mkdir(path)
            if not os.path.exists(filenp):
                print("file '{0}' not exist... create and save it....".format(filenp))
            with open(filenp, "wb") as f:
                f.write(content)

    def get_date(self, fmt=''):
        """
        :param fmt:
        :return:
        """
        fmt0 = "%a, %d %b %Y %H:%M:%S GMT" if fmt == '' else fmt
        return time.strftime(fmt0, time.gmtime())

    def get_file_md5(self, filenp):
        """
        :param filenp: file's name and path
        :return:
        """
        with open(filenp, 'rb') as f:
            hash = hashlib.md5()
            hash.update(f.read())
            md5 = base64.b64encode(hash.digest())
            print("{0} 's md5: {1}".format(filenp, md5))
        return md5

    def get_md5(self, content):
        """
        :param content: file's content, like "open(filename, 'rb') as content"
        :return:
        """
        hash = hashlib.md5()
        hash.update(content)
        md5 = base64.b64encode(hash.digest())
        print("md5: {0}".format(md5))
        return md5

    def get_signature(self, **kwargs):
        """
        :param kwargs: AccessKeySecret,Method, Content-MD5,Content-Type,Date, CanonicalizedHeaders, CanonicalizedResource
        canonicalized_resource= "/"  + ((bucketName != null) ? bucketName + "/" : "")  + ((key != null ? key : ""));
        :return:
        """
        access_key_secret = kwargs.get("AccessKeySecret", "")
        method = str(kwargs.get("Method")).upper()
        content_md5 = str(kwargs.get("Content-MD5", ""))
        content_type = str(kwargs.get("Content-Type", ""))
        date = str(kwargs.get("Date"))
        canonicalized_headers = str(kwargs.get("CanonicalizedHeaders", ""))
        bucket_name = str(kwargs.get("BucketName", ""))
        file_key = str(kwargs.get("FileKey", ""))
        canonicalized_resource = "/" + (bucket_name + "/" if bucket_name else "") + file_key

        pre_sign = method + "\n" \
                   + content_md5 + "\n" \
                   + content_type + "\n" \
                   + date + "\n" \
                   + canonicalized_headers \
                   + canonicalized_resource
        # print(type(pre_sign))
        print("pre signature is: {0}".format(pre_sign))
        signature = base64.b64encode(
            hmac.new(access_key_secret.encode('utf8'), pre_sign.encode('utf8'), digestmod=hashlib.sha1).digest())
        print("signature is: {0}".format(signature))
        return signature

    def get_authorization(self, **kwargs):
        """
        :param kwargs: AccessKeyId，
        AccessKeySecret,Method, Content-MD5,Content-Type,Date, CanonicalizedHeaders, BucketName, FileKey
        or
        :param kwargs: AccessKeyId, Signature
        :return:
        """
        access_key_id = kwargs.get("AccessKeyId", "")

        signature = kwargs.get("Signature", self.get_signature(**kwargs))

        authorization = "ESS {0}:{1}".format(access_key_id, signature)
        # print("authorization is: {0}".format(authorization))
        return authorization

    def get_variables_from_yaml(self, filePath):
        print(filePath)
        C = yaml.load(file(filePath, "r"))
        return C

    def get_host_from_url(self, url):
        print("get host from url {0}".format(url))
        return str(url).split('/')[2].split(':')[0]

    def get_bucket_name_from_url(self, url):
        print("get host from url {0}".format(url))
        return str(url).split('/')[2].split('.')[0]

    def get_random_string(self, num):
        ss = "abcdefghijklmnopqrstuvwxyz1234567890_!#^*"
        return "".join(random.sample(ss, int(num)))

    def guess_type_from_file(self, filepath):
        # mime = magic.Magic(mime=True)
        # return mime.from_file(filepath)
        mime = mimetypes.MimeTypes()
        guess = mime.guess_type(filepath)
        if isinstance(guess, tuple):
            return guess[0] if guess[0] else ""
        return ""

    def get_dict_from_string(self, s):
        if s:
            if isinstance(s, bytes):
                s = ast.literal_eval(s)
            elif isinstance(s, str):
                s = eval(s)
            return s
        else:
            return {}

    def print_http_response(self, url, r):
        print("response: {0}, url: {1}, headers: {2}".format(r, url, str(r.headers)))
        if str(r.status_code) != '200':
            print("content: {0}".format(r.content))
            print("text: {0}".format(r.text))

    def handle_http_kwargs(self, kwargs):
        if kwargs.get("headers", ""):
            if isinstance(kwargs.get("headers"), bytes):
                kwargs["headers"] = ast.literal_eval(kwargs.get("headers"))
            elif isinstance(kwargs.get("headers"), str):
                kwargs["headers"] = eval(kwargs.get("headers"))

    def handle_headers_string_to_dic(self, headers):
        headers_dict = {}
        for header in str(headers).split(","):
            hl = header.split(":")
            key, value = hl[0], hl[1] if len(hl) > 1 else ""
            headers_dict[key] = value
        return headers_dict


class BaseHttp(Tools):
    def __init__(self):
        super(BaseHttp, self).__init__()

    def base_get(self, url, **kwargs):
        self.handle_http_kwargs(kwargs)
        r = requests.get(url, **kwargs)
        r.close()
        self.print_http_response(url, r)
        return r

    def base_put(self, url, data=None, **kwargs):
        # handle kwargs, change to need type... like change kwargs["headers"] from unicode to dict
        self.handle_http_kwargs(kwargs)
        # print(kwargs)
        r = requests.put(url, data, **kwargs)
        r.close()
        self.print_http_response(url, r)
        return r

    def base_head(self, url, **kwargs):
        self.handle_http_kwargs(kwargs)
        r = requests.head(url, **kwargs)
        self.print_http_response(url, r)
        return r

    def base_post(self, url, data=None, json=None, tmpHeader=None, **kwargs):
        # print("data is: {0}".format(data))
        self.handle_http_kwargs(kwargs)
        # print("tmpHeader: {0}".format(tmpHeader))
        if tmpHeader:
            if kwargs.has_key('headers'):
                if isinstance(kwargs['headers'], dict):
                    for key, value in tmpHeader.items():
                        kwargs['headers'][key] = value
                elif not kwargs.get('headers'):
                    kwargs['headers'] = tmpHeader
            else:
                kwargs['headers'] = tmpHeader

        print("kwargs for post: {0}".format(kwargs))

        r = requests.post(url, data, json, **kwargs)
        self.print_http_response(url, r)
        return r

    def base_delete(self, url, **kwargs):
        self.handle_http_kwargs(kwargs)
        r = requests.delete(url, **kwargs)
        self.print_http_response(url, r)
        return r


class TestImpl(Tools):
    def __init__(self):
        super(TestImpl, self).__init__()

    def test_status_code(self, statusCode, expect):
        # judge status code first.
        if statusCode == expect:
            print("expect status code is the same with reponse: {0}".format(statusCode))
        else:
            print("expect status code: {0}, but the response is: {1}".format(expect, statusCode))
            raise Exception("status code not the same.")

    def test_file(self, getFilePath, expectFilePath):
        assert (self.get_file_md5(getFilePath) == self.get_file_md5(expectFilePath))
        # TODO: other file compare test.

    def test_headers(self, expectHeaders, headers):
        expectHeaders = dict(expectHeaders)
        headers = dict(headers)
        print("Expect Headers should have: {0}".format(str(expectHeaders)))
        print("Gotten Headers is: {0}".format(str(headers)))
        for header in expectHeaders.keys():
            print("expect header: {0}".format(header))
            assert (headers.has_key(header))
            value = expectHeaders.get(header)
            if value:
                print("expect header '{0}' value: {1}".format(header, value))
                assert (value == headers.get(header))


class EssWrapper(BaseHttp, TestImpl):
    def __init__(self):
        super(EssWrapper, self).__init__()
        # self.expectStatusCode = "expectStatusCode"
        # self.saveAs = "fileSaveAs"
        # self.expectFilePath = "expectFilePath"
        # self.expectHeaders = "expectHeaders"
        # self.dataFile = "dataFile"

    def get_test(self, url, saveAs=None, expectFilePath=None, expectStatusCode=None, expectHeaders=None, **kwargs):
        """
        :param expectHeaders: judge headers. write it like headers=content-Type:image/png,content-md5,server. NO SPACE!!!
        :param expectStatusCode: judge the status of response. like 200/401/
        :param expectFilePath: the file path to compare with the save file.
        :param saveAs: content save path. if expectStatus==200
        :param url:
        :param params:
        :param kwargs:
        expectStatusContent: like Ok/Not Found. TODO

        :return:
        """
        r = self.base_get(url, **kwargs)
        status_code = str(r.status_code)

        # judge status code first.
        if expectStatusCode:
            self.test_status_code(status_code, str(expectStatusCode))
        # judge file
        if status_code == '200':
            # save file.
            self.write_to_file(saveAs, r.content)

            # compare file.
            if expectFilePath:
                self.test_file(saveAs, expectFilePath)
        # judge headers
        if expectHeaders:
            self.test_headers(self.handle_headers_string_to_dic(expectHeaders), r.headers)

        rr = {'headers': self.get_dict_from_string(r.headers)}
        # rr = {'headers': self.get_dict_from_string(r.headers), 'text': r.text}
        return rr

    def head_test(self, url, expectStatusCode=None, expectHeaders=None, **kwargs):
        """
        :param expectHeaders: judge headers. write it like headers=content-Type:image/png,content-md5,server. NO SPACE!!!
        :param expectStatusCode: judge the status of response. like 200/401/
        :param url:
        :param kwargs:

        :return:
        """
        r = self.base_head(url, **kwargs)
        status_code = str(r.status_code)

        # judge status code first.
        if expectStatusCode:
            self.test_status_code(status_code, str(expectStatusCode))
        # judge headers
        if expectHeaders:
            self.test_headers(self.handle_headers_string_to_dic(expectHeaders), r.headers)

        rr = {'headers': self.get_dict_from_string(r.headers), 'text': self.get_dict_from_string(r.text)}
        return rr

    def delete_test(self, url, expectStatusCode=None, expectHeaders=None, **kwargs):
        """
        :param expectHeaders: judge headers. write it like headers=content-Type:image/png,content-md5,server. NO SPACE!!!
        :param expectStatusCode: judge the status of response. like 200/401/
        :param url:
        :param kwargs:

        :return:
        """
        r = self.base_delete(url, **kwargs)
        status_code = str(r.status_code)

        # judge status code first.
        if expectStatusCode:
            self.test_status_code(status_code, str(expectStatusCode))
        # judge headers
        if expectHeaders:
            self.test_headers(self.handle_headers_string_to_dic(expectHeaders), r.headers)

        rr = {'headers': self.get_dict_from_string(r.headers), 'text': r.text}
        # rr = {'headers': self.get_dict_from_string(r.headers), 'text': self.get_dict_from_string(r.text)}
        return rr

    def put_test(self, url, data=None, dataFile=None, expectStatusCode=None, expectHeaders=None, **kwargs):
        """
        :param expectHeaders:judge headers. write it like headers=content-Type:image/png,content-md5,server. NO SPACE!!!
        :param expectStatusCode:judge the status of response. like 200/401/
        :param dataFile: when data not in use, you can use data file path.
        :param url:
        :param data:
        :param kwargs:

        :return:
        """
        if not data:
            if dataFile:
                with open(dataFile, 'rb') as f:
                    r = self.base_put(url, data=f, **kwargs)
            else:
                r = self.base_put(url, data=data, **kwargs)
        else:
            r = self.base_put(url, data=data, **kwargs)

        status_code = str(r.status_code)

        # judge status code first.
        if expectStatusCode:
            self.test_status_code(status_code, str(expectStatusCode))
        # judge headers
        if expectHeaders:
            self.test_headers(self.handle_headers_string_to_dic(expectHeaders), r.headers)

        rr = {'headers': self.get_dict_from_string(r.headers), 'text': self.get_dict_from_string(r.text)}
        return rr

    def __post_multipart_test(self, url, json=None, dataFile=None, contentType=None, **kwargs):
        """
        :param url:
        :param json:
        :param dataFile:
        :param contentType:
        :param kwargs:
        :return:
        """
        # calculate payload.  You can try poster to get multipart-encode data. :)
        boundary = '----{0}'.format(hex(int(time.time() * 1000)))
        # boundary = "--------0x15d0c917807L"
        payload_list = ['--{0}'.format(boundary),
                        'Content-Disposition: form-data; name=\"file\"; filename=\"{0}\"'.format(dataFile)]
        if contentType:
            payload_list.append('Content-Type: {0}'.format(contentType))
        print("contentType: {0}".format(contentType))
        payload_list.append('\r\n')
        payload_list.append('--{0}--'.format(boundary))
        payload = '\r\n'.join(payload_list)
        print('==========post payload data: {0}'.format(payload))
        print('end post payload data=======')
        headers = {
            'Content-Type': "multipart/form-data; boundary={0}".format(boundary),
        }
        r = self.base_post(url, data=payload, json=json, tmpHeader=headers, **kwargs)
        # with open(dataFile, 'rb') as f:
        #     r = self.base_post(url, data=f, json=json, **kwargs)
        return r

    def post_test(self, url, data=None, json=None, dataFile=None, contentType=None, expectStatusCode=None,
                  expectHeaders=None, **kwargs):
        """
        :param json:
        :param contentType: if is 'guess', guess the type
        :param expectHeaders:judge headers. write it like headers=content-Type:image/png,content-md5,server. NO SPACE!!!
        :param expectStatusCode:judge the status of response. like 200/401/
        :param dataFile: when data not in use, you can use data file path.
        :param url:
        :param data:
        :param kwargs:

        :return:
        """
        print("dataFile type: {0}, dataFile: {1}".format(type(dataFile), dataFile))
        if contentType == 'guess':
            contentType = self.guess_type_from_file(dataFile)
            print("guess contentType is: {0}".format(contentType))
        if not data:
            if dataFile:
                r = self.__post_multipart_test(url, json, dataFile, contentType, **kwargs)
            else:
                r = self.base_post(url, data=data, json=json, **kwargs)
        else:
            r = self.base_post(url, data=data, json=json, **kwargs)

        status_code = str(r.status_code)

        # judge status code first.
        if expectStatusCode:
            self.test_status_code(status_code, str(expectStatusCode))
        # judge headers
        if expectHeaders:
            self.test_headers(self.handle_headers_string_to_dic(expectHeaders), r.headers)

        rr = {'headers': self.get_dict_from_string(r.headers), 'text': self.get_dict_from_string(r.text)}
        return rr


def test():
    ml = EssWrapper()

    # ml.get_signature(AccessKeySecret='213', Method="PUT", Date="sf, sds 3 45: s GMT", CanonicalizedResource="/test2/s.png")

    # headers = "content-Type:image/png,content-md5,server"
    # print ml.handle_headers_string_to_dic(headers)

    # headers_string = '''{'headers': u"{'Date':Tue, 06 Jun 2017 08:37:24 GMT,'Content-MD5':5EYtFiesMPz9moh8fVRAgw==,'Authorization':ESS a5ad00c5b27d2f674b0020e430c535f8:HZgWF1LivCe75+saE85lFUUjhjs=}"}'''
    # kwargs = {'headers': u"{'Date':'Tue, 06 Jun 2017 08:48:37 GMT','Content-MD5':'5EYtFiesMPz9moh8fVRAgw==','Authorization':'ESS a5ad00c5b27d2f674b0020e430c535f8:09iZbeMPvemEJ8fDWX6pqBNQL2A='}"}
    # ml.handle_http_kwargs(kwargs)
    # print(kwargs)
    # print(type(kwargs.get("headers")))

    print(ml.get_variables_from_yaml("..\\Variables\\constants_test.yml"))


def test_for_put_test():
    ml = EssWrapper()
    fileKey = "test/test1/test2/test_1M.tar.gz"
    C = ml.get_variables_from_yaml("constants.yml")
    bucket = C.get('pkgstore')
    url = bucket.get('baseUrl') + "/" + fileKey
    print(url)
    date = ml.get_date()
    dataFile = "test_1M.tar.gz"
    # contentType = ml.guess_type_from_file(dataFile)
    md5 = ml.get_file_md5(dataFile)
    kwargs1 = {
        'AccessKeyId': bucket.get('key'),
        'AccessKeySecret': bucket.get('pass'),
        'Method': 'PUT',
        # 'Content-Type': contentType,
        'Content-MD5': md5,
        'Date': date,
        # 'CanonicalizedHeaders': '',
        'BucketName': bucket.get('bucket'),
        'FileKey': fileKey,
        # 'CanonicalizedResource': '/' + bucket.get('bucket') + '/' + fileKey

    }
    print(kwargs1)
    headers = {'Date': date,
               # 'Content-Type': contentType,
               'Authorization': ml.get_authorization(**kwargs1),
               'Content-MD5': md5
               }
    ml.put_test(url, dataFile=dataFile, headers=headers, expectStatusCode=200)


def test_outer_get_with_auth():
    ml = EssWrapper()
    fileKey = "test/test_1M.tar.gz"
    C = ml.get_variables_from_yaml("constants.yml")
    bucket = C.get('pkgstore')
    url = bucket.get('outer').get('baseUrl') + "/" + fileKey
    print(url)
    date = ml.get_date()
    kwargs1 = {
        'AccessKeyId': bucket.get('key'),
        'AccessKeySecret': bucket.get('pass'),
        'Method': 'GET',
        'Content-Type': '',
        # 'Content-Type': contentType,
        'Content-MD5': '',
        'Date': date,
        'CanonicalizedHeaders': '',
        'BucketName': bucket.get('bucket'),
        'FileKey': fileKey,
        # 'CanonicalizedResource': '/' + bucket.get('bucket') + '/' + fileKey

    }
    print(kwargs1)
    headers = {'Date': date,
               # 'Content-Type': contentType,
               'Authorization': ml.get_authorization(**kwargs1),
               }
    ml.get_test(url, saveAs='get_test_1M.tar.gz', headers=headers)


def get_filekey_from_url(url):
    return "/".join(str(url).split("/")[3:])


def get_file_from_ess(url, saveas, **bucket):
    ml = EssWrapper()
    fileKey = get_filekey_from_url(url)
    # url = bucket.get('outer').get('baseUrl') + "/" + fileKey
    print(url)
    date = ml.get_date()
    kwargs1 = {
        'AccessKeyId': bucket.get('key'),
        'AccessKeySecret': bucket.get('pass'),
        'Method': 'GET',
        'Content-Type': '',
        # 'Content-Type': contentType,
        'Content-MD5': '',
        'Date': date,
        'CanonicalizedHeaders': '',
        'BucketName': bucket.get('name'),
        'FileKey': fileKey,
        # 'CanonicalizedResource': '/' + bucket.get('bucket') + '/' + fileKey

    }
    print(kwargs1)
    headers = {'Date': date,
               # 'Content-Type': contentType,
               'Authorization': ml.get_authorization(**kwargs1),
               }
    rr = ml.get_test(url, saveAs=saveas, expectStatusCode="200", headers=headers)
    return rr


def get_file_from_ess2(url, saveas, bucket_name='pkgstore'):
    ml = EssWrapper()
    fileKey = get_filekey_from_url(url)
    C = ml.get_variables_from_yaml("constants.yml")
    bucket = C.get(bucket_name)
    # url = bucket.get('outer').get('baseUrl') + "/" + fileKey
    print(url)
    date = ml.get_date()
    kwargs1 = {
        'AccessKeyId': bucket.get('key'),
        'AccessKeySecret': bucket.get('pass'),
        'Method': 'GET',
        'Content-Type': '',
        # 'Content-Type': contentType,
        'Content-MD5': '',
        'Date': date,
        'CanonicalizedHeaders': '',
        'BucketName': bucket.get('bucket'),
        'FileKey': fileKey,
        # 'CanonicalizedResource': '/' + bucket.get('bucket') + '/' + fileKey

    }
    print(kwargs1)
    headers = {'Date': date,
               # 'Content-Type': contentType,
               'Authorization': ml.get_authorization(**kwargs1),
               }
    rr = ml.get_test(url, saveAs=saveas, expectStatusCode="200", headers=headers)
    return rr


def test_for_get_test():
    ml = EssWrapper()
    fileKey = "$@@& 1.jpg"
    url = 'http://test2.essintra.ejudata.com:8084/' + fileKey
    print(ml.get_test(url))


def test_for_post_test():
    ml = EssWrapper()

    url = 'http://test1.essintra.ejudata.com:8084'
    dataFile = u"D:\worktest\kapalai-robot\Resources/original/1.jpg"

    print(ml.post_test(url, dataFile=dataFile, contentType='guess', headers=None, json=None))


def test_for_post_test2():
    ml = EssWrapper()
    C = ml.get_variables_from_yaml("..\\Variables\\constants.yml")
    fileKey = "1.jpg"
    url = 'http://test2.essintra.ejudata.com:8084/'
    date = ml.get_date()
    # date = 'Thu, 15 Jun 2017 06:33:32 GMT'
    dataFile = "D:\worktest\kapalai-robot\Resources\original\\1.jpg"
    # contentType = ml.guess_type_from_file(dataFile)
    contentType = "multipart/form-data"
    md5 = ml.get_file_md5(dataFile)
    kwargs1 = {
        'AccessKeyId': C.get('priw').get('key'),
        'AccessKeySecret': C.get('priw').get('pass'),
        'Method': 'POST',
        'Content-Type': contentType,
        'Content-MD5': md5,
        'Date': date,
        'CanonicalizedHeaders': '',
        'BucketName': 'test2',
        'FileKey': '',
        # 'CanonicalizedResource': '/test2/test.png'

    }
    print(kwargs1)
    headers = {'Date': date,
               'Content-Type': contentType,
               'Authorization': ml.get_authorization(**kwargs1),
               'Content-MD5': md5
               }
    ml.post_test(url, dataFile=dataFile, headers=headers, contentType="guess")


def get_bucket_from_url(url):
    return url.split("//")[1].split(".")[0]


if __name__ == '__main__':
    # test()
    # test_for_post_test()
    # test_for_post_test2()
    # test_for_put_test()
    # test_outer_get_with_auth()
    # test_for_get_test()
    # aa= get_file_from_ess("http://jobs.ess.ejucloud.cn/1512544662421398765", '1512544662421398765.txt', bucket_name='jobs')
    # print(aa)
    print(get_bucket_from_url("http://jobs.ess.ddd/cjoa"))
