import mimetypes
from functools import partial
from uuid import uuid4

from os.path import getsize
from tornado import gen


def encode_formdata(fields):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be
    uploaded as files.
    Return (content_type, body) ready for httplib.HTTP instance
    """
    boundary = '----' + uuid4().hex
    crlf = b'\r\n'
    l = []
    for (key, value) in fields:
        l.append(b'--' + boundary.encode())
        l.append(b'Content-Disposition: form-data; name="%s"' % key.encode())
        l.append(b'')
        l.append(value.encode())
    l.append(b'--' + boundary.encode() + b'--')
    l.append(b'')
    body = crlf.join(l)
    content_type = b'multipart/form-data; boundary=%s' % boundary.encode()
    return content_type, body


# Using HTTP POST, upload one or more files in a single multipart-form-encoded
# request.
@gen.coroutine
def multipart_producer(boundary, fields, files, write):
    '''
    :param boundary:
    :param fields: ((name, value),(name, value))
    :param files: ((name, filename, filepath),(name, filename, filepath))
    :param write:
    :return:
    '''
    boundary_bytes = boundary.encode()
    buf = b''
    for (key, value) in fields:
        buf = (
                (b'--%s\r\n' % boundary_bytes) +
                (b'Content-Disposition: form-data; name="%s"\r\n' % key.encode()) +
                b'\r\n' +
                value.encode() +
                b'\r\n'
        )
        yield write(buf)
    for (key, filename, filepath) in files:
        mtype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        buf += (
                (b'--%s\r\n' % boundary_bytes) +
                (b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' %
                 (key.encode(), filename.encode())) +
                (b'Content-Type: %s\r\n' % mtype.encode()) +
                b'\r\n'
        )
        yield write(buf)
        with open(filepath, 'rb') as f:
            while True:
                # 16k at a time.
                chunk = f.read(16 * 1024)
                if not chunk:
                    break
                yield write(chunk)

        yield write(b'\r\n')

    yield write(b'--%s--\r\n' % boundary_bytes)


def get_content_length(boundary, fields, files):
    boundary_bytes = boundary.encode()
    buf = b''
    length = 0
    for (key, value) in fields:
        buf = (
                (b'--%s\r\n' % boundary_bytes) +
                (b'Content-Disposition: form-data; name="%s"\r\n' % key.encode()) +
                b'\r\n' +
                value.encode() +
                b'\r\n'
        )
        length += len(buf)
    for (key, filename, filepath) in files:
        mtype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        buf += (
                (b'--%s\r\n' % boundary_bytes) +
                (b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' %
                 (key.encode(), filename.encode())) +
                (b'Content-Type: %s\r\n' % mtype.encode()) +
                b'\r\n'
        )
        length += len(buf)
        length += getsize(filepath)
        length += len(b'\r\n')
    length += len(b'--%s--\r\n' % boundary_bytes)
    return length


def get_multipart_producer(fields, files):
    '''
    :param fields: ((name, value),(name, value))
    :param files: ((name, filename, filepath),(name, filename, filepath))
    :return: content_type, str(length), producer
    '''
    boundary = uuid4().hex
    content_type = 'multipart/form-data; boundary=%s' % boundary
    length = get_content_length(boundary, fields, files)
    producer = partial(multipart_producer, boundary, fields, files)
    return content_type, str(length), producer
