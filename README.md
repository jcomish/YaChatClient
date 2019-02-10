#YaChat Client

#####Warning: I heard that the front-end technology I am using has some compatibility issues with Windows. I developed this in MacOS, but there shouldn't be a problem in Linux.
         
###Run Instructions:

  - While inside the YaChat directory, run
  
  
    pip install -r requirements.txt
    
  - Navigate to the "services" directory and run 
  
  
    python main.py
 
Once you follow the above two steps a standalone application should appear.
From here, you can click settings and enter your server information. It is prepopulated with likely values
Everything else is pretty straigtforward from there.

###Notes
Since any technologies were available to us, I decided to make this look snazzy with a web framework. I used
Flask to do this. I simply downloaded a template for the overwhelming majority of the UI componets. Credit for 
this is given to Emil Carlsson. This can be found here: https://bootsnipp.com/snippets/exR5v

I used a web tool that hooks in with web frameworks called "pywebview". This is the problem library that may or may
not work with windows. All it does is wrap your web browser in a window to make it look and feel like a standalone app.

There were a few snippets of code that I pulled from the web to help me with my front end. Namely:
  - Code to implement Modals since Bootstrap was not working for some reason 
  - Code to generate avatars with the first letter of the names of people. This was written by Artur Heinze and can be
    found here: https://gist.github.com/leecrossley/6027780
    
In regards to the technologies that I used: standard front-end technologies; namely: JavaScript, AJAX, jQuery, 
and Web Sockets. It is important to note that I have all of my networking code inside the services directory, and it is 
compliant with the protocol. My testing showed that it was interoperable with the provided clients and server.

I have a listener thread that is running in parallel with the runner/web server. I figure that I don't need any 
more than one thread with the expected traffic.
  
### If you have any questions, please reach out to jcomish@utexas.edu