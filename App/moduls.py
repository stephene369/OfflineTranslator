import argostranslate.package
import argostranslate.translate
from json import dumps, loads , load
from pathlib import Path 
from os import path 
from time import time 
import sqlite3 
from datetime import datetime

class Translator : 
    def __init__(self ) -> None:
        self.isLangInit = False
        #argostranslate.package.update_package_index()
        self.available_packages = argostranslate.package.get_available_packages()
        self.available_packages_list = sorted([ str(i).replace("→","->") for i in self.available_packages ] )

        if Path("App/database/").exists() == False : 
            Path("App/database/").mkdir() 
        
        if Path("App/languages/").exists() == False : 
            Path("App/languages/").mkdir() 

        if Path("App/languages/availables.json").exists() == False :
            print("Updating availables.json")
            self.updateAvailablePackages()


        with open("App/languages/codes.json" , "r") as f:
            self.codes = load(f)



    def updateAvailablePackages(self) -> None:
        # TO get all availables packages

        # To get from available languages
        self.models = sorted([ str(i).replace("→","->") for i in self.available_packages ] )

        # To save to jsno 
        with open("App/languages/availables.json","w") as f:
            f.write( dumps( 
                {"Models" : self.models}, 
                indent=4 ) 
            ) 


    def isInstalledLanguagesPackages(self , from_code , to_code) -> bool:
        self.installed = argostranslate.package.get_installed_packages()

        available_package = list(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, self.available_packages
            ))[0]
        return available_package in argostranslate.package.get_installed_packages()


    def installLanguagesPackages(self , from_language , to_language) : 
        print("Updating package index ...")
        argostranslate.package.update_package_index()
        with open("App/languages/codes.json" , "r") as f : 
            data = load(f) 
            from_code = data[from_language]
            to_code = data[to_language]

        available_package = list(filter(lambda x: x.from_code == from_code and x.to_code == to_code, self.available_packages))[0]
        
        print("Downloading Package ...")
        download_path = available_package.download()
        argostranslate.package.install_from_path(download_path)
        print("Downloaded and installed.")
        
        return True
    
    
    def uninstallPackage(self,from_language , to_language):
        with open("App/languages/codes.json" , "r") as f : 
            data = load(f) 
            from_code = data[from_language]
            to_code = data[to_language]

        available_package = list(filter(lambda x: x.from_code == from_code and x.to_code == to_code, self.available_packages))[0]   
             
        argostranslate.package.uninstall( available_package )

    def initDatabase(self):
        self.conn = sqlite3.connect("App/database/history.db")
        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS history ( 
                         id TEXT PRIMARY KEY , 
                         languages VARCHAR, 
                         from_lang TEXT,
                         to_lang TEXT
             )
            """)
        self.conn.commit()


    def insertData(self, languages, from_lang, to_lang):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute("INSERT INTO history (id, languages, from_lang, to_lang) VALUES (?, ?, ?, ?)",
                         (current_time, languages, from_lang, to_lang))
        self.conn.commit()
        

    def installedPackages(self) :
        return argostranslate.package.get_installed_packages()


    def initLang(self , from_language , to_language) : 
        self.isLangInit = True
        with open("App/languages/codes.json" , "r") as f : 
            data = load(f) 
            from_code = data[from_language]
            to_code = data[to_language]


        self.installed_languages = argostranslate.translate.get_installed_languages()
        self.from_lang = list(filter(
                lambda x: x.code == from_code,
                self.installed_languages))[0]

        self.to_lang = list(filter(
                lambda x: x.code == to_code,
                self.installed_languages))[0]
        
        self.translation = self.from_lang.get_translation(self.to_lang)

    def translate(self, text:str) -> str: 
        return self.translation.translate(text)
