"""
Module provides factory method to integrate Redis with Flask app.
"""
import redis


class FlaskRedis(object):
    def __init__(self, app=None, strict=True, config_prefix="REDIS", **kwargs):
        self._redis_client = None
        self.provider_class = redis.StrictRedis if strict else redis.Redis
        self.provider_kwargs = kwargs
        self.config_prefix = config_prefix

        if app is not None:
            self.init_app(app)

    def init_app(self, app, **kwargs):
        redis_url = app.config.get(
            "{0}_URI".format(self.config_prefix), "redis://localhost:6379/0"
        )

        self.provider_kwargs.update(kwargs)
        self._redis_client = self.provider_class.from_url(
            redis_url, **self.provider_kwargs
        )

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions[self.config_prefix.lower()] = self

    def set(self, name, value, expiry):
        return self._redis_client.set(name, value, expiry)

    def get(self, name):
        return self._redis_client.get(name)

    def delete(self, name):
        return self._redis_client.delete(name)
