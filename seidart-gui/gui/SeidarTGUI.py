import exe
import kivy
import numpy as np
import os
import re
import sys

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
HEIGHT = 640
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
        # print (self.parent.name)
        file_name = ""
        for i in self.parent.children:
            if i.name == "image_input":
                file_name = i.file_name
                command = "python exe/prjbuild.py -i gui/" + i.file_name + ".png -o gui/" + i.file_name + ".prj"
                os.system(command)

        f = open("gui/" + file_name + ".prj", "r+")
        text = f.read()
        for i in self.parent.children:
            if i.name == "radar":
                radar = i.children[0]
                text = re.sub("E,time_steps,", "E,time_steps," + radar.children[6].text, text)
                text = re.sub("E,x,", "E,x," + radar.children[10].text, text)
                text = re.sub("E,y,", "E,y," + radar.children[9].text, text)
                text = re.sub("E,z,", "E,z," + radar.children[8].text, text)
                text = re.sub("E,f0,", "E,f0," + radar.children[2].text, text)
                text = re.sub("E,theta,0", "E,theta," + radar.children[4].text, text)
                text = re.sub("E,phi,0", "E,phi," + radar.children[0].text, text)
                f.seek(0)
                f.write(text)
                f.truncate()
            elif i.name == "seismic":
                seismic = i.children[0]
                text = re.sub("S,time_steps,", "S,time_steps," + seismic.children[6].text, text)
                text = re.sub("S,x,", "S,x," + seismic.children[10].text, text)
                text = re.sub("S,y,", "S,y," + seismic.children[9].text, text)
                text = re.sub("S,z,", "S,z," + seismic.children[8].text, text)
                text = re.sub("S,f0,", "S,f0," + seismic.children[2].text, text)
                text = re.sub("S,theta,0", "S,theta," + seismic.children[4].text, text)
                text = re.sub("S,phi,0", "S,phi," + seismic.children[0].text, text)
                f.seek(0)
                f.write(text)
                f.truncate()
            elif i.name == "spacial_information":
                spacial = i.children[0]
                text = re.sub("D,dx", "D,dx," + spacial.children[6].text, text)
                text = re.sub("D,dy,n/a", "D,dy," + spacial.children[5].text, text)
                text = re.sub("D,dz", "D,dz," + spacial.children[4].text, text)

            elif i.name == "material_window":
                for j in i.children:
                    if j.name == "material_box":

                        materialColors = re.findall("\d+/\d+/\d+", text)
                        for k in reversed(j.children):

                            temp = "M," + str(k.material_number) + "," + k.children[6].text + "," + materialColors[
                                k.material_number]

                            for num in range(5, 1, -1):
                                temp += "," + k.children[num].text

                            temp += ",0"

                            temp += "," + str(k.children[1].active) + ","

                            if k.children[1].active:
                                temp += k.children[0].text

                            text = re.sub("M.*,,,,,,,", temp, text, count=1)

                        f.seek(0)
                        # Update this so it writes the proper material information
                        f.write(text)
                        f.truncate()

        command = "python exe/prjrun.py " + file_name + ".prj -M b"

        os.system(command)


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

        # prjbuild -i /path/to/geometry/image.png -o project_filename.prj

        # find a way to call prjbuild
        command = "python exe/prjbuild.py -i gui/" + self.file_name + ".png -o gui/" + self.file_name + ".prj"
        os.system(command)

        prj = open("gui/" + self.file_name + ".prj", 'r')
        contents = prj.read()

        # Fix multiple image inputing stuff
        material_count = len(re.findall("M,", contents))
        self.material_scrollview = MaterialWindow()
        self.material_scrollview.file_name = self.file_name + ".prj"

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

            ###################################################################################
            # The spacing on this is too large, but decreasing it causes some rows to disappear#
            ###################################################################################
            self.box_layout.height += 80

        try:
            self.material_scrollview.add_widget(self.box_layout)
        except:
            pass

        self.parent.add_widget(self.material_scrollview)


class SeidarTGUI(App):

    def build(self):
        # base tabbed thing
        base = TotalLayout(size=(WIDTH, HEIGHT))

        panel1 = TabbedPanelItem()
        panel1.text = "PRJ Info"

        # layout for the first tab
        panel1_layout = RelativeLayout()

        # stupid stubs
        panel2, panel3, panel4, helpPanel = TabbedPanelItem(), TabbedPanelItem(), TabbedPanelItem(), TabbedPanelItem()

        helpPanel.text = "Help Page"

        # input forms
        image_input = ImageInput()
        seismic_stuff = Seismic()
        radar_stuff = Radar()
        spacial_inputs = SpacialInformation()
        dimension_buttons = DimensionButtons()
        run_button = RunButton()

        # adding widgets to the layout
        panel1_layout.add_widget(run_button)
        panel1_layout.add_widget(image_input)
        panel1_layout.add_widget(dimension_buttons)
        panel1_layout.add_widget(seismic_stuff)
        panel1_layout.add_widget(radar_stuff)
        panel1_layout.add_widget(spacial_inputs)

        # adding the layout to the tab
        panel1.add_widget(panel1_layout)

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
