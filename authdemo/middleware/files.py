"""
This middleware handles all request related to files upload and download
"""
from django.shortcuts import reverse


class FileUploadMiddleware:
    """
    If an incoming request is for file uploading; for each chunk send by the client
    this middleware put all related chunks in an unbounded queue which will be consumed
    in the arrival order FIFO.
    For a different file_name, different queue will be created
    """

    def __int__(self, get_response):
        self.get_response = get_response

    def  __call__(self, request):
        # Is the request for file upload ?
        if request.path == reverse("authdemo:upload"):
