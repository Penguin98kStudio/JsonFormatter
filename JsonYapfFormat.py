import sublime
import sublime_plugin

import subprocess
import re
import textwrap


class JsonYapfFormatCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		content = self.view.substr(sublime.Region(0, self.view.size()))
		content = content.replace("//", "#")
		content = content.replace("res:#", "res://")
		indexes = re.finditer(",\\s*[\\)\\]\\}]", content)
		indexes = [i.start() for i in indexes]
		content = "".join(
			[char for i, char in enumerate(content) if i not in indexes]
		)
		content = content.replace("true","True").replace("false","False")
		if '\\' not in sublime.packages_path():
			path = sublime.packages_path() + '/JSONFORMATTERF/'
		else:
			path = sublime.packages_path() + '\\JSONFORMATTERF\\'

		with open(path + 'temporary.notpy', 'w') as file:
			file.write(content)

		command = 'yapf "' + path + 'temporary.notpy" -i --style style.txt'
		print("Running"+command)
		process = subprocess.Popen(command, shell=True)
		error = ""
		if process.wait() != 0:
			error = (
				"Error: Yapf module is either not installed or not on path or Something Went Wrong while YAPF was trying to Format the File"
			)
		with open(path + 'temporary.notpy', 'r') as file:
			content = file.read()
		content = content.replace("#", "//")
		content = content.replace("True","true").replace("False","false")
		if error:
			print(error)
			sublime.set_timeout_async(lambda: sublime.status_message(error), 1000)
	
		self.view.replace(edit, sublime.Region(0, self.view.size()), content)

	def is_enabled(self):
		return self.view.match_selector(0, "source.json")
