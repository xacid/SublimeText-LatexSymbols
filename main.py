# 1. Save settings in *.sublime-settings
# 2. Load settings and convert to *.sublime-commands
# 3. Invoke commands by InsertSymbol with args.

import os
import json
import sublime, sublime_plugin

### Global consts
PLUGIN = 'LatexSymbols'
PLUGIN_SETTINGS = PLUGIN + '.sublime-settings'
PLUGIN_COMMANDS = PLUGIN + '.sublime-commands'
CATEG_JSON = 'category'
ENTRI_JSON = 'entries'
SYMLI_JSON = 'symbol_list'
SEP = ': '

class InsertSymbolCommand(sublime_plugin.TextCommand):
	def run(self, edit, text = ""):
		view = self.view
		view.insert(edit, view.sel()[0].a, text)

def plugin_loaded():
	setting = sublime.load_settings(PLUGIN_SETTINGS)
	setting.add_on_change(PLUGIN, _settingsOnChange)

### Private helpers
def _settingsOnChange():
	#print("update 'LatexSymbols.sublime-commands'")
	commandFilePath = os.path.join(sublime.packages_path(), 'User', PLUGIN_COMMANDS)
	setting = sublime.load_settings(PLUGIN_SETTINGS)
	sym_list = setting.get(SYMLI_JSON, [])
	cmd_list = _parseSettings(sym_list, PLUGIN + SEP)
	#print("write to " + commandFilePath)
	f = open(commandFilePath, 'w')
	f.write(_toSublimeCommands(cmd_list))
	f.close()

def _parseSettings(entries, category):
	ret = []
	for e in entries:
		if isinstance(e, list):
			cmd = {
				'caption': category + e[0] + ' ' + e[1], # TODO: working with package
				'text': e[1]
			}
			ret.append(cmd)
		else:
			sub_cat = _parseSettings(e[ENTRI_JSON], category + e[CATEG_JSON] + SEP)
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
