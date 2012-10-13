import sublime, sublime_plugin, indentation

class JavaSetterGetterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("expand_selection", {"to": "line"}) 

       
        sels = self.view.sel()

        end_position = 0
        all_text = []
        properties = []

        for sel in sels:
            if sel.end > end_position:
                end_position = sel.end()
                all_text = self.view.substr(sel).split('\n')
                print all_text

        for line in all_text:
            if len(line) > 0:
                plain_line = line.split()
                if len(plain_line) != 3:
                    sublime.error_message("You probably have some syntax issues. Check your code.")
                    return
            



        #edit = self.view.begin_edit('java_setter_getter')
        #self.view.insert(edit, end_position, "\nSuck it!")

        #self.view.end_edit(edit)