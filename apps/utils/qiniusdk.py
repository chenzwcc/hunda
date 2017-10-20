# -*- coding: utf-8 -*-


import qiniu
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'IMnNRIzuiOM0TSGEYmfDM_1Y4kUk_PNOuz6JEZW9'
secret_key = 'DVxCeP5uVl-KoLmNrtJ1IqmpkK75nzpNNXXf8Ph3'

# 构建鉴权对象
q = qiniu.Auth(access_key, secret_key)
# 要上传的空间
bucket_name = 'hunda'
domain_prefix = "http://oxr5eyw7q.bkt.clouddn.com/"


def qiniu_upload_file(file_name, source_file):
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, file_name, 3600)
    ret, info = qiniu.put_file(token, file_name, source_file)

    if info.status_code == 200:
        return domain_prefix + ret['key']
    return None