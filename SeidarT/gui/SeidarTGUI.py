import exe
import kivy
import numpy as np
import os
import re
import sys

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout


kivy.require('1.11.1')

MATERIALS = None

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 640
WINDOW_MIN_HEIGHT = 480
WINDOW_MIN_WIDTH = 600

Config.set('graphics', 'width', WINDOW_WIDTH)
Config.set('graphics', 'height', WINDOW_HEIGHT)
Config.set('graphics', 'minimum_width', WINDOW_MIN_WIDTH)
Config.set('graphics', 'minimum_height', WINDOW_MIN_HEIGHT)

#This is the color for the background of the tabs, not the color on each tab.
Window.clearcolor = (.7, .7, .7, 1)

class MultiShotInput(RelativeLayout):
    pass


class Seismic(RelativeLayout):
    pass


class Radar(RelativeLayout):
    pass


class SpacialInformation(RelativeLayout):
    pass


class MaterialBox(BoxLayout):
    pass


class DimensionButtons(RelativeLayout):
    pass


class GlacierImage(Image):
    pass


class MaterialWindow(ScrollView):
    def __init__(self, **kwargs):
        super(MaterialWindow, self).__init__(**kwargs)


class RunButton(Button):
    def __init__(self, **kwargs):
        super(RunButton, self).__init__(**kwargs)

    def run(self):
        curr_prj_file_name = ""
        for widget in self.parent.children:
            if widget.name == "image_input":
                curr_prj_file_name = widget.file_name
                command = "python exe/prjbuild.py -i gui/" + widget.file_name + ".png -o gui/" + widget.file_name + ".prj"
                os.system(command)

        prj_file = open("gui/" + curr_prj_file_name + ".prj", "r+")
        prj_text = prj_file.read()
        for top_level_widget in self.parent.children:
            if top_level_widget.name == "radar":
                radar = top_level_widget.children[0]
                prj_text = re.sub("E,time_steps,", "E,time_steps," + radar.children[6].text, prj_text)
                prj_text = re.sub("E,x,", "E,x," + radar.children[10].text, prj_text)
                prj_text = re.sub("E,y,", "E,y," + radar.children[9].text, prj_text)
                prj_text = re.sub("E,z,", "E,z," + radar.children[8].text, prj_text)
                prj_text = re.sub("E,f0,", "E,f0," + radar.children[2].text, prj_text)
                prj_text = re.sub("E,theta,0", "E,theta," + radar.children[4].text, prj_text)
                prj_text = re.sub("E,phi,0", "E,phi," + radar.children[0].text, prj_text)
            elif top_level_widget.name == "seismic":
                seismic = top_level_widget.children[0]
                prj_text = re.sub("S,time_steps,", "S,time_steps," + seismic.children[6].text, prj_text)
                prj_text = re.sub("S,x,", "S,x," + seismic.children[10].text, prj_text)
                prj_text = re.sub("S,y,", "S,y," + seismic.children[9].text, prj_text)
                prj_text = re.sub("S,z,", "S,z," + seismic.children[8].text, prj_text)
                prj_text = re.sub("S,f0,", "S,f0," + seismic.children[2].text, prj_text)
                prj_text = re.sub("S,theta,0", "S,theta," + seismic.children[4].text, prj_text)
                prj_text = re.sub("S,phi,0", "S,phi," + seismic.children[0].text, prj_text)
            elif top_level_widget.name == "spacial_information":
                spacial = top_level_widget.children[0]
                prj_text = re.sub("D,dx,", "D,dx," + spacial.children[6].text, prj_text)
                prj_text = re.sub("D,dy,n/a", "D,dy," + spacial.children[5].text, prj_text)
                prj_text = re.sub("D,dz,", "D,dz," + spacial.children[4].text, prj_text)

            elif top_level_widget.name == "material_window":
                material_box_widget = top_level_widget.children[0]

                materialColors = re.findall("\d+/\d+/\d+", prj_text)
                for material in reversed(material_box_widget.children):

                    curr_material = "M," + str(material.material_number) + "," + material.children[6].text + "," + materialColors[
                        material.material_number]

                    for num in range(5, 1, -1):
                        curr_material += "," + material.children[num].text

                    curr_material += ",0"

                    curr_material += "," + str(material.children[1].active) + ","

                    if material.children[1].active:
                        curr_material += material.children[0].text

                    prj_text = re.sub("M.*,,,,,,,", curr_material, prj_text, count=1)

        prj_file.seek(0)
        # Update this so it writes the proper material information
        prj_file.write(prj_text)
        prj_file.truncate()

        #return file name for higher level button types have access to it
        return curr_prj_file_name




class SingleRunButton(RunButton):
    def SingleShot(self):
        file_name = super().run()

        #single shot specific stuff
        command = "python exe/prjrun.py " + file_name + ".prj -M b"

        #os.system(command)
        print (command)

class MultiRunButton(RunButton):
    def __init__(self, **kwargs):
        super(MultiRunButton, self).__init__(**kwargs)
    
    def MultiShot(self):
        file_name = super().run()

        command = "wide_angle -f " + file_name + ".prj -I"

        #multi shot specific stuff
        for i in self.parent.children:
            if i.name == "multi_shot_input":
                child = i.children[0]
                command += " " + child.children[8].text
                command += " " + child.children[7].text
                command += " " + child.children[6].text
                command += " -F"
                command += " " + child.children[4].text
                command += " " + child.children[3].text
                command += " " + child.children[2].text
                command += " -d " + child.children[0].text
                command += " -s" 


        #os.system(command)
        print (command)

class MaterialInput(GridLayout):
    def __init__(self, **kwargs):
        super(MaterialInput, self).__init__(**kwargs)
        self.material_number = None
        self.color = None


class TotalLayout(TabbedPanel):
    def __init__(self, **kwargs):
        super(TotalLayout, self).__init__(**kwargs)


class ImageInput(RelativeLayout):
    def __init__(self, **kwargs):
        super(ImageInput, self).__init__(**kwargs)
        self.image_things = [] #list of 4 ImageInput 
        self.box_layout = None
        self.image = None
        self.material_scrollview = None
        self.file_name = ""
        self.image_inputs = []
        self.defaultTab = False

    def getImage(self, first = True):
        if self.image:
            if first:
                self.parent.remove_widget(self.material_scrollview)
                self.material_scrollview = None
                self.box_layout = None
            self.remove_widget(self.image)
            self.image = None

        self.file_name = self.ids['file_path'].text

        if first:
            for i in self.image_inputs:
                if not i == self:
                    for j in i.children:
                        if j.name == "file_name":
                            j.text = self.file_name
                            i.getImage(first= False)
                            break
            

        self.image = GlacierImage()
        self.image.source = "gui/" + self.file_name + ".png"

        self.add_widget(self.image)

        # prjbuild -i /path/to/geometry/image.png -o project_filename.prj
        if self.defaultTab:
            # find a way to call prjbuild
            prj = None
            exists = False
            try:
                prj = open("gui/" + self.file_name + ".prj", 'r')
                exists = True
            except:
                command = "python exe/prjbuild.py -i gui/" + self.file_name + ".png -o gui/" + self.file_name + ".prj"
                os.system(command)
                prj = open("gui/" + self.file_name + ".prj", 'r')

            contents = prj.read()

            material_count = len(re.findall("M,", contents))


            self.material_scrollview = MaterialWindow()

            self.box_layout = MaterialBox(spacing=60, orientation='vertical', size_hint_y=None, height=0)

            # Acquire the colors from the prj
            colors = re.findall("\d*/\d*/\d*", contents)
            colorsKivy = []
            for i in range(len(colors)):
                colorsSplit = colors[i].split("/")

                colorsTuple = (
                (float(colorsSplit[0]) / 256), (float(colorsSplit[1]) / 256), (float(colorsSplit[2]) / 256), 1)

                colorsKivy.append(colorsTuple)

            for i in range(material_count):
                # Replace this with a row for a material
                # Create a new "structure" in the KV file for a row, given the color from the .prj
                temp = MaterialInput(size_hint_y=None, height=30)
                temp.material_number = i
                temp.color = colorsKivy[i]

                self.box_layout.add_widget(temp)

                ####################################################################################
                #TODO The spacing on this is too large, but decreasing it causes some rows to disappear#
                ####################################################################################
                self.box_layout.height += 80

            self.material_scrollview.add_widget(self.box_layout)

            self.parent.add_widget(self.material_scrollview)

            if exists:
                self.readExisting(contents)

    def readExisting(self, contents):
        for i in self.parent.children:
            #radar, seismic, spacial_information, material_window / material_box
            if i.name == "radar":
                radar = i.children[0]
                #populate radar text fields
                radar.children[6].text = re.findall("E,time_steps,\S*", contents)[0][13:]
                radar.children[10].text = re.findall("E,x,\S*", contents)[0][4:]
                radar.children[9].text = re.findall("E,y,\S*", contents)[0][4:]
                radar.children[8].text = re.findall("E,z,\S*", contents)[0][4:]
                radar.children[2].text = re.findall("E,f0,\S*", contents)[0][5:]
                radar.children[4].text = re.findall("E,theta,\S*", contents)[0][8:]
                radar.children[0].text = re.findall("E,phi,\S*", contents)[0][6:]
                for i in radar.children:
                    try:
                        if i.text == "":
                            i.text = None
                    except:
                        pass
            elif i.name == "seismic":
                seismic = i.children[0]
                #populate radar text fields
                seismic.children[6].text = re.findall("S,time_steps,\S*", contents)[0][13:]
                seismic.children[10].text = re.findall("S,x,\S*", contents)[0][4:]
                seismic.children[9].text = re.findall("S,y,\S*", contents)[0][4:]
                seismic.children[8].text = re.findall("S,z,\S*", contents)[0][4:]
                seismic.children[2].text = re.findall("S,f0,\S*", contents)[0][5:]
                seismic.children[4].text = re.findall("S,theta,\S*", contents)[0][8:]
                seismic.children[0].text = re.findall("S,phi,\S*", contents)[0][6:]
                for i in seismic.children:
                    try:
                        if i.text == "":
                            i.text = None
                    except:
                        pass

            elif i.name == "spacial_information":
                spacial = i.children[0]
                spacial.children[6].text = re.findall("D,dx,\S*", contents)[0][5:]
                spacial.children[5].text = re.findall("D,dy,\S*", contents)[0][5:]
                spacial.children[4].text = re.findall("D,dz,\S*", contents)[0][5:]

                for i in spacial.children:
                    try:
                        if i.text == "":
                            i.text = None
                    except:
                        pass

            elif i.name == "material_window":
                for j in i.children:
                    if j.name == "material_box":
                        for curr_material in zip(re.findall("M,\S*", contents),reversed(j.children)):
                            values = curr_material[0].split(",")
                            curr_widget = curr_material[1]

                            curr_widget.children[6].text = values[2]
                            curr_widget.children[5].text = values[4]
                            curr_widget.children[4].text = values[5]
                            curr_widget.children[3].text = values[6]
                            curr_widget.children[2].text = values[7]
                            curr_widget.children[1].active = True if values[9] == "True" else False
                            curr_widget.children[0].text = values[10]
                        #populate the material sections with this information
class SeidarTGUI(App):
    def build(self):
        # base tabbed thing
        base = TotalLayout(size=(WINDOW_WIDTH, WINDOW_HEIGHT))

        # Creating all tab panels
        panel1 = TabbedPanelItem()
        panel2 = TabbedPanelItem()
        panel3 = TabbedPanelItem()
        panel4 = TabbedPanelItem()
        helpPanel = TabbedPanelItem()
        
        # Naming all tabs
        panel1.text = "PRJ Info"
        panel2.text = ""
        panel3.text = ""
        panel4.text = ""
        helpPanel.text = "Help Page"

        # layout for the first tab
        panel1_layout = RelativeLayout()
        panel2_layout = RelativeLayout()
        
        #Image input stuff
        image_input = ImageInput()
        image_input_2 = ImageInput()

        image_input.defaultTab = True

        image_inputs = [image_input, image_input_2]
        image_input.image_inputs = image_inputs
        image_input_2.image_inputs = image_inputs

        # panel1-------------------------------------------------------------
        # PRJ info: imports image, prj data entry, and uses the build and single shot operations.

        # Elements for panel1
        dimension_buttons = DimensionButtons()
        spacial_inputs = SpacialInformation()
        radar_stuff = Radar()
        seismic_stuff = Seismic()
        run_button = SingleRunButton()

        # Adding elements to panel1 layout
        panel1_layout.add_widget(image_input)
        panel1_layout.add_widget(dimension_buttons)
        panel1_layout.add_widget(spacial_inputs)
        panel1_layout.add_widget(radar_stuff)
        panel1_layout.add_widget(seismic_stuff)
        panel1_layout.add_widget(run_button)

        # Assigning layout to panel1
        panel1.add_widget(panel1_layout)

        # panel2-------------------------------------------------------------
        # NEEDS NAME: Import image and Multi run

        # Elements for panel1
        multi_shot_inputs = MultiShotInput()
        run_button_2 = MultiRunButton()
       
        # Adding elements to panel2 layout
        panel2_layout.add_widget(image_input_2)
        panel2_layout.add_widget(multi_shot_inputs)
        panel2_layout.add_widget(run_button_2)

        # Assigning layout to panel2
        panel2.add_widget(panel2_layout)

        # panel3-------------------------------------------------------------
        # ______: ___________


        # panel4-------------------------------------------------------------
        # ______: ___________


        # help pannel--------------------------------------------------------
        # Help Page: Contains user manual


        # adding tabs to the window
        base.add_widget(panel1)
        base.add_widget(panel2)
        base.add_widget(panel3)
        base.add_widget(panel4)
        base.add_widget(helpPanel)

        # setting the default tab
        base.default_tab = panel1

        return base


def startGui():
    SeidarTGUI().run()
