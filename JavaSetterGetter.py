import sublime, sublime_plugin

def getLastSelection(view):
    position = 0
    selected = []
    sels     = view.sel()
    for sel in sels:
        if sel.end() > position:
            position = sel.end()
            if '\n' in view.substr(sel):
                selected.extend(view.substr(sel).split('\n'))  
            else:
                selected.append(view.substr(sel))

    return [position, selected]

class JavaSetterGetterCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        selections = getLastSelection(self.view)
        sels = self.view.sel()
        selected_text = selections[1]
        properties = []
        insert_position = selections[0]
        output_arr = []


        for line in selected_text:
            line = line.strip();
            if len(line) > 0 and line[0] != '@':
                plain_line = line.split()
                if len(plain_line) != 3:
                    sublime.error_message("You probably have some syntax issues. Check your code.")
                    return

                properties.append( [plain_line[1], plain_line[2] ] )

        for prop in properties:
            property_name = prop[1].replace(';', '')
            capitalized_name = property_name[0].capitalize() + property_name[1:len(property_name)]

            template = """
    public void set{0}({1} {2}) {{
        this.{2} = {2};
    }}

    public {1} get{0}() {{
        return this.{2};
    }}"""

            output_arr.append(template.format(capitalized_name, prop[0], property_name))

        try:
            edit = self.view.begin_edit('java_setter_getter')
            insert_count = self.view.insert(edit, insert_position, '\n'.join(output_arr))
            final = getLastSelection(self.view)
            if insert_position == final[0]:
                final[0] = final[0] + insert_count

            self.view.sel().clear()
            self.view.sel().add(sublime.Region(insert_position, final[0]))
        finally:
            self.view.end_edit(edit)
