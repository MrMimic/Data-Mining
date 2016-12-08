#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Un code pour afficher des boites de saisies pour générer plus vite la fiche documentalistes.

# # # # # # # # # # # # #
# IMPORTS
import tkinter
import re

# PARENT CLASS
class simpleapp_tk(tkinter.Tk):
	def __init__(self, parent):
		tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	# SELF INIT
	def initialize(self):
		self.grid()

		# WINDOW SIZE
		#self.grid_columnconfigure(1,weight=6)
		#self.resizable(True,False)
		# Horiz / Vert
 
		# CATEGORIES VARIABLES
		self.category = tkinter.StringVar()
		self.maintener_name = tkinter.StringVar()
		self.maintener_email = tkinter.StringVar()
		self.tool_name = tkinter.StringVar()
		self.tool_url = tkinter.StringVar()
	
		self.description = tkinter.StringVar()
	  
		self.documentation = tkinter.StringVar()
		self.forum = tkinter.StringVar()
		self.addinfos = tkinter.StringVar()
	  
		self.affiliation = tkinter.StringVar()
	  
		self.fundings = tkinter.StringVar()
	  
		self.autetal = tkinter.StringVar()
		self.pubname = tkinter.StringVar()
		self.pubjournal = tkinter.StringVar()
		self.doi = tkinter.StringVar()
	  
		self.taxon = tkinter.StringVar()

		### DOUBLE BOUCLE FOR POUR ACCHIER CETTE MERDE
		# CATEGORIES POP
		self.entry = tkinter.Entry(self, textvariable=self.category) ; self.entry.grid(column = 1, row = 0, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
		self.entry = tkinter.Entry(self, textvariable=self.maintener_name) ; self.entry.grid(column = 1, row = 1, ipadx=200, ipady=5, padx=5, pady=5)
		self.entry = tkinter.Entry(self, textvariable=self.maintener_email) ; self.entry.grid(column = 2, row = 1, ipadx=200, ipady=5, padx=5, pady=5)
		self.entry = tkinter.Entry(self, textvariable=self.tool_name) ; self.entry.grid(column = 1, row = 3, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
		self.entry = tkinter.Entry(self, textvariable=self.tool_url) ; self.entry.grid(column = 1, row = 4, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
	
		self.entry = tkinter.Entry(self, textvariable=self.description) ; self.entry.grid(column = 1, row = 5, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
	  
		self.entry = tkinter.Entry(self, textvariable=self.documentation) ; self.entry.grid(column = 1, row = 6, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
		self.entry = tkinter.Entry(self, textvariable=self.forum) ; self.entry.grid(column = 1, row = 7, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
		self.entry = tkinter.Entry(self, textvariable=self.addinfos) ; self.entry.grid(column = 1, row = 8, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
	  
		self.entry = tkinter.Entry(self, textvariable=self.affiliation) ; self.entry.grid(column = 1, row = 9, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
	  
		self.entry = tkinter.Entry(self, textvariable=self.fundings) ; self.entry.grid(column = 1, row = 10, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
	  
		self.entry = tkinter.Entry(self, textvariable=self.autetal) ; self.entry.grid(column = 0, row = 11, ipadx=200, ipady=5, padx=5, pady=5, columnspan = 2)
		self.entry = tkinter.Entry(self, textvariable=self.pubname) ; self.entry.grid(column = 1, row = 11, ipadx=200, ipady=5, padx=5, pady=5, columnspan = 2)
		self.entry = tkinter.Entry(self, textvariable=self.pubjournal) ; self.entry.grid(column = 2, row = 11, ipadx=200, ipady=5, padx=5, pady=5, columnspan = 2)
		self.entry = tkinter.Entry(self, textvariable=self.doi) ; self.entry.grid(column = 1, row = 12, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
	 
		self.entry = tkinter.Entry(self, textvariable=self.taxon) ; self.entry.grid(column = 1, row = 13, ipadx=467, ipady=5, padx=5, pady=5, columnspan = 2)
	  
	  
		self.category.set("Category")
		self.maintener_name.set("Maintener Name")
		self.maintener_email.set("email@maintener")
	  
		self.tool_name.set("Tool name")
		self.tool_url.set("Tool URL")
	  
		self.description.set("Description")
	  
		self.documentation.set("Documentation")
		self.forum.set("Forum")
		self.addinfos.set("Additionnal Infos")
	  
		self.affiliation.set("Affiliation")
	  
		self.fundings.set("Fundings")
	  
		self.autetal.set("Author et al.")
		self.pubname.set("Publication title")
		self.pubjournal.set("Journal")
		self.doi.set("DOI")
	  
		self.taxon.set("Taxon")
  
		# BUTTON POP
		button = tkinter.Button(self, text = "Submit", command = self.OnButtonClick, bg = "forestgreen")
		button.grid(column = 2, row = 14, ipadx = 100, columnspan = 1, padx = 5, pady = 5)

	# GET VARIABLES WITH BUTTON ACTION
	def OnButtonClick(self):
  
		v_cat = self.category.get()
		v_mai = self.maintener_name.get()
		v_mem = self.maintener_email.get()
		v_tna = self.tool_name.get()
		v_tur = self.tool_url.get()
	  
		v_des = self.description.get()
	  
		v_doc = self.documentation.get()
		v_for = self.forum.get()
		v_add = self.addinfos.get()
	  
		v_aff = self.affiliation.get()
	  
		v_fun = self.fundings.get()
	  
		v_aut = self.autetal.get()
		v_pna = self.pubname.get()
		v_pjo = self.pubjournal.get()
		v_doi = self.doi.get()
	  
		v_tax = self.taxon.get()

		with open("my_submission.txt", "w", encoding = "utf-8") as mon_fichier:

			# WRITING IN NEW FILE
			mon_fichier.write("## \n")
			mon_fichier.write(v_cat + "\n")
			v_mem2 = re.sub(r"\@", " at ", v_mem)
			mon_fichier.write(v_mai + "<" + v_mem2 + ">" + "\n")
			mon_fichier.write(v_tna + "\n")
			mon_fichier.write(v_tur + "\n" + "\n")
			
			mon_fichier.write(v_des + "\n" + "\n")
			
			mon_fichier.write(v_doc + "\n")
			mon_fichier.write(v_for + "\n")
			mon_fichier.write(v_add + "\n" + "\n")
			
			mon_fichier.write(v_aff + "\n" + "\n")
			
			mon_fichier.write(v_fun + "\n" + "\n")
			
			mon_fichier.write("(" + v_aut + ")")
			mon_fichier.write(" " + v_pna + ". ")
			mon_fichier.write(v_pjo + ".\n")
			mon_fichier.write(v_doi + "\n" + "\n")
			mon_fichier.write(v_tax + "\n" + "\n")
	
		mon_fichier.close()
	  
		app.destroy()

if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title("Data Submussion Tool - Main")
	app.mainloop()


#########################################
############ WINDOWS 2 ##################
#########################################

class simpleapp_tk(tkinter.Tk):
	def __init__(self, parent):
		tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	# SELF INIT
	def initialize(self):
		self.grid()
		
		# CATEGORIES
		self.label = tkinter.Label(self, text = "Desktop App", fg = "red", relief = "groove") ; self.label.grid(column = 1, row = 1, ipadx = 30, columnspan = 2, padx = 5, pady = 5)
		self.label = tkinter.Label(self, text = "Web App", fg = "blue", relief = "groove") ; self.label.grid(column = 4, row = 1, ipadx = 30, columnspan = 2, padx = 5, pady = 5)
		self.label = tkinter.Label(self, text = "Database", fg = "green", relief = "groove") ; self.label.grid(column = 7, row = 1, ipadx = 30, columnspan = 2, padx = 5, pady = 5)
		
		### BOUCLE FOR POUR AFFICHER TOUTE CETTE MERDE
		# DESKTOP APP
		self.da_arc = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_arc) ; self.entry.grid(column = 1, row = 2, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_arc.set("Software")
		self.da_pla = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_pla) ; self.entry.grid(column = 1, row = 3, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_pla.set("Desktop app")
		self.da_ver = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_ver) ; self.entry.grid(column = 1, row = 4, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_ver.set("Version")
		self.da_sta = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_sta) ; self.entry.grid(column = 1, row = 5, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_sta.set("Stable")
		self.da_dow = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_dow) ; self.entry.grid(column = 1, row = 6, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_dow.set("Download URL")
		self.da_req = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_req) ; self.entry.grid(column = 1, row = 7, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_req.set("Requirement")
		self.da_typ = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_typ) ; self.entry.grid(column = 1, row = 8, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_typ.set("Package")
		self.da_lau = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_lau) ; self.entry.grid(column = 1, row = 9, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_lau.set("GUI")
		self.da_ind = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_ind) ; self.entry.grid(column = 1, row = 10, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_ind.set("Input Data")
		self.da_inf = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_inf) ; self.entry.grid(column = 1, row = 11, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_inf.set("Input Format")
		self.da_oud = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_oud) ; self.entry.grid(column = 1, row = 12, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_oud.set("Output Data")
		self.da_ouf = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_ouf) ; self.entry.grid(column = 1, row = 13, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_ouf.set("Output Format")
		self.da_ops = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_ops) ; self.entry.grid(column = 1, row = 14, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_ops.set("All platforms")
		self.da_lan = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_lan) ; self.entry.grid(column = 1, row = 15, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_lan.set("Language")
		self.da_sou = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_sou) ; self.entry.grid(column = 1, row = 16, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_sou.set("Source URL")
		self.da_ski = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_ski) ; self.entry.grid(column = 1, row = 17, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_ski.set("Basic")
		self.da_res = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_res) ; self.entry.grid(column = 1, row = 18, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_res.set("Restrictions")
		self.da_lic = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_lic) ; self.entry.grid(column = 1, row = 19, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_lic.set("License")
		
		# WEB APP
		self.wa_arc = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_arc) ; self.entry.grid(column = 4, row = 2, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_arc.set("Software")
		self.wa_pla = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_pla) ; self.entry.grid(column = 4, row = 3, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_pla.set("Web app")
		self.wa_ver = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_ver) ; self.entry.grid(column = 4, row = 4, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_ver.set("Version")
		self.wa_sta = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_sta) ; self.entry.grid(column = 4, row = 5, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_sta.set("Stable")
		self.wa_req = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_req) ; self.entry.grid(column = 4, row = 6, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_req.set("Requirement")
		self.wa_typ = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_typ) ; self.entry.grid(column = 4, row = 7, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_typ.set("Package")
		self.wa_lau = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_lau) ; self.entry.grid(column = 4, row = 8, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_lau.set("WUI")
		self.wa_ind = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_ind) ; self.entry.grid(column = 4, row = 9, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_ind.set("Input Data")
		self.wa_inf = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_inf) ; self.entry.grid(column = 4, row = 10, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_inf.set("Input Format")
		self.wa_oud = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_oud) ; self.entry.grid(column = 4, row = 11, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_oud.set("Output Data")
		self.wa_ouf = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_ouf) ; self.entry.grid(column = 4, row = 12, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_ouf.set("Output Format")
		self.wa_ops = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_ops) ; self.entry.grid(column = 4, row = 13, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_ops.set("All platforms")
		self.wa_lan = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_lan) ; self.entry.grid(column = 4, row = 14, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_lan.set("Language")
		self.wa_sou = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_sou) ; self.entry.grid(column = 4, row = 15, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_sou.set("Source URL")
		self.wa_ski = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_ski) ; self.entry.grid(column = 4, row = 16, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_ski.set("Basic")
		self.wa_res = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_res) ; self.entry.grid(column = 4, row = 17, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_res.set("Restrictions")
		self.wa_lic = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.wa_lic) ; self.entry.grid(column = 4, row = 18, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.wa_lic.set("License")
		
		# DATABSE
		self.da_arc = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_arc) ; self.entry.grid(column = 7, row = 2, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_arc.set("Database")
		self.da_ver = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_ver) ; self.entry.grid(column = 7, row = 3, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_ver.set("Version")
		self.da_acc = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_acc) ; self.entry.grid(column = 7, row = 4, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_acc.set("Access")
		self.da_man = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_man) ; self.entry.grid(column = 7, row = 5, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_man.set("Management")
		self.da_lan = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_lan) ; self.entry.grid(column = 7, row = 6, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_lan.set("Language")
		self.da_uss = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_uss) ; self.entry.grid(column = 7, row = 7, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_uss.set("No")
		self.da_cdr = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_cdr) ; self.entry.grid(column = 7, row = 8, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_cdr.set("No")
		self.da_res = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_res) ; self.entry.grid(column = 7, row = 9, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_res.set("Restriction")
		self.da_lic = tkinter.StringVar() ; self.entry = tkinter.Entry(self, textvariable=self.da_lic) ; self.entry.grid(column = 7, row = 10, ipadx = 30, ipady = 5, columnspan = 2, padx = 5, pady = 5) ; self.da_lic.set("License")

		# BUTTONS
		button_daa = tkinter.Button(self, text = "Submit", command = self.OnButtonClick_dap, bg = "red") ; button_daa.grid(column = 1, row = 20, ipadx = 30, columnspan = 2, padx = 5, pady = 5)
		button_waa = tkinter.Button(self, text = "Submit", command = self.OnButtonClick_wap, bg = "blue") ; button_waa.grid(column = 4, row = 20, ipadx = 30, columnspan = 2, padx = 5, pady = 5)
		button_dat = tkinter.Button(self, text = "Submit", command = self.OnButtonClick_dat, bg = "green") ; button_dat.grid(column = 7, row = 20, ipadx = 30, columnspan = 2, padx = 5, pady = 5)
		
	def OnButtonClick_dap(self):
		# GET DESKTOP APP VAR
		app.destroy()
		
	def OnButtonClick_wap(self):
		# GET WEB APP VAR
		app.destroy()
		
	def OnButtonClick_dat(self):
		# GET DATABASE APP
		app.destroy()

if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title("Data Submussion Tool - Detail")
	app.mainloop()	
