#!/usr/bin/python

import webapp

def extractBody(request, method):
    if (method == "POST"):
        body = request.split()[-1]
    elif (method == "GET"):
        body = ""
    return body


def extractUrl(body):
    url = body.split("=")[1]
    if len(url.split("%3A%2F%2F")) == 1:
		if url != "":
			url = "http://" + url
    else:
        url = url.replace("%3A%2F%2F", "://")
    print "***URL***" + url + "***"
    return url


def createForm():
	form = "<html><body>" 
	form += '<body style="background:#5C0349">'
	form += '<span style="color:#FCF8FA">'
	form += '<form action=""method="POST">'
	form += "<h1>ACORTADOR DE URLS<h1><br>"
	form += '<h4>Introduce una Url para acortar -> <input type="text" name="url"</h4>'
	form += '<input type="submit">'
	form += '</form>'
	form += "</body></html>"
	return form


def createLink(string):
    link = '<table border="2px" style="background:#B294AC">'
    link += "<tr>"
    link += "<td>" + string + "</td>"
    link += "</tr>"
    link += "</table>"
    return link
    
    
def createTable(list1, list2):
	table = '<table border="5px" style="background:#B294AC">'
	table += "<tr>"
	table += "<td>URL ORIGINAL</td>"
	table += "<td>URL ACORTADA</td>"
	table += "</tr>"
	table += "<tr>"
	table += "<td>" + list1 + "</td>"
	table += "<td>" + list2 + "</td>"
	table += "</tr>"
	table += "</table>"
	return table
	

def createErrorMsg(msg):
	link = createLink("VOLVER AL ACORTADOR DE URLS")
	error = "<html><body><h2>ERROR: " + msg + "</h2>"
	error += "<a + href='http://localhost:1234'>" + link + "</a><br><br>"
	error += "</body></html>"	
	return error
	
	
class p1 (webapp.webApp):

    diccUrl = {}
    diccShortedUrl = {}
    numUrls = 0
    
    listUrl = ""
    listShortedUrl = ""
    
    def parse(self, request):
		method = request.split()[0]
		attribute = request.split()[1][1:]
		body = extractBody(request, method)
		return (method, attribute, body)

    def process(self, parsedRequest):
		if not parsedRequest:
			return("400 Bad Request", "<html><body><h1>ERROR</h1></body></html>")
		(method, attribute, body) = parsedRequest
		if method == "GET":
			if attribute == "":
				form = createForm()
				httpCode = "200 OK!"
				htmlBody = form
				if (self.numUrls > 0):
					table = createTable(self.listUrl, self.listShortedUrl)
					htmlBody += ("<html><body><h3>Lista de urls:</h3>" + table + "</body></html>")
			else:
				urlShortedKey = int(attribute)
				if urlShortedKey in self.diccShortedUrl.keys():
					url = self.diccShortedUrl[urlShortedKey]
					httpCode = "307 REDIRECT"
					htmlBody = "<html><head><meta http-equiv=Refresh content= 0;url=" + url + "></head></body></html>"
				else:
					httpCode = "400 Resource not available"
					htmlBody = createErrorMsg("No existe la Url introducida");
					return (httpCode,  htmlBody)

		elif method == "POST":
			url = extractUrl(body)
			if url is "":
				httpCode = "400 Resource not available"
				htmlBody = createErrorMsg("Introduce una Url");
				return (httpCode,  htmlBody)
				
			if url not in self.diccUrl.keys():
				self.diccShortedUrl[self.numUrls] = url
				self.diccUrl[url] = self.numUrls
				self.listUrl += "<p>" + str(url) + "</p>"
				self.listShortedUrl += "<p>http://localhost:1234/" + str(self.numUrls) + "</p>"
				self.numUrls = self.numUrls + 1

			urlShorted = "http://localhost:1234/" + str(self.numUrls - 1)
			link = createLink("VOLVER")
			linkUrl = createLink(str(url))
			linkShortedUrl = createLink(str(urlShorted))
			clickable = '<p><h4><a style="color:#FCF8FA"' + "href='" + url + "'>Url" + linkUrl + "</a></h4></p>"
			clickable += '<p><h4><a style="color:#FCF8FA"' + "href='" + url + "'>Url acortada" + linkShortedUrl + "</a></h4></p>"
			clickable += "<p><a href='http://localhost:1234/'>" + link + "</a></p>"
			httpCode = "200 OK!"
			htmlBody = '<html><body style="background:#5C0349">' + clickable + "</body></html>"

		return (httpCode, htmlBody)

if __name__ == "__main__":
	testWebApp = p1("localhost", 1234)
