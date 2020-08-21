import os
import paramiko
from client import RemoteClient
from paramiko import BadHostKeyException, AuthenticationException, SSHException
from scp import SCPException, SocketTimeout


def sync_dir(
    local_dir="/home/mike/googledrive/reMarkable",
    remote_dir="/home/root/koreader/01-pdfs",
    retries=100,
):

    fail = 0
    success = 0
    while (success == 0) and (fail < retries):
        print()
        try:
            remote_client = RemoteClient()
            success += 1
        except (
            TimeoutError,
            BadHostKeyException,
            AuthenticationException,
            SSHException,
            SCPException,
            SocketTimeout,
        ) as e:
            if fail < retries:
                print(f"{e} retrying... {retries - fail} left")
                fail += 1
            else:
                break

    local_pdf_files = [f for f in os.listdir(local_dir) if f.endswith(".pdf")]
    remote_files = remote_client.execute_commands([f"cd {remote_dir} && ls"])
    print(f"Local Files {local_pdf_files}")
    print(f"KOR Files {remote_files}")

    print(f"Removing {len(remote_files)} files from reMarkable:{remote_dir}")
    remote_client.execute_commands([f"rm -rf {remote_dir}/*"])

    print(f"Uploading {len(local_pdf_files)} from {local_dir}")
    remote_client.bulk_upload(
        [os.path.join(local_dir, file) for file in local_pdf_files]
    )


if __name__ == "__main__":
    sync_dir()
