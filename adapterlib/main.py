# -*- coding: utf-8 -*-
# Copyright (c) 2006-2010 Tampere University of Technology
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
AdapterMain contains functionality for parsing general command line options
and starting a test based on the given options.

Example main program for adapter:

from ExampleAdapter.testrunner import TestRunner
from adapterlib.main import AdapterMain
if __name__ == "__main__":
    
    am = AdapterMain()
    options, args = am.parseArguments()
    if options:
        testRunner = TestRunner(args,options.delay,options.record,"lastrun.log")
        am.runAdapter(testRunner,options)
"""

import sys
from optparse import OptionParser

class AdapterMain(object):

    def __init__(self):
    
        #Parse command line arguments
        parser = OptionParser(usage="%s [options] target\nUse -h for list of available options" % sys.argv[0])
        parser.add_option("-f", "--file", dest="filename",
                          help="read keywords from FILENAME")
        parser.add_option("-i", "--interactive", dest="interactive", 
                          action="store_true", default = False,
                          help="read keywords from command line")
        parser.add_option("-t", "--time", dest="delay", default = "0",
                          help ="Delay (in seconds) between consecutive keywords")
        parser.add_option("-a", "--address", dest="address",
                          help ="MBT server address")
        parser.add_option("-p", "--port", dest="port", 
                          help ="MBT server port")
        parser.add_option("--protocol", dest="protocol", 
                          help ="HTTP or HTTPS. If not given, socket is used")
        #parser.add_option("--passive", dest="passive", default = False, action="store_true",
        #                 help ="Use MBT server in a passive mode => "+
        #                 "Server will send a keyword when there is on to execute")
        parser.add_option("-u","--username", dest="username", 
                          help ="MBT server username")
        parser.add_option("--record", dest="record",action="store_true", default = False, help="Records the test to a file")
        
        self.parser = parser
        
        
    def parseArguments(self):
            
        #Argument parsing...
        (options, args) = self.parser.parse_args()
        if len(args) == 0:
            self.parser.error("incorrect number of arguments")
            return None
        else:
            if options.interactive or options.filename:
                pass
            elif options.address or options.port:
                if not options.address:
                    options.address = "localhost"
                if(options.port):
                    try:
                        options.port = int(options.port)
                        if options.port < 0 or options.port > 65535:
                            self.parser.error("Illegal port")
                            return None
                    except Exception:
                        self.parser.error("Illegal port")
                        return None
                else:
                    options.port = 9090
                if(options.protocol):
                    if not options.username:
                        self.parser.error("No username specified")
                if(options.username):
                    if not options.protocol:
                        self.parser.error("No protocol specified")                          
            else:
                self.parser.error("No mode specified")
                exit(1)
            if(options.delay):
                try:
                    options.delay = float(options.delay)
                    if options.delay < 0:
                        self.parser.error("Illegal delay")
                        return None
                except Exception:
                    self.parser.error("Illegal delay")
                    return None
        #Argument parsing ends...
        return options, args
    
    def runAdapter(self, testrunner, options):
        
        if not testrunner.initTest():
            return
        try:
            try:

                #Run interactive test   
                if options.interactive:
                    testrunner.runInteractive()

                #Run test from file
                elif(options.filename != None):
                    testrunner.runFromFile(options.filename)

                #Run test from server
                elif(options.address != None):
                    testrunner.runFromServer(options.address,options.port,options.username,options.protocol)

            except KeyboardInterrupt:
                pass

        finally:
            testrunner.endTest()
