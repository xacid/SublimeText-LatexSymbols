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
	#print("LatexSymbols get_settings()")
	setting = sublime.load_settings('LatexSymbols.sublime-settings')
	sym_list = setting.get('symbol_list', [])
	cmd_list = parse_settings(sym_list, 'LatexSymbols: ')
	#print(cmd_list)
	# write sym_list to LatexSymbols.sublime-commands
	commandFilePath = os.path.join(sublime.packages_path(), 'User', 'LatexSymbols.sublime-commands')
	f = open(commandFilePath, 'w')
	json.dump(cmd_list, f, indent=4)

def parse_settings(entries, category):
	ret = []
	for e in entries:
		if isinstance(e, list):
			cmd = {
				'caption': category + e[1] + ' ' + e[0], 
				'command': 'insert_symbol', 'args': {'text': e[1]}
			}
			ret.append(cmd)
		else:
			sub_cat = parse_settings(e['entries'], category + e['category'] + ': ')
			ret.extend(sub_cat)
	return ret

def plugin_loaded():
	get_settings()

