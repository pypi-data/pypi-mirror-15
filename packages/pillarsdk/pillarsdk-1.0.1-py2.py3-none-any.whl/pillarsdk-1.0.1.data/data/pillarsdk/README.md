# Pillar Python REST SDK
Integrate this module in your Python app to communicate with an Pillar server.


## Caching

[Requests-Cache](https://requests-cache.readthedocs.org/) can be used to
cache HTTP requests. The Pillar Python REST SDK does not support it
directly, but provides the means to plug in different session objects:

    import requests_cache
    import pillarsdk

    req_sess = requests_cache.CachedSession(backend='sqlite',
                                            cache_name='blender_cloud')
    pillarsdk.Api.requests_session = req_sess

Any `pillarsdk.Api` instance will now use the cached session. To
temporary disable it, use:

    api = pillarsdk.Api.Default(endpoint="https://your.endpoint")
    with api.requests_session.cache_disabled():
        node = pillarsdk.Node.find('1234')
