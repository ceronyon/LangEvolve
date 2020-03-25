'''
Created on Mar 25, 2020

@author: ojima
'''

import gi
import json
import re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

__author__ = "ojima"
__version__ = "0.1"


class LangEvolveWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "LangEvolve v{0}".format(__version__))
        
        self.set_size_request(800, 600)
        self.set_border_width(12)
        
        super_frame = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        self.add(super_frame)
        
        columns = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        columns.set_property("expand", True)
        input_frame = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        rules_frame = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        output_frame = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        
        input_frame.pack_start(Gtk.Label("Input Lexicon"), False, True, 0)
        output_frame.pack_start(Gtk.Label("Output Lexicon"), False, True, 0)
        
        # Packing the input frame
        input_scroller = Gtk.ScrolledWindow()
        input_scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        input_view = Gtk.TextView()
        input_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.input_words = Gtk.TextBuffer()
        self.input_words.set_text("Input your words here...")
        input_view.set_buffer(self.input_words)
        input_scroller.add(input_view)
        input_frame.pack_start(input_scroller, True, True, 0)
        
        import_buttons = Gtk.Grid()
        input_frame.pack_start(import_buttons, False, True, 0)
        
        self.import_word_button = Gtk.Button("Import Words")
        self.import_word_button.connect("clicked", self.on_words_import)
        import_buttons.attach(self.import_word_button, 0, 0, 1, 1)
        
        self.save_word_button = Gtk.Button("Save Words")
        self.save_word_button.connect("clicked", self.on_input_export)
        import_buttons.attach(self.save_word_button, 1, 0, 1, 1)
        
        # Packing the rules frame
        rules_frame.pack_start(Gtk.Label("Categories"), False, True, 0)
        
        categories_scroller = Gtk.ScrolledWindow()
        categories_view = Gtk.TextView()
        self.categories = Gtk.TextBuffer()
        self.categories.set_text("Input your categories here...")
        categories_view.set_buffer(self.categories)
        categories_scroller.add(categories_view)
        
        rules_frame.pack_start(categories_scroller, True, True, 0)
        
        rules_frame.pack_start(Gtk.Label("Rules"), False, True, 0)
        
        rules_scroller = Gtk.ScrolledWindow()
        rules_view = Gtk.TextView()
        self.rules = Gtk.TextBuffer()
        self.rules.set_text("Input your rules here...")
        rules_view.set_buffer(self.rules)
        rules_scroller.add(rules_view)
        
        rules_frame.pack_start(rules_scroller, True, True, 0)
        
        rules_frame_buttons = Gtk.Grid()
        rules_frame.pack_start(rules_frame_buttons, False, True, 0)
        
        # Import rules button
        self.import_rules_button = Gtk.Button("Import Rules")
        self.import_rules_button.connect("clicked", self.on_rules_import)
        rules_frame_buttons.attach(self.import_rules_button, 0, 0, 1, 1)
        
        # Save rules button
        self.save_rules_button = Gtk.Button("Save Rules")
        self.save_rules_button.connect("clicked", self.on_rules_export)
        rules_frame_buttons.attach(self.save_rules_button, 1, 0, 1, 1)
        
        # Apply rules button
        self.apply_rules_button = Gtk.Button("Apply Rules")
        self.apply_rules_button.connect("clicked", self.on_rules_apply)
        rules_frame_buttons.attach(self.apply_rules_button, 0, 1, 2, 1)
        
        # Packing the output frame
        output_scroller = Gtk.ScrolledWindow()
        output_scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        output_view = Gtk.TextView()
        output_view.set_wrap_mode(Gtk.WrapMode.WORD)
        output_view.set_property("editable", False)
        self.output_buffer = Gtk.TextBuffer()
        self.output_buffer.set_text("Your results will appear here")
        output_view.set_buffer(self.output_buffer)
        output_scroller.add(output_view)
        output_frame.pack_start(output_scroller, True, True, 0)
        
        output_buttons = Gtk.Grid()
        self.save_output_button = Gtk.Button("Save Output")
        self.save_output_button.connect("clicked", self.on_output_export)
        output_buttons.attach(self.save_output_button, 0, 0, 1, 1)
        output_frame.pack_start(output_buttons, False, True, 0)
        
        # Pack all the individual columns into the column frame
        columns.pack_start(input_frame, True, True, 0)
        columns.pack_start(rules_frame, False, True, 0)
        columns.pack_start(output_frame, True, True, 0)
        
        # Pack the column frame into the central frame
        super_frame.pack_start(columns, True, True, 0)
        
        # Add a progress bar at the bottom.
        self.progress_bar = Gtk.ProgressBar()
        super_frame.pack_start(self.progress_bar, False, True, 0)
        
    def on_words_import(self, widget):
        dialog = Gtk.FileChooserDialog("Import words from file.", self, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        response = dialog.run()
        if response == Gtk.ResponseType.CANCEL:
            pass
        elif response == Gtk.ResponseType.OK:
            try:
                with open(dialog.get_filename(), 'r') as fp:
                    self.input_words.set_text(fp.read())
            except Exception as e:
                err = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Failed to read file.")
                err.format_secondary_text(str(e))
                err.run()
                err.destroy()
        
        dialog.destroy()
    
    def on_rules_import(self, widget):
        dialog = Gtk.FileChooserDialog("Import rules from file.", self, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                with open(dialog.get_filename(), 'r') as fp:
                    data = json.load(fp)
                    
                    res = ""
                    if 'categories' in data:
                        categories = data['categories']
                        for key in categories:
                            value = categories[key]
                            res += "{0}={1}\n".format(key, value)
                    
                    self.categories.set_text(res)
                    
                    res = ""
                    if 'rules' in data:
                        rules = data['rules']
                        for rule in rules:
                            key = list(rule.keys())[0]
                            value = rule[key]
                            
                            res += "{0}>{1}\n".format(key, value)
                    
                    self.rules.set_text(res)
                    
            except Exception as e:
                err = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Failed to read file.")
                err.format_secondary_text(str(e))
                err.run()
                err.destroy()
        
        dialog.destroy()
    
    def on_input_export(self, widget):
        try:
            dialog = Gtk.FileChooserDialog("Save input to file.", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
            
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                with open(dialog.get_filename(), 'w') as fp:
                    inputs = self.input_words.get_text(self.input_words.get_start_iter(), self.input_words.get_end_iter(), True).split('\n')
                    for line in inputs:
                        line = line.strip()
                        if line == '':
                            continue
                        
                        fp.write(line + '\n')
            elif response == Gtk.ResponseType.CANCEL:
                pass
            
            dialog.destroy()
        except Exception as e:
            err = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Failed to export input vocabulary.")
            err.format_secondary_text(str(e))
            err.run()
            err.destroy()
    
    def on_rules_export(self, widget):
        try:
            dialog = Gtk.FileChooserDialog("Save input to file.", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
            
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                res = { 'categories' : {}, 'rules' : [] }
                
                cats = self.categories.get_text(self.categories.get_start_iter(), self.categories.get_end_iter(), True).split('\n')
                for c in cats:
                    c = c.strip().split('=')
                    if len(c) < 2:
                        continue
                    res['categories'][c[0]] = c[1]
                
                rules = self.rules.get_text(self.rules.get_start_iter(), self.rules.get_end_iter(), True).split('\n')
                for r in rules:
                    r = r.strip().split('>')
                    if len(r) < 2:
                        continue
                    res['rules'].append({r[0] : r[1]})
                
                with open(dialog.get_filename(), 'w') as fp:
                    json.dump(res, fp, indent = 2, ensure_ascii = False)
            elif response == Gtk.ResponseType.CANCEL:
                pass
            
            dialog.destroy()
        except Exception as e:
            err = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Failed to export rules.")
            err.format_secondary_text(str(e))
            err.run()
            err.destroy()
    
    def on_output_export(self, widget):
        try:
            dialog = Gtk.FileChooserDialog("Save input to file.", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
            
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                with open(dialog.get_filename(), 'w') as fp:
                    inputs = self.output_buffer.get_text(self.output_buffer.get_start_iter(), self.output_buffer.get_end_iter(), True).split('\n')
                    for line in inputs:
                        line = line.strip()
                        if line == '':
                            continue
                        
                        fp.write(line + '\n')
            elif response == Gtk.ResponseType.CANCEL:
                pass
            
            dialog.destroy()
        except Exception as e:
            err = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Failed to export output vocabulary.")
            err.format_secondary_text(str(e))
            err.run()
            err.destroy()
    
    def on_rules_apply(self, widget):
        try:
            lines = self.input_words.get_text(self.input_words.get_start_iter(), self.input_words.get_end_iter(), True).split('\n')
            if len(lines) == 0:
                raise Exception("No input words found!")
            
            categories = { }
            for cat in self.categories.get_text(self.categories.get_start_iter(), self.categories.get_end_iter(), True).split('\n'):
                cat = cat.strip()
                if cat == '':
                    continue
                
                splits = cat.split('=')
                
                if len(splits) != 2:
                    raise Exception("Failed to parse category '{0}'.".format(cat))
                
                inp = splits[0].strip()
                out = splits[1].strip()
                
                categories[inp] = out
            
            rules = [ ]
            
            for rule in self.rules.get_text(self.rules.get_start_iter(), self.rules.get_end_iter(), True).split('\n'):
                rule = rule.strip()
                if rule == '':
                    continue
                
                splits = rule.split('>')
                
                if len(splits) != 2:
                    raise Exception("Failed to parse rule '{0}'.".format(rule))
                
                inp = splits[0].strip()
                out = splits[1].strip()
                
                if '%' in out:
                    i = list(re.findall("%([a-zA-Z]{1})", inp))[0]
                    o = list(re.findall("%([a-zA-Z]{1})", out))[0]
                    
                    if i not in categories:
                        raise Exception("Failed to find category {0} needed for rule '{1}'".format(i, rule))
                    
                    if o not in categories:
                        raise Exception("Failed to find category {0} needed for rule '{1}'".format(o, rule))
                    
                    in_cat = categories[i]
                    out_cat = categories[o]
                    
                    if len(in_cat) != len(out_cat):
                        raise Exception("Failed to substitute categories into rule '{0}': unequal category size.".format(rule))
                    
                    for x, y in zip(in_cat, out_cat):
                        rules.append((re.sub("%{0}".format(i), x, inp), re.sub("%{0}".format(o), y, out)))
                else:
                    for cat in categories.keys():
                        inp = re.sub('%{0}'.format(cat), '[{0}]'.format(categories[cat]), inp)
                    
                    rules.append((inp, out))
            
            self.progress_bar.set_fraction(0.0)
            
            results = ''
            for i, line in enumerate(lines):
                res_line = ''
                words = line.strip().split(' ')
                for word in words:
                    outcome = word.strip()
                    
                    for rule, replace in rules:
                        outcome = re.sub(rule, replace, outcome)
                    
                    res_line += '{0} '.format(outcome)
                
                results += '{0}\n'.format(res_line.strip())
                    
                self.progress_bar.set_fraction((i + 1) / len(lines))
                
            self.output_buffer.set_text(results)
        except Exception as e:
            err = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Failed to apply rules.")
            err.format_secondary_text(str(e))
            err.run()
            err.destroy()
    
    def on_results_export(self, widget):
        print("Pressed export results button.")


win = LangEvolveWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
