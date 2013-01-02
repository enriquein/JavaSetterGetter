import sublime, sublime_plugin
import re

DEBUG = False

java_field_pat = "(?P<indent>\s*)" + \
                 "(?P<access>protected|private)" + \
                 "(?: (?P<transient>transient|volatile))?" + \
                 "(?: (?P<static>static))?" + \
                 "(?: (?P<final>final))?" + \
                 "(?: (?P<type>[a-zA-Z0-9_$]+))" + \
                 "(?: (?P<varname>[a-zA-Z0-9_$]+))" + \
                 "(?:\s*=.+)?;"

java_field_pat = re.compile(java_field_pat)

def matchdict(text):
    m = java_field_pat.match(text)
    if m:
        return m.groupdict()
    else:
        return {}

def getSelections(view):
    position = 0
    selected = []
    sels     = view.sel()

    for sel in sels:
        lineRegions = view.lines(sel)
        for lineRegion in lineRegions:
            position = max(position, lineRegion.end())
            selected.extend(view.substr(lineRegion).split("\n"))

    selection_matches = []
    for line in selected:
        md = matchdict(line)
        if DEBUG:
            print line, md
        if md.get("access", None) is not None: # Make sure it's private or protected
            if md.get("static", None) is None: # Make sure it's not static
                if md.get("final", None) is None: # Make sure it's not final
                    selection_matches.append(md)
    return {"position": position, "selections": selection_matches}

class JavaSetterGetterCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        selections = getSelections(self.view)
        selection_matches = selections["selections"]
        properties = []
        insert_position = selections["position"]

        getter_arr = []
        setter_arr = []

        getterTemplate = """
{3}public {1} get{0}() {{
{3}    return this.{2};
{3}}}"""

        setterTemplate = """
{3}public void set{0}({1} {2}) {{
{3}    this.{2} = {2};
{3}}}"""

        for prop in selection_matches:
            property_name = prop['varname']
            capitalized_name = property_name[0].capitalize() + property_name[1:len(property_name)]

            getter_arr.append(getterTemplate.format(capitalized_name, prop['type'], prop['varname'], prop['indent']))
            setter_arr.append(setterTemplate.format(capitalized_name, prop['type'], prop['varname'], prop['indent']))

        try:
            edit = self.view.begin_edit('java_setter_getter')
            properties_text = "\n" + "\n".join(getter_arr) + "\n" + "\n".join(setter_arr)
            insert_count = self.view.insert(edit, insert_position, properties_text)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(insert_position, (insert_position + insert_count)))
        except Exception, ex:
            if DEBUG:
                print ex
        finally:
            self.view.end_edit(edit)
