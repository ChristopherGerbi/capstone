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
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

WIDTH = 800
HEIGHT= 640
MIN_HEIGHT = 480
MIN_WIDTH = 600

Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)
Config.set('graphics', 'minimum_width', MIN_WIDTH)
Config.set('graphics', 'minimum_height', MIN_HEIGHT)

Window.clearcolor = (.7, .7, .7, 1)

class SeismicRadarTabs(TabbedPanel):
    pass

class SpacialInformation(RelativeLayout):
    pass

class DimensionButtons(RelativeLayout):
    pass

class GlacierImage(Image):
    pass

class MaterialWindow(ScrollView):
    pass

#This is an exercise in my ability to push stuff to the repo.

class ImageInput(RelativeLayout):
    def __init__(self, **kwargs):
        super(ImageInput, self).__init__(**kwargs)

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
        
        material_count = len(re.findall("M,", contents))
        material_scrollview = MaterialWindow()
        box_layout = BoxLayout(orientation = 'vertical', size_hint_y= None, height =0)

        for i in range(material_count):
            #Replace this with a row for a material
            #Create a new "structure" in the KV file for a row, given the color from the .prj
            box_layout.add_widget(TextInput(hint_text = "M"+str(i), height = 30, size_hint_y = None))
            box_layout.height += 30

        material_scrollview.add_widget(box_layout)

        app = App.get_running_app()
        app.root.add_widget(material_scrollview)

        print (material_count)



class SeidarTGUI(App):
    def build(self):
        layout = RelativeLayout(size=(WIDTH, HEIGHT))

        image_input = ImageInput()        
        seismic_radar_tabbed_panel = SeismicRadarTabs()
        spacial_inputs = SpacialInformation()
        dimension_buttons = DimensionButtons()

        layout.add_widget(image_input)
        layout.add_widget(dimension_buttons)
        layout.add_widget(seismic_radar_tabbed_panel)
        layout.add_widget(spacial_inputs)
        return layout

if __name__ == '__main__':
    SeidarTGUI().run()