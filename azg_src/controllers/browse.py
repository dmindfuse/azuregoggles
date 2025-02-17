from cement import Controller, ex
import subprocess
import configparser
import os
import json

class BrowseController(BaseController):
    class Meta:
        label = 'browse'
        stacked_on = 'base'
        stacked_type = 'nested'

    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.storage_type = config['STORAGE']['type']
        self.account_name = config['STORAGE']['account_name']
        self.container_name = config['STORAGE']['container_name']

    @ex(help='Browse storage')
    def browse(self):
        self.read_config()

        if self.storage_type == 'azure':
            self.browse_azure()
        elif self.storage_type == 'local':
            self.browse_local()
        else:
            print('Invalid storage type.')

    def browse_azure(self):
        def list_blobs(path='/'):
            result = subprocess.run(
                ['az', 'storage', 'blob', 'list',
                '--account-name', self.account_name,
                '--container-name', self.container_name,
                '--prefix', path,
                '--output', 'json'],
                capture_output=True, text=True
            )
            return result.stdout

        current_path = '/'
        while True:
            output = list_blobs(current_path)
            blobs = self.parse_blobs(output)
            self.display_blobs(blobs)

            choice = input('Enter row number, or "q" to quit, "c" to configure, "s" to search: ')
            if choice == 'q':
                break
            elif choice == 'c':
                self.app.args.parse(['config'])
                self.app.run()
            elif choice == 's':
                self.app.args.parse(['search'])
                self.app.run()
            elif choice.isdigit() and int(choice) in blobs:
                selected_blob = blobs[int(choice)]
                if selected_blob['is_dir']:
                    current_path = selected_blob['name']
                else:
                    download = input('Download file? (yes/no): ')
                    if download.lower() == 'yes':
                        target_path = input('Enter target path: ')
                        self.download_blob(selected_blob['name'], target_path)
            else:
                print('Invalid choice.')

    def browse_local(self):
        def list_files(path='/'):
            try:
                files = os.listdir(path)
                files_info = []
                for file in files:
                    file_path = os.path.join(path, file)
                    if os.path.isdir(file_path):
                        size = '<DIR>'
                    else:
                        size = os.path.getsize(file_path)
                    modified_time = os.path.getmtime(file_path)
                    files_info.append({
                        'name': file,
                        'is_dir': os.path.isdir(file_path),
                        'last_modified': modified_time,
                        'size': size
                    })
                return files_info
            except Exception as e:
                print(f"Error: {e}")
                return []

        current_path = '/'
        while True:
            files = list_files(current_path)
            self.display_files(files)

            choice = input('Enter row number, or "q" to quit, "c" to configure, "s" to search: ')
            if choice == 'q':
                break
            elif choice == 'c':
                self.app.args.parse(['config'])
                self.app.run()
            elif choice == 's':
                self.app.args.parse(['search'])
                self.app.run()
            elif choice.isdigit() and int(choice) in range(len(files)):
                selected_file = files[int(choice)]
                if selected_file['is_dir']:
                    current_path = os.path.join(current_path, selected_file['name'])
                else:
                    download = input('Download file? (yes/no): ')
                    if download.lower() == 'yes':
                        target_path = input('Enter target path: ')
                        self.download_file(os.path.join(current_path, selected_file['name']), target_path)
            else:
                print('Invalid choice.')

    def parse_blobs(self, output):
        blobs = json.loads(output)
        parsed = {}
        for i, blob in enumerate(blobs):
            parsed[i] = {
                'name': blob['name'],
                'is_dir': blob.get('properties', {}).get('is_directory', False),
                'last_modified': blob['properties']['lastModified'],
                'size': blob['properties']['contentLength']
            }
        return parsed

    def display_blobs(self, blobs):
        print('Available blobs:')
        print(f'{"ID":<5} {"Name":<50} {"Last Modified":<30} {"Size (bytes)":<15}')
        print('-' * 100)
        for key, blob in blobs.items():
            last_modified = blob['last_modified']
            size = blob['size']
            print(f'{key:<5} {blob["name"]:<50} {last_modified:<30} {size:<15}')

    def display_files(self, files):
        print('Available files:')
        print(f'{"ID":<5} {"Name":<50} {"Last Modified":<30} {"Size (bytes)":<15}')
        print('-' * 100)
        for i, file in enumerate(files):
            last_modified = file['last_modified']
            size = file['size']
            print(f'{i:<5} {file["name"]:<50} {last_modified:<30} {size:<15}')

    def download_blob(self, blob_name, target_path):
        subprocess.run(
            ['az', 'storage', 'blob', 'download',
            '--account-name', self.account_name,
            '--container-name', self.container_name,
            '--name', blob_name,
            '--file', target_path]
        )
        print(f'{blob_name} downloaded to {target_path}')

    def download_file(self, source_path, target_path):
        try:
            import shutil
            shutil.copy(source_path, target_path)
            print(f'{source_path} downloaded to {target_path}')
        except Exception as e:
            print(f"Error: {e}")
