import kivy, sys
import os
import re

kivy.require('1.11.1')

sys.path.append("../")
import exe


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
        for i in self.parent.children:
            if i.name == "material_window":
                for j in i.children:
                    if j.name == "material_box":
                        for k in reversed(j.children):
                            #i.file_name

                            #find the first instance of an empty slot
                            
                            #split that line on ","
                            #construct the material

                            #replace the first
                            f  = open(i.file_name, "r+")
                            text = f.read()
                            
                            temp = re.findall("M.*,,,,,,,", text)[0]
                            text = re.sub("M.*,,,,,,,", k.text, text, count = 1)

                            f.seek(0)
                            #Update this so it writes the proper material information
                            f.write(text)
                            f.truncate()


class MaterialInput(TextInput):
    pass

class TotalLayout(TabbedPanel):
    def __init__(self, **kwargs):
        super(TotalLayout, self).__init__(**kwargs)

class ImageInput(RelativeLayout):
    def __init__(self, **kwargs):
        super(ImageInput, self).__init__(**kwargs)

        self.box_layout = None
        self.image = None

    def getImage(self):
        #This allows for multiple images
        if self.image:
            self.remove_widget(self.image)

        file_name = self.ids['file_path'].text

        self.image = GlacierImage()
        self.image.source = file_name + ".png"
        self.add_widget(self.image)

        #prjbuild -i /path/to/geometry/image.png -o project_filename.prj

        #find a way to call prjbuild
        command = "python3 ../exe/prjbuild.py -i" + file_name + ".png -o " + file_name + ".prj"
        os.system(command)

        prj = open(file_name + ".prj", 'r')
        contents = prj.read()
        
        #Fix multiple image inputing stuff
        material_count = len(re.findall("M,", contents))
        material_scrollview = MaterialWindow()
        material_scrollview.file_name = file_name + ".prj"

        if  self.box_layout:
            for i in self.box_layout:
                pass
                #delete all of the "i"s
            self.box_layout.height = 0
            
        else:
            self.box_layout = MaterialBox(orientation = 'vertical', size_hint_y= None, height =0)

        for i in range(material_count):
            #Replace this with a row for a material
            #Create a new "structure" in the KV file for a row, given the color from the .prj
            self.box_layout.add_widget(MaterialInput(hint_text = "Enter material " + str(i), height = 40, size_hint_y = None))
            self.box_layout.height += 40

        material_scrollview.add_widget(self.box_layout)

        self.parent.add_widget(material_scrollview)
        
        print (material_count)


class SeidarTGUI(App):
    def build(self):
        #base tabbed thing
        base = TotalLayout(size=(WIDTH, HEIGHT))

        panel1 = TabbedPanelItem()
        panel1.text = "test"

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

if __name__ == '__main__':
    SeidarTGUI().run()