import sublime, sublime_plugin

def getSelections(view):
    position = 0
    selected = []
    sels     = view.sel()
    for sel in sels:
        if sel.end() > position:
            position = sel.end()
            line     = view.substr(sel)
            # Check for CRLF
            if "\r\n" in line:
                selected.extend(line.split("\r\n"))
            # Check for LF
            elif: "\n" in line:
                selected.extend(line.split("\n"))
            else:
                selected.append(line)

    return {"position": position, "selections": selected}

class JavaSetterGetterCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        selections = getSelections(self.view)
        selected_text = selections["position"]
        properties = []
        insert_position = selections["position"]
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
            #final = getLastSelection(self.view)
            #if insert_position == final[0]:
            #    final[0] = final[0] + insert_count

            # insert_count + insert_position = final[0] always. I had failed to see
            # that self.view.insert returned an int (I'm learning the API myself)
            # We can eliminate the second call of getLastSelection(self.view)
            # and just run the following:

            self.view.sel().clear()
            #self.view.sel().add(sublime.Region(insert_position, final[0]))
            self.view.sel().add(sublime.Region(insert_position, (insert_position + insert_count)))
        finally:
            self.view.end_edit(edit)
