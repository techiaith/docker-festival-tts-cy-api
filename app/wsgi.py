import os
import cherrypy
import festival


from tools import de_accent
from cherrypy.lib.static import serve_file


class Stream(object):

    def __init__(self):
        festival.execCommand("(voice_cb_cy_llg_diphone)")
     
    @cherrypy.expose
    def index(self, name=''):
        if len(name)==0:
            name='index.html'
        return serve_file(os.path.join(static_dir, name))
    	
    @cherrypy.expose
    def speak(self, text, stretch=1.2, format='mp3', pitch=5, **kwargs):
        
        try:
            format = format.lower()
            
            if format not in ('mp3', 'wav'):
                raise ValueError("'format' must be either 'mp3' or 'wav")
            
            try:
                pitch = float(pitch)
                if not (1 <= pitch <= 9):
                    raise ValueError
            except ValueError:
                raise ValueError("'pitch' must be between 1 and 9")
        except ValueError as e:
            return "ERROR: %s" % str(e)

        is_mp3 = (format.lower() == 'mp3')
        festival.setStretchFactor(stretch)
        
        # set the pitch
        # quadratic eqn. Values taken from int_simple_params
        # pitch = 5, f0_mean = 130
        # pitch = 1, f0_mean = 70
        # pitch = 9, f0_mean = 400
        # y = 5.9375x^2 - 20.625x + 84.6875
        pitch = (5.9375*(pitch*pitch) - 20.625*pitch + 84.6875) if pitch != 5 else 130
        festival.execCommand("(set! int_simple_params '((f0_mean %s) (f0_std 10)))" % pitch)
        
        text_de_accented = de_accent(text)
        tmpfile = festival.textToMp3(text_de_accented) if is_mp3 else festival.textToWav(text_de_accented)
        
        cherrypy.response.headers["Content-Type"] = "audio/%s" % ('mpeg' if is_mp3 else 'wav')
        return tmpfile.read()

static_dir = "/festival/static"

cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.error_file': '/var/log/festival/festivalapi.error.log',
})

conf = {
        '/': {  # Root folder.
            'tools.staticdir.on':   True,  # Enable or disable this rule.
            'tools.staticdir.root': static_dir,
            'tools.staticdir.dir':  '',
         }
       }
    
cherrypy.tree.mount(Stream(), '/', config=conf)
application = cherrypy.tree

