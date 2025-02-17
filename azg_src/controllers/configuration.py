from cement import Controller, ex
import configparser

class ConfigController(BaseController):
    class Meta:
        label = 'config'
        stacked_on = 'base'
        stacked_type = 'nested'

    @ex(help='Configure storage')
    def config(self):
        storage_type = input('Enter storage type (azure/local): ')
        if storage_type not in ['azure', 'local']:
            print('Invalid storage type. Please enter "azure" or "local".')
            return
        account_name = input('Enter storage account name: ') if storage_type == 'azure' else ''
        container_name = input('Enter container name: ') if storage_type == 'azure' else ''

        config = configparser.ConfigParser()
        config['STORAGE'] = {
            'type': storage_type,
            'account_name': account_name,
            'container_name': container_name
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        
        print('Configuration saved.')
