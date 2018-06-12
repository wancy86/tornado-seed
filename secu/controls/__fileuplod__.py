import json
import uuid
import os
import zipfile
import filetype
import tornado
import urllib.parse
from tornado import gen, httpclient
from tornado.web import RequestHandler, stream_request_body
from sqlalchemy import func, and_

import config
from secu.controls.polyv_upload import POLYVUpload
from ..base.decrators import authenticated, handle_request_exception
from ..base.request import BaseHandler, JsonResponse
from common.json import json_by_result
import config as conf
from common.streamrequest import PostDataStreamer

MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB


@stream_request_body
class StreamFileUploadHandler(RequestHandler):

    def initialize(self):
        self.request.connection.set_max_body_size(GB)
        self.request.connection.set_body_timeout(7200)

    def prepare(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        try:
            total = int(self.request.headers.get("Content-Length", "0"))
        except:
            total = 0
        rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.tmpdir = os.path.join(rootpath, 'tempfiles')
        self.ps = PostDataStreamer(total, self.tmpdir)

    def data_received(self, chunk):
        self.ps.receive(chunk)

    def options(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
        self.set_header('Access-Control-Max-Age', 86400)
        self.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        self.write('')

    @handle_request_exception
    def get(self):
        html = ''' 
                    <html>
                      <head><title>Upload File</title></head>
                      <body>
                        <form action='/service/secu/file-stream-upload' enctype="multipart/form-data" method='post'>
                            <input type='file' name='file'/><br/>
                            <input name="ACTION" type="text" value="UP-IMAGE"><br>
                            <input type='submit' value='submit'/>
                        </form>
                      </body>
                    </html>
                '''
        self.write(html)

    # 仅支持单文件上传
    @handle_request_exception
    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        try:
            self.ps.finish_receive()
            paras = self.ps.get_values(self.ps.get_nonfile_names())
            ACTION, file = paras.get('ACTION'), None

            for part in self.ps.parts:
                filename = self.ps.get_part_ct_param(part, "filename", None)
                if filename:
                    file = {
                        'filename': filename,
                        'filesize': part['size'],
                        'filepath': part["tmpfile"].name,
                        'tmpfilename': part['tmpfilename'],
                    }
                    break

            for part in self.ps.parts:
                part["tmpfile"].close()

            url, remotepath, extension = '', '', ''
            if file:
                kind = filetype.guess(file['filepath'])
                if kind:
                    extension = kind.extension
                else:
                    extension = file['filepath'][file['filepath'].rfind('.') + 1:]
                if ACTION == b'UP-IMAGE':  # 上传图片
                    if extension not in ('jpg', 'png', 'gif', 'bmp', 'ico'):
                        return JsonResponse(self, '002', msg='请上传图片文件')
                    else:
                        remotepath = os.path.join('images', file['tmpfilename'])
                        url = url + remotepath.replace('\\', '/')
                elif ACTION == b'UP-VIDEO':  # 上传视频
                    if extension != 'mp4':
                        return JsonResponse(self, '002', msg='请上传MP4文件')
                    else:
                        remotepath = os.path.join('videos', file['tmpfilename'])
                        url = url + remotepath.replace('\\', '/')

                elif ACTION == b'UP-H5-VIDEO':  # 上传H5视频
                    if extension != 'mp4':
                        return JsonResponse(self, '002', msg='请上传MP4文件')
                    else:
                        remotepath = os.path.join('videos', file['tmpfilename'])
                        url = url + remotepath.replace('\\', '/')

                elif ACTION == b'UP-H5-SITE':  # 上传H5课件
                    if extension != 'zip':
                        return JsonResponse(self, '002', msg='请上传ZIP文件')
                    else:
                        remotepath = os.path.join('h5', file['tmpfilename'].split('.')[0])
            print(remotepath)
            # H5网站需要解压处理
            if extension == 'zip':
                with zipfile.ZipFile(file['filepath']) as zf:
                    zf.extractall(os.path.join(self.tmpdir, 'h5', file['tmpfilename'].split('.')[0]))
                    zf.close()
                # 解压后文件路径
                file['filepath'] = os.path.join(self.tmpdir, 'h5', file['tmpfilename'].split('.')[0])
                url = url + 'h5/' + file['tmpfilename'].split('.')[0] + '/'
            scpcmd = ''
            # 同步远程文件服务器
            if ACTION != b'UP-VIDEO' and ACTION != b'UP-H5-VIDEO':
                remotes = conf.STATIC.get('REMOTES')
                if remotes:
                    for remote in remotes:
                        scpcmd = "scp -r {0} {1}".format(file['filepath'], os.path.join(remote, remotepath))
                        os.system(scpcmd)

            # 上传保利威视
            polyv_result, vendor_url, polyv_response = '', {}, ''
            if ACTION == b'UP-VIDEO':  # 上传视频
                polyv_response = yield POLYVUpload().asyncUpload(file['filepath'], config.VIDEO_CATAID,
                                                                 file['tmpfilename'], 'video', '')
            elif ACTION == b'UP-H5-VIDEO':  # 上传H5视频
                polyv_response = yield POLYVUpload().asyncUpload(file['filepath'], config.H5_CATAID,
                                                                 file['tmpfilename'], 'h5', '')
            if polyv_response:
                polyv_result = polyv_response.body
                polyv_result = json.loads(polyv_result)
                if polyv_result['error'] == '0':
                    vendor_url['url1'] = polyv_result['data'][0].get('mp4_1')
                    vendor_url['url2'] = polyv_result['data'][0].get('mp4_2')
                    vendor_url['url3'] = polyv_result['data'][0].get('mp4_3')
            url = conf.STATIC['URL'] + urllib.parse.quote(url)

            JsonResponse(self, '000', msg='请求处理成功', data={'url': url, 'vendor_url': json.dumps(vendor_url)})
        except Exception as e:
            raise e
        finally:
            self.ps.release_parts()
            self.finish()
