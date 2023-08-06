---
service_name: "Wheres Your Trash Django Application"
subdomain: www
domain_name: wheresyourtrash.com
ssl_enabled: True
app_name: wheresyourtrash
deployment_path: /home
deployment_name: wyt_production 
gunicorn_workers: 2
django_state: Prod
django_port: 10910
django_sentry_code: https://9c043a8153a24eb99ad89c65045459c9:2203bd97fcc04dfb9710daeb16a67b15@app.getsentry.com/82313
django_secret_key: KLJSDLFKJjLKSDjf82938ujoKLJSDF9j203jfsdf
django_admin: admin@wheresyourtrash.com
django_pass: Lauren renter's skyjacker Leonard
database_pass: kjsldfjoi2j3flksjldfkjsldfkajdoijf90sdfj
django_database: postgres://{{deployment_name}}:{{database_pass}}@localhost/{{deployment_name}}
email_host: smtp.sparkpostmail.com
email_host_user: SMTP_Injection
email_host_password: 7c27e4866adc6f58f9a879b785742a0119c09119
email_host_port: 587
use_aws: true
bower_enabled: false
aws_access_key: AKIAIFRTE72QLLQS5WXA
aws_secret_key: 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
celery_enabled: true
celerybeat_enabled: true
