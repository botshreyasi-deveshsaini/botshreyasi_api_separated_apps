from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from helper.views import *

@method_decorator(csrf_exempt,name='dispatch')
class getCvparsedTotalApplication(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        print(":---------------------------->")
        # print(self.request.query_params.get('start'))
        start = request.GET.get('start')
        end =request.GET.get('end')
        appid = GetAppID()
        getQueary = f'call callandcvparsedtotalReportapi({appid},{start},{end})'
        print(getQueary)
    # return \DB::connection('mysqlslave')->select('call callandcvparsedtotalReportapi(:appid,:start,:end)', $param);
        app_id = GetAppID()
        return Response('true')

