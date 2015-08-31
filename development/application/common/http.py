#!/usr/bin/env python
# coding: utf-8
"""
HTTP-Helfer
"""

import os
import urllib
import urllib2
import urlparse
import base64
import socket
import cherrypy
import cherrypy.lib.httputil


def request(
    url,
    webuser = None,
    webpass = None,
    data = None,
    raw_data = None,
    headers = None,
    return_response_obj = None,
    timeout = socket.getdefaulttimeout()
):
    """
    Datei aus dem Internet herunterladen (POST oder GET Request)

    Wird *webuser* angegeben, dann wird der Benutzer mit "BASE-Authorization"
    übermittelt.

    Wird *data* übergegeben, dann wird ein POST-Request gestartet. Die Daten
    werden mit *urlencode* codiert.

    Wird *data* NICHT übergeben, dann wird ein GET-Request gestartet.

    :param raw_data: Wenn übergeben, dann wird *data* ignoriert und dieser
        Bytestring ohne umwandlung übergeben

    :param headers: Erwartet ein Dictionary mit Name-Value-Paaren, die zusätzlich
        als Header beim Request übergeben werden.

    :param return_response_obj: Wenn `True`, dann wird nicht das Ergebnis als
        String, sondern das komplette Respone-Objekt zurück gegeben
    """

    if raw_data:
        data = raw_data
    elif data:
        data = urllib.urlencode(data)

    if not headers:
        headers = {}

    request_ = urllib2.Request(url, data, headers = headers)

    if webuser:
        base64string = base64.encodestring('%s:%s' % (webuser, webpass))[:-1]
        request_.add_header("Authorization", "Basic %s" % base64string)

    response= urllib2.urlopen(request_, timeout = timeout)
    if return_response_obj:
        return response
    else:
        response_data = response.read()
        response.close()
        return response_data


def check_only_post_allowed():
    """
    Prüft ob der Request ein POST-Request ist. 
    
    GET-Requests sind nur für 'localhost' erlaubt.
    """
    
    if not "localhost" in cherrypy.request.base:
        if cherrypy.request.method != "POST":
            raise cherrypy.HTTPError(
                message = "If not 'localhost': Only POST-requests allowed."
            )


def get_client_ip():
    """
    Gibt die IP-Adresse des Clients oder dessen Router zurück
    """
    
    client_ip = cherrypy.request.headers.get("X-FORWARDED-FOR")
    if not client_ip:
        if cherrypy.request.remote:
            client_ip = cherrypy.request.remote.ip

    # Gefakte IP-Adresse für den Testcomputer
    if client_ip and client_ip.startswith("10."):
        client_ip = "62.46.201.29"

    return client_ip


def set_content_type_text():
    """
    Setzt den Content-Type des Response auf "text/plain"
    """

    cherrypy.response.headers["Content-Type"] = "text/plain; charset=utf-8"

    
def set_content_type_json():
    """
    Setzt den Content-Type des Response auf "application/json"

    Nicht mehr "text/x-json".
    """

    cherrypy.response.headers["Content-Type"] = "application/json; charset=utf-8"


def set_content_type_xml():
    """
    Setzt den Content-Type des Response auf "text/xml"
    """

    cherrypy.response.headers["Content-Type"] = "text/xml; charset=utf-8"


def set_content_type_rss():
    """
    Setzt den Content-Type des Response auf "application/rss+xml"
    """

    cherrypy.response.headers["Content-Type"] = "application/rss+xml; charset=utf-8"


def set_content_type_image(imageformat):
    """
    Setzt den Content-Type des Response auf "image/<imageformat>"
    """
    
    cherrypy.response.headers["Content-Type"] = "image/%s" % imageformat


def set_content_type_download(filename):
    """
    Setzt den Content-Type des Response auf "application/x-download"
    """

    cherrypy.response.headers["Content-Type"] = "application/x-download"
    if filename:
        cherrypy.response.headers["Content-Disposition"] = 'attachment; filename="%s"' % filename
    else:
        cherrypy.response.headers["Content-Disposition"] = 'attachment'


def set_no_cache():
    """
    Setzt die Header-Einträge so, dass die Proxies und Browser aufgefordert
    werden, die Seite nicht zu speichern.
    """
    
    cherrypy.response.headers["Cache-Control"] = "no-cache"
    cherrypy.response.headers["Pragma"] = "no-cache"


class Url(object):
    """
    Repräsentiert eine URL, wie sie im Onlineshop üblich ist.
    """
    
    __slots__ = [
        "scheme",
        "netloc",
        "path",
        "query",
        "fragment",
    ]
    
    
    def __init__(
        self, 
        url = None, # URL 
        scheme = None, # "http" oder "https"
        netloc = None, # z.B. devshop.skischoolshop.com
        path = None, # z.B. "/" oder "groupcourses"
        query = None, # 
        fragment = None
    ):
        """
        Info: ``<scheme>://<netloc>/<path>?<query>#<fragment>``
        
        :param scheme: "http" oder "https"
        :param netloc: z.B. "devshop.skischoolshop.com"
        :param path: z.B. "/" oder "groupcourses". Es kann aber auch ein
            itterierbares Objekt mit Strings übergeben werden. Der Pfad
            wird dann zusammengesetzt.
        :param query: Dictionary mit den Query-Key-Value-Paaren oder ein
            String. Ein String wird automatisch in ein Dictionary umgewandelt.
        :param fragment: Dictionary mit den Hash-Key-Value-Paaren oder ein
            String. Ein String wird automatisch in ein Dictionary umgewandelt.
        """
        
        # Falls die URL übergeben wurde...
        if url:
            (
                parsed_scheme,
                parsed_netloc,
                parsed_path,
                parsed_query,
                parsed_fragment
            ) = urlparse.urlsplit(url)
            if scheme is None:
                scheme = parsed_scheme
            if netloc is None:
                netloc = parsed_netloc
            if path is None:
                path = parsed_path
            if query is None:
                query = parsed_query
            if fragment is None:
                fragment = parsed_fragment
        
        # Scheme
        if isinstance(scheme, basestring):
            self.scheme = scheme.strip(":/")
        else:
            self.scheme = None
        
        # Netloc
        if isinstance(netloc, basestring):
            self.netloc = netloc.strip("/")
        else:
            self.netloc = None
        
        # Path
        if isinstance(path, basestring):
            self.path = path
        else:
            try:
                self.path = "/".join(path)
            except TypeError:    
                self.path = None
        
        # Query
        if isinstance(query, basestring):
            if isinstance(query, unicode):
                query = query.encode("utf-8")
            self.query = cherrypy.lib.httputil.parse_query_string(query.strip(u"?&"))
        else:
            self.query = query or {}
        
        # Fragment
        if isinstance(fragment, basestring):
            if isinstance(fragment, unicode):
                fragment = fragment.encode("utf-8")
            self.fragment = cherrypy.lib.httputil.parse_query_string(fragment.strip("?&"))
        else:
            self.fragment = fragment or {}
    
    
    def __str__(self):
        """
        Gibt die URL als String zurück
        """
        
        if self.netloc:
            scheme = self.scheme or "http"
        else:
            scheme = None
        
        if isinstance(self.path, basestring):
            path = self.path
        else:
            try:
                path = "/".join(self.path) or "/"
            except TypeError:    
                path = "/"
        
        if self.query:
            query = {}
            for key, value in self.query.items():
                if isinstance(key, unicode):
                    key = key.encode("utf-8")
                if isinstance(value, unicode):
                    value = value.encode("utf-8")
                query[key] = value
            query_str = urllib.urlencode(query)
        else:
            query_str = None
        
        if self.fragment:
            fragment = {}
            for key, value in self.fragment.items():
                if isinstance(key, unicode):
                    key = key.encode("utf-8")
                if isinstance(value, unicode):
                    value = value.encode("utf-8")
                fragment[key] = value
            fragment_str = urllib.urlencode(fragment)
        else:
            fragment_str = None
        
        return urlparse.urlunsplit((
            scheme,
            self.netloc,
            path,
            query_str,
            fragment_str
        ))
    
    
    __repr__ = __str__
    

def get_current_url():
    """
    Gibt die URL des aktuellen cherrypy-Requests zurück.
    """
    
    request = cherrypy.request
    url = urllib.basejoin(request.base, request.path_info)
    if request.query_string:
        url += "?" + request.query_string
    return unicode(url)


def get_portal_url():
    """
    Gibt die URL des Portales zurück
    """

    return unicode(urllib.basejoin(cherrypy.request.base, u"/"))

    
def is_productive_system():
    """
    Prüft ob das Programm auf einem Testcomputer läuft oder auf dem Produktivsystem.

    :return: `True`, wenn Produktivsystem. `False`, wenn Test- oder Entwicklungscomputer.
    """

    return not os.environ.get('SERVER_SOFTWARE', '').startswith('Development')


