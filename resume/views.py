from django.shortcuts import render

# Create your views here.
def resume_view(request):
    return render(request, 'ramki.html')

# views.py

from django.http import HttpResponse
from azure.storage.blob import BlobServiceClient
import os

def download_resume(request):
    # Azure Blob Storage credentials (secure storage method recommended)
    azure_storage_connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    blob_container_name = "resume"
    blob_name = "Ramki_Python.pdf"  # Name of the PDF file in Azure Blob Storage

    try:
        # Connect to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
        blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=blob_name)

        # Download the PDF file from Azure Blob Storage to a temporary file
        temp_file_path = "/tmp/" + blob_name  # Change the path as per your environment
        with open(temp_file_path, "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())

        # Serve the file as a downloadable response
        with open(temp_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Ramki_Python.pdf"'
            return response
    
    except Exception as e:
        # Handle exceptions (e.g., Azure connection errors, file not found)
        return HttpResponse(f"Error downloading file: {str(e)}", status=500)
    
    finally:
        # Clean up: Delete the temporary file after serving
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
