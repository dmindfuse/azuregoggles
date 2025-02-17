from cement import Controller, ex
import subprocess
import configparser
import os
import re
import json

class SearchController(Controller):
    class Meta:
        label = 'search'
        stacked_on = 'base'
        stacked_type = 'nested'

    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.storage_type = config['STORAGE']['type']
        self.account_name = config['STORAGE']['account_name']
        self.container_name = config['STORAGE']['container_name']

    @ex(help='Search storage')
    def search(self):
        self.read_config()

        pattern = input('Enter regex pattern to filter (ESC to cancel): ')
        if pattern.lower() == 'esc':
            print('Search cancelled.')
            self.app.run()

        if self.storage_type == 'azure':
            self.search_azure(pattern)
        elif self.storage_type == 'local':
            self.search_local(pattern)
        else:
            print('Invalid storage type.')

    def search_azure(self, pattern):
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
            filtered_blobs = self.filter_blobs(blobs, pattern)
            self.display_blobs(filtered_blobs)

            choice = input('Enter row number, or "q" to quit, "c" to configure: ')
            if choice == 'q':
                break
            elif choice == 'c':
                self.app.args.parse(['config'])
                self.app.run()
            elif choice.isdigit() and int(choice) in filtered_blobs
