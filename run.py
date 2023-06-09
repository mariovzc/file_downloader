
import click
import logging
import requests
import os

from utils import HttpFormatter, uri_validator, timestamp

"""Setup Logs"""
formatter = HttpFormatter('{asctime} {levelname} {name} {message}', style='{')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.basicConfig(level=logging.DEBUG, handlers=[handler])



def check_download_folder(f):
    directory = "./downloads"
    if not os.path.exists(directory):
        # If it doesn't exist, create it
        click.echo("Create download folder")
        os.makedirs(directory)
    return f


@click.group()
def cli():
   pass


# EXAMPLE https://images.generated.photos/LfGoSVC95b6mmQWHYZLgO-T6WPSStPPoecILWi9Wnj4/rs:fit:512:512/wm:0.95:sowe:18:18:0.33/czM6Ly9pY29uczgu/Z3Bob3Rvcy1wcm9k/LnBob3Rvcy92M18w/NTkzMTQzLmpwZw.jpg
@click.command()
@click.argument('image_url', required=True)
@check_download_folder
def download_image(image_url):
   if not uri_validator(image_url):
      logging.error("Invalid image url")
      return
   response = requests.get(image_url)
   if response.status_code == 200:
        with open(f"./downloads/{timestamp()}.{response.url.split('.')[-1]}", "wb") as f:
            f.write(response.content)


cli.add_command(download_image)


def main():
   cli()
 
if __name__ == '__main__':
   main()