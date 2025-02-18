from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import User, Patient, HeartRateRecord
from .serializers import UserSerializer, PatientSerializer, HeartRateRecordSerializer
from django_filters import rest_framework as filters
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import Q

# Create your views here.

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not enforce CSRF

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(request, username=email, password=password)
    if user:
        login(request, user)
        serializer = UserSerializer(user)
        return Response({
            'message': 'Login successful',
            'user': serializer.data
        })
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

class PatientViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['first_name', 'last_name', 'gender']

class HeartRateFilter(filters.FilterSet):
    heart_rate_min = filters.NumberFilter(field_name='heart_rate', lookup_expr='gte')
    heart_rate_max = filters.NumberFilter(field_name='heart_rate', lookup_expr='lte')
    recorded_at_after = filters.DateTimeFilter(field_name='recorded_at', lookup_expr='gte')
    recorded_at_before = filters.DateTimeFilter(field_name='recorded_at', lookup_expr='lte')

    class Meta:
        model = HeartRateRecord
        fields = ['patient', 'heart_rate_min', 'heart_rate_max', 'recorded_at_after', 'recorded_at_before']

class HeartRateRecordViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [permissions.AllowAny]
    queryset = HeartRateRecord.objects.all()
    serializer_class = HeartRateRecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = HeartRateFilter

    def get_queryset(self):
        queryset = HeartRateRecord.objects.all()
        
        # Get filter parameters
        patient_id = self.request.query_params.get('patient_id')
        heart_rate_min = self.request.query_params.get('heart_rate_min')
        heart_rate_max = self.request.query_params.get('heart_rate_max')
        
        # Apply filters
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if heart_rate_min:
            queryset = queryset.filter(heart_rate__gte=heart_rate_min)
        if heart_rate_max:
            queryset = queryset.filter(heart_rate__lte=heart_rate_max)
            
        return queryset
