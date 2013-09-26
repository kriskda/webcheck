import urllib2, smtplib
import socket


class URLCheck(object):

    def __get_response(self, url):
        try:
            return urllib2.urlopen(url, timeout = 10)           
        except urllib2.URLError:
            return None
        except socket.timeout:
            return None

    def get_url_status(self, url):
        response = self.__get_response(url)

        if response == None:
            return "Offline"
        else:
            return str(response.getcode())
