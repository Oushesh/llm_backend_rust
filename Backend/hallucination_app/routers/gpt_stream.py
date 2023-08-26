from django.http import StreamingHttpResponse
import subprocess
from ninja import Router
import os, sys

router = Router()

# Get the absolute path of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the project root directory (three levels up from loaders.py)
project_root = os.path.abspath(
    os.path.join(current_script_dir, "../../../../rust_core/ggml")
)


# The subprocess command
@router.get("/stream")
def generate_output(request):
    def stream_output():
        command = [
            ".project_root/build/bin/gpt-2",
            "-m",
            "project_root/models/gpt-2-117M/ggml-model-gpt-2-1558M.bin",
            "-p",
            "What is the capital of France?",
        ]

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            for line in iter(process.stdout.readline, ""):
                yield line
        except Exception as e:
            yield f"An error occurred: {e}"

    response = StreamingHttpResponse(stream_output(), content_type="text/plain")
    return response
