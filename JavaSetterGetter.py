import sublime, sublime_plugin

class JavaSetterGetterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("expand_selection", {"to": "line"}) 

        edit = self.view.begin_edit('java_setter_getter')
        sels = self.view.sel()

        end_position = 0
        all_text = []

        for sel in sels:
            if sel.end > end_position:
                end_position = sel.end()
                all_text.append(self.view.substr(sel))

        print all_text

        self.view.insert(edit, end_position, "\nSuck it!")

        self.view.end_edit(edit)