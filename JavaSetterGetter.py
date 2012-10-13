import sublime, sublime_plugin

class JavaSetterGetterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("expand_selection", {"to": "line"}) 

        sels = self.view.sel()
        selected_text = []
        properties = []
        end_position = 0
        output_arr = []

        for sel in sels: 
            if sel.end > end_position:
                end_position = sel.end()
                selected_text = self.view.substr(sel).split('\n')

        for line in selected_text:
            if len(line) > 0:
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
            self.view.insert(edit, end_position, '\n'.join(output_arr))            
        finally:
            self.view.end_edit(edit)   
