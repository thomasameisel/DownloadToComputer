import json
import hashlib
import base64
import subprocess
import os, sys
import time
import urllib
import os.path
import glib
import requests
from urlparse import urlparse
from lxml import html

from pushbullet import PushBullet, Listener

class Downloader(object):

    def __init__(self, auth_key, device_name, last_push = time.time(), device_iden=None):
        self._auth_key = auth_key
        self.pb = PushBullet(self._auth_key)
        self.listener = Listener(self.pb, self.download_link)

        self.last_push = last_push

        self.device = None
        if device_iden:
            results = [d for d in self.pb.devices if d.device_iden == device_iden and d.active]
            self.device = results[0] if results else None

        if not self.device:
            try:
                device = self.pb.new_device(device_name)
                print("Created new device:",device_name,"iden:",device.device_iden)
                self.device = device
            except:
                print("Error: Unable to create device")
                raise

    def get_unique_filename(self, filename, downloads_dir):
        unique_filename = filename
        i = 0
        while os.path.isfile(downloads_dir+"/"+unique_filename):
            i+=1
            unique_filename=filename+" (%i)" % i
        return unique_filename

    def get_filename_from_url(self, url):
        if url.rfind('/') != -1:
            title = url[url.rfind('/')+1:]
        if len(title) < 1:
            try:
                response = requests.get(url)
                parsed_body = html.fromstring(response.text)
                titles = parsed_body.xpath('//title/text()')
                if len(titleArray) == 0:
                    title="tmptitle"
                else:
                    title=titles[0]
            except:
                title="tmptitle"
        return title

    def download_link(self, push):
        pushes = self.pb.get_pushes(self.last_push)[1]
        if (len(pushes) != 0):
            last_push = pushes[len(pushes)-2]
            if last_push.get("url"):
                url = last_push.get("url")
                filename = self.get_filename_from_url(url)

                downloads_dir = glib.get_user_special_dir(glib.USER_DIRECTORY_DOWNLOAD)
                unique_filename = self.get_unique_filename(filename, downloads_dir)
                unique_filename_full_path = downloads_dir+"/"+unique_filename

                urllib.urlretrieve (url, unique_filename_full_path)
                print "URL: %s Downloaded: %s" % (url, unique_filename_full_path)
            self.last_push = max(self.last_push, last_push.get("created"))

    def run(self):
        try:
            self.listener.run_forever()
        except KeyboardInterrupt:
            self.listener.close()

    def dump_config(self, path):
        config = {"auth_key": self._auth_key,
                  "device_name": self.device.nickname,
                  "device_iden": self.device.device_iden}
        with open(path, "w") as conf:
            json.dump(config, conf)

def main():
    config_file = sys.argv[1]
    with open(config_file) as conf:
        config = json.load(conf)

    m = Downloader(**config)
    m.run()
    m.dump_config(config_file)


if __name__ == '__main__':
    main()
