from rest_framework.routers import SimpleRouter, Route, DefaultRouter


class DetailOnlyRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        )
    ]


class DetailReadOnlyRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        )
    ]
