import boto3

import requests

from urllib.parse import urlparse

from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

# AWS CloudFormation output of the Amazon S3 bucket created by the solution : s3://batch-ffmpeg-stack-bucketxxxx/

s3_bucket_url = "s3://batch-ffmpeg-stack-batchffmpegbucketd97ee012-ecqnbuy6q1jv/"

# Amazon S3 key of the media Asset uploaded on S3 bucket, to compute by FFmpeg command : test/myvideo.mp4

s3_key_input = "input/***.mp4"

# Amazon S3 key of the result of FFmpeg Command : test/output.mp4

s3_key_output = "output/***.mp4"

# EC2 instance family : `intel`, `arm`, `amd`, `nvidia`, `fargate`

compute = "intel"

job_name = "add-subtitles-video"

command={

    "name": job_name,

    #"global_options":  "",

    "input_url" : s3_bucket_url + s3_key_input,

   #"input_file_options" :,

    "output_url" : s3_bucket_url + s3_key_output,

    "output_file_options":  "-vf subtitles="+s3_bucket_url+s3_key_input+".srt "+" -c:a copy"

}
batch = boto3.client("batch")

result = batch.submit_job(

    jobName=job_name,

    jobQueue="batch-ffmpeg-job-queue-" + compute,

    jobDefinition="batch-ffmpeg-job-definition-" + compute,

    parameters=command,

)
print(result)