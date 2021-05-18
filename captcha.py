from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import PySimpleGUI as simpleGUI
import re
from PIL import Image
from anticaptchaofficial.imagecaptcha import *

API_KEY = 'ec149064d7188f1f5d75bec750b5c15d'

captcha_svgFile = './captcha/captcha.svg'
captcha_pngFile = './captcha/captcha.png'
captcha_gifFile = './captcha/captcha.gif'

captcha_svg = './captcha/captcha.svg'
captcha_png = './captcha/captcha.png'


def captcha_builder(resp):
    with open(captcha_svgFile, 'w') as f:
        f.write(re.sub('(<path d=)(.*?)(fill="none"/>)', '', resp['captcha']))

    drawing = svg2rlg(captcha_svgFile)
    renderPM.drawToFile(drawing, captcha_pngFile, fmt="PNG")

    im = Image.open(captcha_pngFile)
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
    im.save(captcha_gifFile)

    layout = [[simpleGUI.Image(captcha_gifFile)],
              [simpleGUI.Text("Enter Captcha Below")],
              [simpleGUI.Input(key='input')],
              [simpleGUI.Button('Submit', bind_return_key=True)]]

    window = simpleGUI.Window('Enter Captcha', layout, finalize=True)
    window.TKroot.focus_force()  # focus on window
    window.Element('input').SetFocus()  # focus on field
    event, values = window.read()
    window.close()
    return values['input']


def captcha_builder_auto(resp):
    with open('./captcha/captcha.svg', 'w') as f:
        f.write(re.sub('(<path d=)(.*?)(fill=\"none\"/>)', '', resp['captcha']))

    drawing = svg2rlg('./captcha/captcha.svg')
    renderPM.drawToFile(drawing, "./captcha/captcha.png", fmt="PNG")

    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(API_KEY)
    captcha_text = solver.solve_and_return_solution("./captcha/captcha.png")

    if captcha_text != 0:
        print(f"Captcha text: {captcha_text}")
    else:
        print(f"Task finished with error: {solver.error_code}")

    return captcha_text
