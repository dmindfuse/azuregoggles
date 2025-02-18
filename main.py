from cement import App, Controller, ex
from azg_src.controllers import LoginController, ConfigController, BrowseController, SearchController

class MyApp(App):
    class Meta:
        label = 'azure_blob_browser'
        handlers = [LoginController, ConfigController, BrowseController, SearchController]

if __name__ == '__main__':
    with MyApp() as app:
        app.run()

