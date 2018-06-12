import os
import json
import sys
import datetime
import time

from secu.controls.__ueditor_config import img_config
from ..base.request import BaseHandler, JsonResponse
from ..base.decrators import authenticated, handle_request_exception
import config as conf


class _Ueditor(BaseHandler):
    @handle_request_exception
    def prepare(self):
        if not hasattr(_Ueditor, 'config'):
            _Ueditor.config = img_config
            # config = ''
            # with open(os.path.dirname(os.path.abspath(__file__)) + '/config.json', 'r', encoding='utf-8') as f:
            #     config = f.read()
            # _Ueditor.config = json.loads(config)
        super(_Ueditor, self).prepare()

    @handle_request_exception
    def get(self):
        action = self.request.query_arguments.get('action', '')
        if action and len(action) > 0:
            action = action[0].decode()
        if action == 'config':
            callback = self.request.query_arguments.get('callback', '')
            if callback and len(callback) > 0:
                callback = callback[0].decode()
            if callback == '':
                self.write(json.dumps(_Ueditor.config))
            else:
                self.write(callback + '(' + json.dumps(_Ueditor.config) + ')')
        elif action == 'listimage':
            self.write('')
            # return JsonResponse(self, '50000', msg='get request is invoked', data=item_info)

    @handle_request_exception
    def post(self):
        # print(self.request.query_arguments.get)
        # print(self.request.files)
        action = self.request.query_arguments.get('action', '')
        if action and len(action) > 0:
            action = action[0].decode()
        if action == "uploadimage":
            upload_handler = Upload(self.request, **{
                'AllowExtensions': _Ueditor.config.get("imageAllowFiles"),
                'PathFormat': _Ueditor.config.get("imagePathFormat"),
                'SizeLimit': _Ueditor.config.get("imageMaxSize"),
                'UploadFieldName': _Ueditor.config.get("imageFieldName"),
                'UrlPrefix': _Ueditor.config.get("imageUrlPrefix")
            })
        elif action == "uploadscrawl":
            upload_handler = Upload(self.request, **{
                'AllowExtensions': [".png"],
                'PathFormat': _Ueditor.config.get("scrawlPathFormat"),
                'SizeLimit': _Ueditor.config.get("scrawlMaxSize"),
                'UploadFieldName': _Ueditor.config.get("scrawlFieldName"),
                'Base64': True,
                'Base64Filename': "scrawl.png",
                'UrlPrefix': _Ueditor.config.get("scrawlUrlPrefix")
            })
        elif action == "uploadvideo":
            upload_handler = Upload(self.request, **{
                'AllowExtensions': _Ueditor.config.get("videoAllowFiles"),
                'PathFormat': _Ueditor.config.get("videoPathFormat"),
                'SizeLimit': _Ueditor.config.get("videoMaxSize"),
                'UploadFieldName': _Ueditor.config.get("videoFieldName"),
                'UrlPrefix': _Ueditor.config.get("videoUrlPrefix")
            })
        elif action == "uploadfile":
            upload_handler = Upload(self.request, **{
                'AllowExtensions': _Ueditor.config.get("fileAllowFiles"),
                'PathFormat': _Ueditor.config.get("filePathFormat"),
                'SizeLimit': _Ueditor.config.get("fileMaxSize"),
                'UploadFieldName': _Ueditor.config.get("fileFieldName"),
                'UrlPrefix': _Ueditor.config.get("fileUrlPrefix")
            })
        response = ''
        if upload_handler:
            response = upload_handler.run()
        # elif action == "listimage":
        #     action = ListFileManager(self.request.files, _Ueditor.config.get("imageManagerListPath"), _Ueditor.config.get("imageManagerAllowFiles"))
        # elif action == "listfile":
        #     action = ListFileManager(self.request.files, _Ueditor.config.get("fileManagerListPath"), _Ueditor.config.get("fileManagerAllowFiles"))
        # elif action == "catchimage":
        #     action = CrawlerHandler(self.request.files)
        # print(sys.path[0])
        # print(os.path.dirname(os.path.abspath(__file__)))

        # img有三个键值对可以通过img.keys()查看
        # 分别是 'filename', 'body', 'content_type' 很明显对应着文件名,内容(二进制)和文件类型
        # with open(os.path.dirname(os.path.abspath(__file__)) + '/' + img['filename'], 'wb') as f:
        #     # 文件内容保存 到'/static/uploads/{{filename}}'
        #     f.write(img['body'])
        #
        print(response)
        self.write(json.dumps(response))

    @staticmethod
    def ResultResponse():
        pass


class Upload(object):
    class STATE(object):
        Success = 'SUCCESS'
        FileAccessError = '文件访问出错，请检查写入权限'
        SizeLimitExceed = '文件大小超出服务器限制'
        TypeNotAllow = '不允许的文件格式'
        NetworkError = '网络错误'
        Unknown = '未知错误'

    def __init__(self, request, **config):
        self.config = config
        self.request = request
        self.result = {'state': Upload.STATE.Unknown, 'url': '', 'originFileName': '', 'errorMessage': ''}

    def checkFileType(self, file):
        file_list = file['filename'].split('.')
        if len(file_list) >= 2:
            return self.config.get('AllowExtensions', '').__contains__('.' + file_list[len(file_list) - 1])
        else:
            return False

    def checkFileSize(self, size):
        return self.config.get('SizeLimit', 0) > int(size)

    def run(self):
        rootpath = conf.STATIC['LOCALPATH']
        for file in self.request.files.get(self.config.get('UploadFieldName')):
            if (not file) and (not file.get('filename')) and (not file.get('size')) and (not file.get('body')):
                self.result['state'] = Upload.STATE.NetworkError
            elif not self.checkFileType(file):
                self.result['originFileName'] = file.get('filename')
                self.result['state'] = Upload.STATE.TypeNotAllow
            elif not self.checkFileSize(self.request.headers['Content-Length']):
                self.result['state'] = Upload.STATE.SizeLimitExceed
            else:
                try:
                    path_obj = self.getFormatePath(file.get('filename'))
                    # self.result['url'] = self.config.get('UrlPrefix', '') + '/' + path_obj['path_file']
                    self.result['url'] = conf.STATIC['URL'] + path_obj['path_file']
                    dir_path = rootpath + '/' + path_obj['path_dir']
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    print(rootpath + '/' + path_obj['path_file'])
                    # 文件内容保存 到'/static/uploads/{{filename}}'
                    with open(rootpath + '/' + path_obj['path_file'], 'wb') as f:
                        f.write(file['body'])
                    self.result['originFileName'] = file.get('filename')
                    self.result['state'] = Upload.STATE.Success
                    # 同步远程文件服务器
                    remotes = conf.STATIC.get('REMOTES')
                    if remotes:
                        for remote in remotes:
                            scpcmd = "scp -r {0} {1}".format(rootpath + '/' + path_obj['path_file'],
                                                             os.path.join(remote, path_obj['path_file']))
                            os.system(scpcmd)
                            print(scpcmd)
                except Exception as e:
                    self.result['errorMessage'] = str(e)

        return {
            'state': self.result['state'],
            'url': self.result['url'],
            'title': self.result['originFileName'],
            'original': self.result['originFileName'],
            'error': self.result['errorMessage']
        }

    # @staticmethod
    # def getStateMessage(state):
    #     if state == 0:
    #         return Upload.STATE.Success
    #     elif state == -1:
    #         return Upload.STATE.SizeLimitExceed
    #     elif state == -2:
    #         return Upload.STATE.TypeNotAllow
    #     elif state == -3:
    #         return Upload.STATE.FileAccessError
    #     elif state == -4:
    #         return Upload.STATE.NetworkError
    #     else:
    #         return Upload.STATE.Unknown

    def getFormatePath(self, file_name):
        pathFormat = "{filename}{timestamp}"
        if self.config.get('PathFormat', '') != '':
            pathFormat = self.config['PathFormat']

        file_list = file_name.split('.')
        if len(file_list) >= 2:
            extension = file_list[len(file_list) - 1]
            file_name = file_name[:-(len(extension) + 1)]
        else:
            extension = 'jpg'
            file_name = file_name

        now_datetime = datetime.datetime.today()

        pathFormat = pathFormat.replace("{yyyy}", str(now_datetime.year))
        pathFormat = pathFormat.replace("{yy}", str(datetime.datetime.today().year)[-2:])
        pathFormat = pathFormat.replace("{mm}", ('0' + str(now_datetime.month))[-2:])
        pathFormat = pathFormat.replace("{dd}", ('0' + str(now_datetime.day))[-2:])
        path_dir = pathFormat.replace('{filename}', '')
        path_dir = path_dir.replace('{timestamp}', '')
        pathFormat = pathFormat.replace("{timestamp}", str(int(time.mktime(now_datetime.timetuple()))))
        pathFormat = pathFormat.replace("{filename}", file_name)

        return {'path_dir': path_dir, 'path_file': pathFormat + '.' + extension}
