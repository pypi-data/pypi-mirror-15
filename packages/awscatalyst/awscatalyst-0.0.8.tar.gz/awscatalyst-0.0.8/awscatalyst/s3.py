from __future__ import print_function

import boto3
import botocore.exceptions

from aws import Aws

class S3(Aws):
    def __init__(self, s3_resource=None):
        self._s3r = s3_resource or boto3.resource('s3')

    def safe_create_bucket(self, bucket_name, region=None):
        """
        Create S3 bucket in the specified region if it's not there, 
        and return the boto3 bucket object.
        """
        region = region or self.get_region()

        args = {Bucket: bucket_name}
        if region not in (None, 'us-east-1'):
            args.update({
                CreateBucketConfiguration: {"LocationConstraint": region}
            })

        try:
            return self._s3r.create_bucket(**args)
        except botocore.exceptions.ClientError:
            pass

        return self._s3r.Bucket(bucket_name)

    def upload(self, source, bucket_name, s3_key):
        """
        :param str source: file path or body
        :param bucket_name:
        :param s3_key:
        :return:
        """
        obj = self.safe_create_bucket(bucket_name).Object(s3_key)

        with open(source, 'rb') as fp:
            obj.put(Body=fp)

        return s3_key

    def cleanup_bucket(self, bucket_name):
        print("  * Cleaning up bucket `%s`" % bucket_name)
        bucket = self._s3r.Bucket(bucket_name)

        bucket.delete_objects(
            Delete={
                "Objects": [
                    {"Key": obj.key} for obj in bucket.objects.all()
                ]
            }
        )
