import gi
import random
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# pip install selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="SIA Auto Fill")
        self.set_border_width(10)
        self._entry()
        self._initUI()
        self.array = []
    
    def _initUI(self):
        self.set_size_request(640, 360)

    def _entry(self):
        # Set The Box
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

        self.add(self.vbox) # Add The Box to MainWindow

        # Set Username Input
        self.username = Gtk.Entry()
        self.username.set_text("")
        self.vbox.pack_start(self.username, False, False, 2)

        # Make Password Input
        self.password = Gtk.Entry()
        self.password.set_text("")
        self.password.set_visibility(False)
        self.vbox.pack_start(self.password, False, False, 2)

        # Label
        self.rangeLabel = Gtk.Label("Range Penilaian. Kalian bisa memilih lebih dari satu dan akan menjadi jawaban dari penilaian di kuisioner")
        self.vbox.pack_start(self.rangeLabel, False, False, 2)

        # Make CheckBox
        self.button1 = Gtk.CheckButton(label="1")
        self.button2 = Gtk.CheckButton(label="2")
        self.button3 = Gtk.CheckButton(label="3")
        self.button4 = Gtk.CheckButton(label="4")
        self.button5 = Gtk.CheckButton(label="5")

        self.button1.connect("toggled", self._toggleButton, "1")
        self.button2.connect("toggled", self._toggleButton, "2")
        self.button3.connect("toggled", self._toggleButton, "3")
        self.button4.connect("toggled", self._toggleButton, "4")
        self.button5.connect("toggled", self._toggleButton, "5")

        self.vbox.pack_start(self.button1, False, False, 2)
        self.vbox.pack_start(self.button2, False, False, 2)
        self.vbox.pack_start(self.button3, False, False, 2)
        self.vbox.pack_start(self.button4, False, False, 2)
        self.vbox.pack_start(self.button5, False, False, 2)

        # Make Sign In Button
        self.signInButton = Gtk.Button(label="Sign In")
        self.signInButton.connect("clicked", self._sign_in)

        self.vbox.pack_end(self.signInButton, False, False, 1)

    def _toggleButton(self, checkButton, value):
        if checkButton.get_active():
            self.array.append(value)
        else:
            self.array.remove(value)
        self.array.sort()
        print("List Jawaban: ", end=' ')
        for i in self.array:
            print(i, end=', ')
        print('\n')


    def _sign_in(self, widget):
        self.driver = webdriver.Chrome()

        self.driver.maximize_window()
        self.driver.get("https://sia.unmul.ac.id/home")
        self.driver.implicitly_wait(60)

        username_form = self.driver.find_element_by_id("exampleInputEmail")
        username_form.send_keys(self.username.get_text())

        password_form = self.driver.find_element_by_id("exampleInputPassword")
        password_form.send_keys(self.password.get_text())

        code_text = self.driver.find_element_by_css_selector("div.form-group:nth-child(3) > div:nth-child(1)").text

        security_code_form = self.driver.find_element_by_css_selector("div.form-group:nth-child(4) > input:nth-child(1)")
        security_code_form.send_keys(code_text)

        sign_button = self.driver.find_elements_by_xpath("/html/body/div/div/div/div/div/form/div[5]/button")[0]
        sign_button.click()

        print("\nBerhasil Login!!!")

        self._after_login()

    def _after_login(self):
        self.action = ActionChains(self.driver)
        
        hasil_studi = self.driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div/ul/li[4]")
        self.action.move_to_element(hasil_studi).click(hasil_studi).perform()

        khs         = self.driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div/ul/li[4]/ul/li")
        self.action.move_to_element(khs).click(khs).perform()

        self._khs_pages()


    def _khs_pages(self):
        self.action = ActionChains(self.driver)

        pilih_bar = self.driver.execute_script(open("./js/khs_page.js").read())

        last = self.driver.find_element_by_partial_link_text("Kuisioner")

        print(last.text)
 
        self.action.move_to_element(last).click(last).perform()

        self._kuisioner()
        
    def _kuisioner(self):
        self.action = ActionChains(self.driver)

        allTabs = self.driver.window_handles

        for tab in allTabs:
            self.driver.switch_to.window(tab)
            print(self.driver.current_url)

        kesiapan_mengajar = self.driver.find_element_by_partial_link_text("Kesiapan Mengajar")
        kesiapan_mengajar.click()
        

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

