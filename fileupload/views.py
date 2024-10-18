from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
import pandas as pd
from django.core.mail import send_mail
from django.conf import settings

class FileUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            
            # Check file type and read data
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)

            # Create summary report
            row_count = len(df)
            columns = df.columns.tolist()
            summary = f"Rows: {row_count}, Columns: {', '.join(columns)}"

            # Send summary email
            subject = 'Python Assignment - Arpreet Khare'
            message = f"Summary Report:\n\nRows: {row_count}\nColumns: {', '.join(columns)}"
            recipient = 'tech@themedius.ai'

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient],
                fail_silently=False,
            )

            # Return response with summary
            return Response({'message': 'File processed successfully', 'summary': summary}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
