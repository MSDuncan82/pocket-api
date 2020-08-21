"""""Client to handle connections and actions executed against a remote host."""
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException
import os
import dotenv

dotenv.load_dotenv()


class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(
        self,
        host=os.environ["REMOTE_HOST"],
        user=os.environ["REMOTE_USER"],
        password=os.environ["REMOTE_PASS"],
        ssh_key_filepath=None,
        remote_path=os.environ["KOR_PATH"],
    ):
        self.host = host
        self.user = user
        self.ssh_key_filepath = ssh_key_filepath
        self.remote_path = remote_path
        self.client = self.connect(host, user, password)
        print("SSH Connected")
        self.scp = SCPClient(self.client.get_transport())
        print("SCP Connected")

    def __del__(self):

        if self.client:
            print("Disconnecting...")
            self.disconnect()

    def disconnect(self):
        """Close ssh connection."""
        if self.client:
            self.client.close()
        if self.scp:
            self.scp.close()

    def connect(self, host, user, password, timeout=10):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(host, username=user, password=password, timeout=timeout)

        return client

    def execute_commands(self, commands):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """

        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                print(f"INPUT: {cmd} | OUTPUT: {line}")

            return response

    def bulk_upload(self, files):
        """
        Upload multiple files to a remote directory.

        :param files: List of paths to local files.
        :type files: List[str]
        """
        total_files = len(files)
        file_count = 0
        for f in files:
            self.upload_file(f)
            file_count += 1
            print(f"Uploaded {f}\n{total_files - file_count} to go...")
        print(
            f"Finished uploading {total_files} files to {self.remote_path} on {self.host}"
        )

    def upload_file(self, file):
        """Upload file to remote host"""

        self.scp.put(file, remote_path=self.remote_path)

    def download_file(self, file):
        """Download file from remote host."""

        self.scp.get(file)


if __name__ == "__main__":

    ssh_client = RemoteClient()
    response = ssh_client.execute_commands([f'cd {os.environ["KOR_PATH"]} && ls'])
    print(response)
