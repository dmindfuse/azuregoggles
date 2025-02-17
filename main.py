from cement import App, Controller, ex
from my_app.controllers import LoginController, ConfigController, BrowseController, SearchController

class MyApp(App):
    class Meta:
        label = 'azure_blob_browser'
        handlers = [LoginController, ConfigController, BrowseController, SearchController]

if __name__ == '__main__':
    with MyApp() as app:
        app.run()

