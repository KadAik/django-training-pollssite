from celery import shared_task

import pathlib, os, shutil
from .models import User, FileUploadTracker
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse


@shared_task()
def handle_file_upload_task(file_name, file_extension, chunk_data, chunk_index, total_chunks, user_id):

    # Create a temp dir to store chunks
    temp_dir = pathlib.Path(settings.MEDIA_ROOT, "uploads", "temp", file_name)
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Generate a temporary chunk file name
    chunk_name = file_name + "_" + str(chunk_index)
    chunk_path = temp_dir / chunk_name

    # Track received chunks
    # Create a new tracker or get the existing one
    user = User.objects.get(pk=user_id)
    file_tracked, created = FileUploadTracker.objects.get_or_create(
        file_name=file_name,
        user=user,
        total_chunks=total_chunks,
    )

    # Update the chunk count : be aware of concurrency and race conditions
    file_tracked.update_chunk_count()

    print(f"Chunk count : {file_tracked.chunk_count}")

    # Save the current chunk
    with default_storage.open(chunk_path, "wb") as chunk_file:
        #for fragment in chunk_data.chunks():
        chunk_file.write(chunk_data)

    # If all chunk are received, reassemble them and cleanup
    if file_tracked.chunk_count == total_chunks:
        print(f"Chunk {chunk_index} is received")

        file_path = pathlib.Path(settings.MEDIA_ROOT, "uploads", file_name + file_extension)
        with default_storage.open(file_path, "wb") as final_file:
            for i in range(1, total_chunks + 1):
                chunk_path = temp_dir / f"{file_name}_{i}"
                with default_storage.open(chunk_path, "rb") as current_chunk:
                    final_file.write(current_chunk.read())
                # Then we delete the chunk after it is reassembled
                os.remove(chunk_path)

        # Clean up temp directory after reassembly
        shutil.rmtree(temp_dir)

    #     return JsonResponse({'status': 'File uploaded and reassembled successfully'})
    #
    # # Return success response for each chunk
    # return HttpResponse(status=200)