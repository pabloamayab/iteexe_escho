from twisted.web.resource import Resource
import gettext
import os

def nothing(str):
    return str
_=nothing

# A Page is a collection of Blocks
class Block:
    Edit, View = (1,2)
    def __init__(self, myId):
        self.mode     = Block.Edit
        self.id       = myId
        self.title    = ""
        self.content  = ""

    def render(self):
        if self.mode == Block.Edit:
            return self.renderEdit()
        else:
            return self.renderView()

    def renderEdit(self):
        html  = "<div>\n"
        html += "<input type=\"text\" size=\"51\""
        html += "name=\"title%d\" " % self.id
        html += " value=\"%s\"/><br/>\n" % self.title
        html += "<textarea cols=\"50\" rows=\"12\" "
        html += "name=\"content%d\">\n" % self.id
        html += self.content
        html += "</textarea>\n"
        html += "<input type=\"submit\" name=\"done%d\"" % self.id
        html += " value=\"%s\"/>\n" % _("Done")
        html += "<input type=\"submit\" name=\"del%d\"" % self.id
        html += " value=\"%s\"/>\n" % _("Delete")
        html += "<div>\n"
        return html

    def renderView(self):
        html  = "<div>\n"
        html += "<b>" + self.title + "</b><br/>\n"
        html += self.content
        html += "<input type=\"submit\" name=\"edit%d\" " % self.id
        html += " value=\"%s\"/>\n" % _("Edit")
        html += "<div>\n"
        return html
class Page(Resource):

    gettext.textdomain('')
    gettext.bindtextdomain('', '')
    
    
    def __init__(self):
        Resource.__init__(self)
        self.blocks = {}
        self.nextId = 1

    def render_GET(self, request):
                  
        # Process args
        enStr=""
        frStr=""
        geStr=""
        chStr=""
        for arg in request.args:                    
            if arg == "add":
                blockId = self.nextId
                self.nextId += 1
                self.blocks[blockId] = Block(blockId)

            elif arg.startswith("del"):
                blockId = int(arg[3:])
                del self.blocks[blockId]

            elif arg.startswith("edit"):
                blockId = int(arg[4:])
                self.blocks[blockId].mode = Block.Edit

            elif arg.startswith("done"):
                blockId = int(arg[4:])
                self.blocks[blockId].mode = Block.View
                
            elif arg == "language":
                if request.args["language"][0]=="English":
                    enStr="selected"     
                    
                elif request.args["language"][0]=='French':
                    trans=gettext.GNUTranslations(open("po/fr.mo"))
                    frStr="selected"
                    
                elif request.args["language"][0]=='German':
                    trans=gettext.GNUTranslations(open("po/ge.mo"))
                    geStr="selected"
                    
                elif request.args["language"][0]=='Chinese':
                    trans=gettext.GNUTranslations(open("po/ch.mo"))
                    chStr="selected"
                global _            
                _=trans.gettext
                #break

        # Rendering
        html  = "<html><head><title>eXe: little packaging test</title>\n"
        html += """<meta http-equiv="content-type" content="text/html; charset=UTF-8">\n""";
        html += "</head>\n"
        html += "<body>\n"
        html += "<form method=\"post\" action=\"%s\"" % request.path
        html += " name=\"contentForm\">\n"
        html += """<select onchange="submit()" name="language">            
            <option value="English" %s>English</option>    
            <option value="French" %s >French</option>
            <option value="German" %s >German</option>
            <option value="Chinese" %s >Chinese</option>
            </select> Please select a language <br/>""" %(enStr,frStr,geStr,chStr) 
        html += "<input type=\"submit\" name=\"add\" value=\"%s\"/>\n" % _("Add")
                        
        #html += "<pre>%s</pre>\n" % str(request.args)

        for block in self.blocks.itervalues():
            if "content%d"%block.id in request.args:
                block.title   = request.args["title%d"%block.id][0]
                block.content = request.args["content%d"%block.id][0]

            html += block.render()

        html += "</form>\n"
        html += "</body></html>\n"
        return html
    
    render_POST = render_GET
