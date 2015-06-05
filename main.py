# 1. Save settings in *.sublime-settings
# 2. Load settings and convert to *.sublime-commands
# 3. Invoke commands with InsertSymbol with args.

import os
import json
import sublime, sublime_plugin


class InsertSymbolCommand(sublime_plugin.TextCommand):
	def run(self, edit, text = ""):
		view = self.view
		view.insert(edit, view.sel()[0].a, text)


def get_settings():
	#print("update 'LatexSymbols.sublime-commands'")
	commandFilePath = os.path.join(sublime.packages_path(), 'User', 'LatexSymbols.sublime-commands')
	setting = sublime.load_settings('LatexSymbols.sublime-settings')
	sym_list = setting.get('symbol_list', [])
	cmd_list = _parseSettings(sym_list, 'LatexSymbols: ')
	#print("write to " + commandFilePath)
	f = open(commandFilePath, 'w')
	f.write(_toSublimeCommands(cmd_list))
	f.close()

def plugin_loaded():
	setting = sublime.load_settings('LatexSymbols.sublime-settings')
	setting.add_on_change('LatexSymbols', get_settings)

def _parseSettings(entries, category):
	ret = []
	for e in entries:
		if isinstance(e, list):
			cmd = {
				'caption': category + e[1] + ' ' + e[0],
				'text': e[1]
			}
			ret.append(cmd)
		else:
			sub_cat = _parseSettings(e['entries'], category + e['category'] + ': ')
			ret.extend(sub_cat)
	return ret

# Sublime command format
# [
#     {
#         "command": "insert_symbol", 
#         "caption": "LatexSymbols: Greek: \\alpha \u03b1", 
#         "args": {
#             "text": "\\alpha"
#         }
#     }, 
# ]
def _toSublimeCommands(cmd_list):
	warningMsg = """// DO NOT EDIT!
// This file is generated from LatexSymbols.sublime-settings automatically.
// Always edit that settings file.
"""
	ret = []
	for e in cmd_list:
		cmd = {
			'caption': e['caption'],
			'command': 'insert_symbol',
			'args': {'text': e['text']}
		}
		ret.append(cmd)
	return warningMsg + json.dumps(ret, indent=4)

# Sublime snippet format -- this only works with one snippet
# <snippet>
#     <content><![CDATA[\alpha]]></content>
#     <!-- Optional: Scope the tab trigger will be active in -->
#     <scope>text.tex</scope>
#     <!-- Optional: Description to show in the menu -->
#     <description>My Fancy Snippet &#x03B1;</description>
# </snippet>
def _toSublimeSnippets(cmd_list):
	warningMsg = """<!--
DO NOT EDIT!
This file is generated from LatexSymbols.sublime-settings automatically.
Always edit that settings file.
-->
"""
	ret = ""
	for e in cmd_list:
		s = """<snippet>
    <content><![CDATA[""" + e['text'] + """]]></content>
    <scope>text.tex</scope>
    <description>""" + e['caption'] + """</description>
</snippet>
"""
		ret += s
	return warningMsg + ret
