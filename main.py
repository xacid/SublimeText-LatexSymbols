"""
1. Save settings in *.sublime-settings
2. Load settings and convert to *.sublime-commands
3. Invoke commands with InsertSymbol with args.
"""

import sublime, sublime_plugin



class InsertSymbolCommand(sublime_plugin.TextCommand):
	def run(self, edit, name = ""):
		view = self.view
		view.insert(edit, view.sel()[0].a, name)


def get_settings():
	setting = sublime.load_settings('LatexSymbols.sublime-settings')
	sym_list = setting.get('symbol_list', [])
	# write sym_list to Default.sublime-commands
	for sym in sym_list:
		print(sym['command'], sym['text'])

def plugin_loaded():
	get_settings()

