import random

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.popup import Popup
from kivy.lang import Builder

result_num1, result_num2, result_num3 = random.sample(range(0, 5), 3)
code_dg1 = random.randint(1, 8)
code_dg2 = random.randint(1, 8)
code_dg3 = random.randint(1, 8)
code = str(code_dg1) + str(code_dg2) + str(code_dg3)

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()

class ErrorPopupWindow(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.size_hint = (.4, .4)
        self.title = "Wrong Input"

        grid = GridLayout(cols=1)
        grid.add_widget(Label(text='The code has 3 digits.', font_size=18))
        grid.add_widget(Label(text='Please enter again.', font_size=18))
        btn = Button(text="OK", font_size=18)
        btn.bind(on_press=self.dismiss)
        grid.add_widget(btn)
        self.add_widget(grid)

class PopupWindow(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.size_hint = (.4, .4)

        grid = GridLayout(cols=1)
        grid.add_widget(Label(text='Wrong code', font_size=18))
        grid.add_widget(Label(text=f'remaining chance(s): {3-decode_app.try_times}'))
        btn = Button(text="Try Again", font_size=18)
        btn.bind(on_press=self.again_button)
        grid.add_widget(btn)
        self.add_widget(grid)

    def again_button(self, instance):
        self.dismiss()
        if decode_app.try_times == 1:
            decode_app.add_game1_page()
        else:
            decode_app.add_game2_page()
        screen_manager.switch_to(screens[decode_app.try_times+4])

class MenuPage(Screen):
    def start_button(self):
        decode_app.try_times = 0
        screen_manager.switch_to(screens[1])

    def quit_button(self):
        decode_app.get_running_app().stop()


class RulePage(Screen):
    def button(self):
        screen_manager.switch_to(screens[4])


class GamePage0(Screen):
    def get_img1_path(self, c):
        if c==1:
            return 'results/'+str(result_num1)+'/'+str(code_dg1)+'.png'
        return 'results/' + str(result_num1) + '/' + str(c) + '.png'

    def get_img2_path(self, c):
        if c==2:
            return 'results/'+str(result_num2)+'/'+str(code_dg2)+'.png'
        return 'results/' + str(result_num2) + '/' + str(c) + '.png'

    def get_img3_path(self, c):
        if c==3:
            return 'results/'+str(result_num3)+'/'+str(code_dg3)+'.png'
        return 'results/' + str(result_num3) + '/' + str(c) + '.png'

    def submit_button(self):
        new_code = self.ids.new_code.text
        if len(new_code) != 3 or not new_code.isdigit(): # check validity
            popup = ErrorPopupWindow()
            popup.open()
            self.ids.new_code.text = ''
        elif new_code == code:
            screen_manager.switch_to(screens[2])
        else:
            decode_app.try_times += 1
            decode_app.prev_code = new_code
            popup = PopupWindow()
            popup.open()

class GamePage1(Screen):
    def show_prev_input(self):
        return decode_app.prev_code

    def get_img1_path(self, c):
        prev_code1 = int(decode_app.prev_code[0])
        if c==1:
            return 'results/'+str(result_num1)+'/'+str(code_dg1)+'.png'
        if c < prev_code1 < code_dg1 or code_dg1 < prev_code1 < c:
            return 'results/' + str(result_num1) + '/' + str(prev_code1) + '.png'
        return 'results/' + str(result_num1) + '/' + str(c) + '.png'
    def get_img2_path(self, c):
        prev_code2 = int(decode_app.prev_code[1])
        if c==2:
            return 'results/'+str(result_num2)+'/'+str(code_dg2)+'.png'
        if c < prev_code2 < code_dg2 or code_dg2 < prev_code2 < c:
            return 'results/' + str(result_num2) + '/' + str(prev_code2) + '.png'
        return 'results/' + str(result_num2) + '/' + str(c) + '.png'
    def get_img3_path(self, c):
        prev_code3 = int(decode_app.prev_code[2])
        if c==3:
            return 'results/'+str(result_num3)+'/'+str(code_dg3)+'.png'
        if c < prev_code3 < code_dg3 or code_dg3 < prev_code3 < c:
            return 'results/' + str(result_num3) + '/' + str(prev_code3) + '.png'
        return 'results/' + str(result_num3) + '/' + str(c) + '.png'

    def get_lab1_text(self, c):
        prev_code1 = decode_app.prev_code[0]
        if c < prev_code1 < str(code_dg1) or str(code_dg1) < prev_code1 < c:
            return prev_code1
        return c
    def get_lab2_text(self, c):
        prev_code2 = decode_app.prev_code[1]
        if c < prev_code2 < str(code_dg2) or str(code_dg2) < prev_code2 < c:
            return prev_code2
        return c
    def get_lab3_text(self, c):
        prev_code3 = decode_app.prev_code[2]
        if c < prev_code3 < str(code_dg3) or str(code_dg3) < prev_code3 < c:
            return prev_code3
        return c

    def submit_button(self):
        new_code = self.ids.new_code.text
        if len(new_code) != 3 or not new_code.isdigit(): # check validity
            popup = ErrorPopupWindow()
            popup.open()
            self.ids.new_code.text = ''
        elif new_code == code:
            screen_manager.switch_to(screens[2])
        else:
            decode_app.try_times += 1
            decode_app.prev_code = new_code
            popup = PopupWindow()
            popup.open()

class GamePage2(Screen):
    def show_prev_input(self):
        return decode_app.prev_code

    def get_img1_path(self, c):
        prev_code1 = int(decode_app.prev_code[0])
        if c==1:
            return 'results/'+str(result_num1)+'/'+str(code_dg1)+'.png'
        if c < prev_code1 < code_dg1 or code_dg1 < prev_code1 < c:
            return 'results/' + str(result_num1) + '/' + str(prev_code1) + '.png'
        return 'results/' + str(result_num1) + '/' + str(c) + '.png'
    def get_img2_path(self, c):
        prev_code2 = int(decode_app.prev_code[1])
        if c==2:
            return 'results/'+str(result_num2)+'/'+str(code_dg2)+'.png'
        if c < prev_code2 < code_dg2 or code_dg2 < prev_code2 < c:
            return 'results/' + str(result_num2) + '/' + str(prev_code2) + '.png'
        return 'results/' + str(result_num2) + '/' + str(c) + '.png'
    def get_img3_path(self, c):
        prev_code3 = int(decode_app.prev_code[2])
        if c==3:
            return 'results/'+str(result_num3)+'/'+str(code_dg3)+'.png'
        if c < prev_code3 < code_dg3 or code_dg3 < prev_code3 < c:
            return 'results/' + str(result_num3) + '/' + str(prev_code3) + '.png'
        return 'results/' + str(result_num3) + '/' + str(c) + '.png'

    def get_lab1_text(self, c):
        prev_code1 = decode_app.prev_code[0]
        if c < prev_code1 < str(code_dg1) or str(code_dg1) < prev_code1 < c:
            return prev_code1
        return c
    def get_lab2_text(self, c):
        prev_code2 = decode_app.prev_code[1]
        if c < prev_code2 < str(code_dg2) or str(code_dg2) < prev_code2 < c:
            return prev_code2
        return c
    def get_lab3_text(self, c):
        prev_code3 = decode_app.prev_code[2]
        if c < prev_code3 < str(code_dg3) or str(code_dg3) < prev_code3 < c:
            return prev_code3
        return c

    def submit_button(self):
        new_code = self.ids.new_code.text
        if len(new_code) != 3 or not new_code.isdigit(): # check validity
            popup = ErrorPopupWindow()
            popup.open()
            self.ids.new_code.text = ''
        elif new_code == code:
            screen_manager.switch_to(screens[2])
        else:
            screen_manager.switch_to(screens[3])

class SuccessPage(Screen):
    def quit_button(self):
        decode_app.get_running_app().stop()

class FailPage(Screen):
    def show_code(self):
        return "The code is " + code + "."
    def quit_button(self):
        decode_app.get_running_app().stop()


kv = Builder.load_file("style.kv")
screen_manager = WindowManager()

screens = [MenuPage(name="Menu"), RulePage(name="Rule"), SuccessPage(name="Success"), FailPage(name="Fail"),
           GamePage0(name="Game0")]
for screen in screens:
    screen_manager.add_widget(screen)

screen_manager.current = "Menu"


class DecodeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.try_times = 0 # 0-success; 1-try once; 2-try twice; 3-fail
        self.prev_code = ''

    def build(self):
        return screen_manager

    def add_game1_page(self):
        screens.append(GamePage1(name="Game1"))
        screen_manager.add_widget(screens[5])

    def add_game2_page(self):
        screens.append(GamePage2(name="Game2"))
        screen_manager.add_widget(screens[6])

if __name__ == "__main__":
    decode_app = DecodeApp()
    decode_app.run()