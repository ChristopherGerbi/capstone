import kivy, sys
import os
import re
import exe
import numpy as np

kivy.require('1.11.1')

sys.path.append("../")

MATERIALS = None

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

temp = TabbedPanelItem()

WIDTH = 800
HEIGHT= 640
MIN_HEIGHT = 480
MIN_WIDTH = 600

Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)
Config.set('graphics', 'minimum_width', MIN_WIDTH)
Config.set('graphics', 'minimum_height', MIN_HEIGHT)

Window.clearcolor = (.7, .7, .7, 1)

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

        self.file_name = ""

class RunButton(Button):
    def __init__(self, **kwargs):
        super(RunButton, self).__init__(**kwargs)

    def run(self):
        #print (self.parent.name)
        file_name = ""
        for i in self.parent.children:
            if i.name == "image_input":
                file_name = i.file_name
                command = "python exe/prjbuild.py -i gui/" + i.file_name + ".png -o gui/" + i.file_name + ".prj"
                os.system(command)


        f = open("gui/"+file_name +".prj", "r+")
        text = f.read()
        for i in self.parent.children:
            if i.name == "radar":
                radar = i.children[0] 
            elif i.name == "seismic":
                seismic = i.children[0]
            elif i.name == "spacial_information":
                pass
            elif i.name == "material_window":
                for j in i.children:
                    if j.name == "material_box":
                        
                        materialColors = re.findall("\d+/\d+/\d+", text)
                        print (materialColors)
                        for k in reversed(j.children):
                            """
                            #i.file_name

                            #find the first instance of an empty slot
                            
                            #split that line on ","
                            #construct the material

                            #replace the first
                            f  = open("gui/"+i.file_name, "r+")
                            text = f.read()
                            
                            temp = re.findall("M.*,,,,,,,", text)[0]
                            text = re.sub("M.*,,,,,,,", k.text, text, count = 1)

                            """
                            
                            temp = "M," + str(k.material_number) + "," + k.children[6].text + "," + materialColors[k.material_number]

                            for num in range(5,1, -1):
                                temp += "," + k.children[num].text

                            temp += ",0"

                            temp += "," + str(k.children[1].active) + ","

                            if k.children[1].active:
                                temp+= k.children[0].text

                            text = re.sub("M.*,,,,,,,",temp, text, count=1)

                        f.seek(0)
                        #Update this so it writes the proper material information
                        f.write(text)
                        f.truncate()

        # command = "python exe/prjbuild.py -i gui/" + self.file_name + ".png -o gui/" + self.file_name + ".prj"
        command = "python exe/prjrun.py " +file_name + ".prj -M b"
        print (command)

        ####################
        #uncomment this when run method finalized
        #os.system(command)
                            

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

        self.box_layout = None
        self.image = None
        self.material_scrollview = None
        self.file_name = ""

    def getImage(self):

        if self.image:
            self.parent.remove_widget(self.material_scrollview)
            self.material_scrollview = None
            self.box_layout = None


        self.file_name = self.ids['file_path'].text

        self.image = GlacierImage()
        self.image.source = "gui/" + self.file_name + ".png"

        self.add_widget(self.image)

        #prjbuild -i /path/to/geometry/image.png -o project_filename.prj

        #find a way to call prjbuild
        command = "python exe/prjbuild.py -i gui/" + self.file_name + ".png -o gui/" + self.file_name + ".prj"
        os.system(command)

        prj = open("gui/" + self.file_name + ".prj", 'r')
        contents = prj.read()
        
        #Fix multiple image inputing stuff
        material_count = len(re.findall("M,", contents))
        print (material_count)
        self.material_scrollview = MaterialWindow()
        self.material_scrollview.file_name = self.file_name + ".prj"

        self.box_layout = MaterialBox(spacing = 60, orientation = 'vertical', size_hint_y= None, height =0)

        #Acquire the colors from the prj
        colors = re.findall(",,.*/.*/.*,", contents)
        colorsKivy = []
        for i in range(len(colors)):
            colors[i] = colors[i][2:]
            colors[i] = colors[i][:-7]

            colorsSplit = colors[i].split("/")

            colorsTuple = ((float(colorsSplit[0])/256),(float(colorsSplit[1])/256),(float(colorsSplit[2])/256),1)

            colorsKivy.append(colorsTuple)


        for i in range(material_count):
            #Replace this with a row for a material
            #Create a new "structure" in the KV file for a row, given the color from the .prj
            temp = MaterialInput(size_hint_y = None, height = 40)
            temp.material_number = i
            temp.color = colorsKivy[i]

            self.box_layout.add_widget(temp)
            
            ###################################################################################
            #The spacing on this is too large, but decreasing it causes some rows to disappear#
            ###################################################################################
            self.box_layout.height += 80

        try:
            self.material_scrollview.add_widget(self.box_layout)
        except:
            pass

        self.parent.add_widget(self.material_scrollview)

class SeidarTGUI(App):

    def build(self):

        #base tabbed thing
        base = TotalLayout(size=(WIDTH, HEIGHT))

        panel1 = TabbedPanelItem()
        panel1.text = "PRJ Info"

        #layout for the first tab
        panel1_layout = RelativeLayout()

        #stupid stubs
        panel2, panel3, panel4 = TabbedPanelItem(),TabbedPanelItem(),TabbedPanelItem()

        #input forms 
        image_input = ImageInput()        
        seismic_stuff = Seismic()
        radar_stuff = Radar()
        spacial_inputs = SpacialInformation()
        dimension_buttons = DimensionButtons()
        run_button = RunButton()

        #adding widgets to the layout
        panel1_layout.add_widget(run_button)
        panel1_layout.add_widget(image_input)
        panel1_layout.add_widget(dimension_buttons)
        panel1_layout.add_widget(seismic_stuff)
        panel1_layout.add_widget(radar_stuff)
        panel1_layout.add_widget(spacial_inputs)

        #adding the layout to the tab
        panel1.add_widget(panel1_layout)

        #adding tabs to the window
        base.add_widget(panel1)
        base.add_widget(panel2)
        base.add_widget(panel4)
        base.add_widget(panel3)

        #setting the default tab
        base.default_tab = panel1

        return base


def startGui():
    SeidarTGUI().run()