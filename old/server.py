from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>Hello World!"
				output += "<form method=POST enctype='multipart/form-data' action='/hello'><h2>What do you want me to say</h2><input name='message' type='text'><input type='submit' value='submit'> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/home"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += """	<html><body><h1>home</h1> <br /> <a href='/signup'>Signup</a></body></html>"""
				self.wfile.write(output)
				print output
				return

                        if self.path.endswith("/signup"):
                                self.send_response(200)
                                self.send_header('Content-type', 'text/html')
                                self.end_headers()
                                output = ""
                                output += """   <html><body><h1>Create New Account</h1><form method=POST enctype='multimart/form-data' action='/signup'> First Name:<br /> <input name='message' type='text'> <br /> Email Address: <br /> <input name='message' type='text'>
<br /><input type='submit' value='sumbit'></form><form method=GET action='/home'><input type='submit' value='cancel'></form></body></html>"""
                                self.wfile.write(output)
                                print output
                                return


		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
#		try:
			self.send_response(301)
			self.end_headers()
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				print "ctpe check here"
				fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
			output = ""
			output += "<html><body>"
			output += "<h2> Okay how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]
			output += "<form method=POST enctype='multipart/form-data' action='/hello'><h2>What do you want me to say</h2><input name='message' type='text'><input type='submit' value='submit'> </form>"
			output += "</body></html>"
			self.wfile.write(output)
			print(output)
			

#		except:
#			print "Someting wong"
def main():
	try:
		port = 80
		server = HTTPServer(('',port), webserverHandler)
		print "Web server is running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()
