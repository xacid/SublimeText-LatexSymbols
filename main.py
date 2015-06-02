"""
1. Save settings in *.sublime-settings
2. Load settings and convert to *.sublime-commands
3. Invoke commands with InsertSymbol with args.
"""

import os
import json
import sublime, sublime_plugin



class InsertSymbolCommand(sublime_plugin.TextCommand):
	def run(self, edit, text = ""):
		view = self.view
		view.insert(edit, view.sel()[0].a, text)


def get_settings():
	setting = sublime.load_settings('LatexSymbols.sublime-settings')
	sym_list = setting.get('symbol_list', [])
	cmd_list = []
	for sym in sym_list:
		cmd = {'caption': sym['caption'], 'command': 'insert_symbol', 'args': {'text': sym['text']}}
		cmd_list.append(cmd)
	# write sym_list to LatexSymbols.sublime-commands
	commandFilePath = os.path.join(sublime.packages_path(), 'User', 'LatexSymbols.sublime-commands')
	f = open(commandFilePath, 'w')
	json.dump(cmd_list, f)

def plugin_loaded():
	get_settings()

