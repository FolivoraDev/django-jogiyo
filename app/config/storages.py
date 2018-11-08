from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    # 이 Storage를 사용해서 저장되는 파일들이
    # <location의 값>/<추가경로> 부분에 저장됨
    location = 'media'
    default_acl = 'private'


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'