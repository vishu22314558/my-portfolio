import json
import boto3
from botocore.client import Config
import zipfile
import mimetypes
import io
from io import BytesIO
#SNS


def lambda_handler(event, context):
    
    #Create S3 object 
    try:
        job = event.get("CodePipeline.job")

        
        s3 = boto3.resource('s3', config = Config(signature_version = 's3v4'))
        sns = boto3.resource('sns')

        topic = sns.Topic('arn:aws:sns:us-east-1:244691138631:deployPortfolioTopic')

        # Create Bucekt Objects 
        
        portfolio_bucket = s3.Bucket('portfolio.svadhyaya.info')
        build_bucket = s3.Bucket('portfoliobuild.svadhyaya.info')
        
        #portfolio_zip = io.StringIO()
        portfolio_zip = BytesIO()
        
        build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm , ExtraArgs = {'ContentType' : mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL = 'public-read')
        
        topic.publish(Subject = "Updated Portfolio" , Message="We have deployed yout Portfolio")
    except:
        topic.publish(Subject = "Updated Portfolio" , Message="Deployment Failed")    
        raise
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

