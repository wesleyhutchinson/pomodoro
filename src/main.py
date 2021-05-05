from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.config import Config
import time

# Settings for window display
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', '0')
Config.write()

class Timer(Widget):
    focus_time, default = 1500, 1500
    rest_time = 300
    recover = 900
    sequence = ['Focus', 'Rest', 'Focus', 'Rest', 'Focus', 'Rest', 'Focus', 'Recover']
    cycle = 0
    phase = "Focus"
    pomo_count = 1
    timer_On = False
    timer_alarm = SoundLoader.load('resources/alert.mp3')

    def __init__(self, **kwargs):
        super(Timer, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    #Function to convert time into minutes and seconds
    def time_convert(self):
        self.minutes, self.seconds = divmod(self.focus_time, 60)
        return str("%d:%02d" %(self.minutes, self.seconds))

    #Function to start timer
    def start_timer(self):
        self.timer_On = True

    #Function to stop timer
    def stop_timer(self):
        self.timer_On = False

    # Restore timer to default settings
    def reset_timer(self):
        self.cycle = 0
        self.pomo_count = 1
        self.timer_On = False
        self.focus_time = self.default

    # Checks for number of completed cycles
    def check_cycle(self):
        if self.cycle < 7:
            self.cycle += 1
        else:
            self.cycle = 0
        self.setup()
    
    def setColor(self, state):
        color = [0.88, 0.47, 0.0, 1]
        if state == "Rest":
            color = [0.07, 0.31, 0.95, 1]
        self.displayLabel.color = color
        self.statusLabel.color = color
        self.cycleLabel.color = color

    # Determines if the "Status" of the timer
    def setup(self):
        self.statusLabel.text = str(self.sequence[self.cycle])
        if self.sequence[self.cycle] == 'Focus':
            self.focus_time = self.default
            self.pomo_count += 1
            if self.pomo_count == 4:
                self.pomo_count = 0
            self.cycleLabel.text = 'Focus Cycle: ' + str(self.pomo_count)
            self.setColor("Focus")
            self.phase = "Focus"
            self.start_timer()
        elif self.sequence[self.cycle] == 'Rest':
            self.cycleLabel.text = 'Completed Focus: ' + str(self.pomo_count)
            self.focus_time = self.rest_time
            self.setColor("Rest")
            self.phase = "Rest"
            self.start_timer()
        else:
            self.cycleLabel.text = 'Completed Four Focus Cylces'
            self.focus_time = self.recover
            self.setColor("Rest")
            self.phase = "Rest"
        
        if self.timer_On is False:
            self.btn_default()
            self.other_btn()
        else:
            self.pause_default()
            self.other_btn()

    # Default style of the Pause Button
    def pause_default(self):
        if self.phase == "Rest":
            self.main_btn.background_normal = './resources/pause-rest.png'
            self.main_btn.background_down = './resources/pause-rest.png'
        else:
            self.main_btn.background_normal = './resources/pause.png'
            self.main_btn.background_down = './resources/pause.png'

    # Default style of Buttons
    def btn_default(self):
        if self.phase == "Rest":
            self.main_btn.background_normal = './resources/play-rest.png'
            self.main_btn.background_down = './resources/play-rest.png'  
        else:
            self.main_btn.background_normal = './resources/play.png'
            self.main_btn.background_down = './resources/play.png'

    
    def other_btn(self):
        if self.phase == "Rest":
            self.skip.background_normal = './resources/skip-rest.png'
            self.skip.background_down = './resources/skip-rest.png'
            self.reset.background_normal = './resources/reset-rest.png'
            self.reset.background_down = './resources/reset-rest.png' 
            self.reset.background_disabled_normal: './resources/reset-rest-disabled.png'   
        else:
            self.skip.background_normal = './resources/skip.png'
            self.skip.background_down = './resources/skip.png'
            self.reset.background_normal = './resources/reset.png'
            self.reset.background_down = './resources/reset.png' 
            self.reset.background_disabled_normal: './resources/reset-disabled.png'

    # Start/Pause Button
    def start_button(self):
        if self.timer_On:
            self.btn_default()
            self.other_btn()
            self.stop_timer()
        else:
            self.pause_default()
            self.other_btn()
            self.start_timer()

    # Button to skip to next cycle
    def break_button(self):
        self.timer_On = True
        self.check_cycle()

    # Button to reset all timer values back to default
    def reset_button(self):
        self.reset.disabled = True
        self.reset_timer()
        self.displayLabel.text = str(self.time_convert())
        self.cycleLabel.text = "Focus Cycle 1"
        self.statusLabel.text = "Focus"
        self.btn_default()

    def update(self, *args, **kwargs):
        if self.timer_On and self.focus_time > 0:
            self.reset.disabled = False
            self.focus_time -= 1
            self.displayLabel.text = self.time_convert()
            self.displayLabel.font_size = "120"     
        elif self.timer_On and self.focus_time > -2:
            self.focus_time -= 1
            if self.focus_time == -1:
                self.timer_alarm.play()
            self.displayLabel.text = "Cycle Completed"
            self.displayLabel.font_size = "50"           
        elif self.focus_time == -2:
            self.timer_On = False
            self.check_cycle()
            self.displayLabel.text = self.time_convert()
            self.displayLabel.font_size = "120"                   

class PomoApp(App):
    def build(self):
        return Timer()

if __name__ == '__main__':
    PomoApp().run()