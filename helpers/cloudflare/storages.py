from storages.backends.s3 import S3Storage
from decouple import config as env_config



class StaticFileStorage(S3Storage):
    location = "static"
    

    def url(self, name, **kwargs):
        return f"https://static.voidback.com/static/{name}"



class MediaFileStorage(S3Storage):

    location = "media"

    def url(self, name, **kwargs):
        return f"https://media.voidback.com/media/{name}"




storageSettings = {
    "default": {
        "BACKEND": "helpers.cloudflare.storages.MediaFileStorage",
        "OPTIONS": {
            "bucket_name": "media",
            "endpoint_url": env_config("ENDPOINT", cast=str, default=""),
            "access_key": env_config("ACCESS_KEY_ID", cast=str, default=""),
            "secret_key": env_config("SECRET_ACCESS_KEY", cast=str, default=""),
            "file_overwrite": False,
            "default_acl": "public-read",
            "signature_version": "s3v4", # s3 v4 signature version
        },
    },

    "staticfiles": {
        "BACKEND": "helpers.cloudflare.storages.StaticFileStorage",
        "OPTIONS": {
            "bucket_name": "static",
            "endpoint_url": env_config("ENDPOINT"),
            "access_key": env_config("ACCESS_KEY_ID"),
            "secret_key": env_config("SECRET_ACCESS_KEY"),
            "file_overwrite": False,
            "default_acl": "public-read", # access control for staticfiles should be public
            "signature_version": "s3v4", # s3 v4 signature version

        },
    }
}
