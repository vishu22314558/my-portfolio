import json
import boto3
from botocore.client import Config
import zipfile
import mimetypes
import io
from io import BytesIO

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

portfolio_bucket = s3.Bucket('portfolio.svadhyaya.info')

build_bucket = s3.Bucket('portfoliobuild.svadhyaya.info')

# On Windows, this will need to be a different location than /tmp
build_bucket.download_file('portfoliobuild.zip', '/tmp/portfoliobuild.zip')

with zipfile.ZipFile('/tmp/portfoliobuild.zip') as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm , ExtraArgs = {'ContentType' : mimetypes.guess_type(nm)[0]})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')