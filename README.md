# django-jogiyo

Django Rest Framework로 개발한 요기요 copy API입니다.

## Getting Started
---

### Prerequisites

.secrets/base.json
```python
{
  "SECRET_KEY": { Django Proejct SECRET_KEY },
  "EMAIL_HOST_USER": { EMAIL_HOST_UESR },
  "EMAIL_HOST_PASSWORD": { EMAIL_HOST_PASSWORD }
}
```

.secrets/dev.json
```python
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.contrib.gis.db.backends.postgis",
      "HOST": { RDS HOST },
      "NAME": { DB NAME },
      "USER": { AWS USER },
      "PASSWORD": { AWS PASSWORD },
      "PORT": { RDS PORT }
    }
  },
  "AWS_ACCESS_KEY_ID": { AWS S3 ACCESS_KEY_ID },
  "AWS_SECRET_ACCESS_KEY": { AWS S3 SECRET_ACCESS_KEY },
  "AWS_STORAGE_BUCKET_NAME": { AWS_STORAGE_BUCKET_NAME },
  "ALLOWED_HOSTS": [ ALLWED_HOSTS ]
}
```


.secrets/production.json
```python
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.contrib.gis.db.backends.postgis",
      "HOST": { RDS HOST },
      "NAME": { DB NAME },
      "USER": { AWS USER },
      "PASSWORD": { AWS PASSWORD },
      "PORT": { RDS PORT }
    }
  },
  "AWS_ACCESS_KEY_ID": { AWS S3 ACCESS_KEY_ID },
  "AWS_SECRET_ACCESS_KEY": { AWS S3 SECRET_ACCESS_KEY },
  "AWS_STORAGE_BUCKET_NAME": { AWS_STORAGE_BUCKET_NAME },
  "ALLOWED_HOSTS": [ ALLWED_HOSTS ],
  "SENTRY_DNS": { SENTRY_DNS }
}
```

### requirements
```shell
pip install -r requiments.txt
```

### API Docs

[API DOCS](https://jogiyo.co.kr/docs/)