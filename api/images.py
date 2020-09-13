"""
Image REST API
=================

Serializer and view to enable the rest framework for the user model abs

:Author: Nik Sumikawa
:Date: June 20, 2020
"""

import logging
log = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes


from django.http import JsonResponse
from django.conf.urls import url
from django.db.models import Q, F

from oAuth.models import User
from images.models import Images
from django_config.rest_framework import RestFramework


# class DocumentationSchema(AutoSchema):
#     """
#     Overrides `get_link()` to provide Custom Behavior X
#     """
#     def __init__( self ):
#         super().__init__()
#
#     def get_tags(self, path, method):
#
#         return ['System Metadata']
#
#     def get_filter_parameters(self, view, method):
#         from docs.rest.parameters.system_metadata.data.product import parameters
#         return parameters
#
#     def get_responses(self, path, method):
#         from docs.rest.responses.system_metadata.data.product import responses
#         return responses




@authentication_classes([])
@permission_classes([])
class ImageAPI(RestFramework):

    # schema = DocumentationSchema()

    def get(self, request):
        """ returns the image and user parameters based on the provided attributes """

        from django_config.request_params import request_params

        # parse the parameter from the request
        params = request_params(request)

        objects = self.query( Images, **params )


        # return JsonResponse( objects.values(), safe=False )
        return Response(data=objects.values(
            'id',
            'url',
            'date',
            'user__id',
        ))



    def post(self, request):
        """ Create an object that connects the image url with the user object """

        import json

        # parses the json object from the body of the post request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        # retrieve the user object corresponding to the user ID
        user_obj = User.objects.get( id = body['user_id'] )

        # buffer to hold the id of all created objects
        images = []

        for url in body['image_url'].split(','):

            # create the image object
            obj = Images.objects.get_or_create(
                url=url,
                user= user_obj,
                )[0]

            # update the output buffer
            images.append( {
                'url': url,
                'user_id': user_obj.id,
                'id': obj.id
                })


        return Response(data={'images': images})


    # def authenticate(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #
    #
    #     from rest_framework.authentication import TokenAuthentication
    #
    #     if self.request.method == 'POST':
    #         authentication_classes = [TokenAuthentication]
    #
    #     else:
    #         authentication_classes = []
    #
    #     return [authentication() for authentication in authentication_classes]


    def query_parameters( self, variable, var_list ):
        """ returns a dictionary containing all queryset parameters """

        return {
            'id': Q(id__in = var_list ),
            'user_id': Q(user__id = var_list ),
        }



urlpatterns = [
    url(r'^images$', ImageAPI.as_view(), name='ImageAPI'),
]
