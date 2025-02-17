from cement import Controller, ex

class LoginController(BaseController):
    class Meta:
        label = 'login'
        stacked_on = 'base'
        stacked_type = 'nested'

    @ex(help='Login to Azure')
    def login(self):
        import subprocess
        import re
        
        result = subprocess.run(['az', 'login', '--use-device-code'], capture_output=True, text=True)
        output = result.stdout
        
        url_match = re.search(r'(https://microsoft.com/devicelogin)', output)
        code_match = re.search(r'(\w{9})', output)
        
        if url_match and code_match:
            print(f'Visit {url_match.group(1)} and enter the code: {code_match.group(1)}')

        # Return to main menu
        self.app.run()
