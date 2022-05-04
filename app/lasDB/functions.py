from django.http import HttpResponse

# Simple Http output
def httpOutput(aOutput,mimetype='text/plain'):
	txtOutput = HttpResponse(aOutput)
	txtOutput['Content-Type'] = mimetype
	return txtOutput
