from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import PySimpleGUI as simpleGUI
import re
from PIL import Image
# from anticaptchaofficial.imagecaptcha import imagecaptcha

captcha_svgFile = './captcha/captcha.svg'
captcha_pngFile = './captcha/captcha.png'
captcha_gifFile = './captcha/captcha.gif'

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
    window.TKroot.focus_force()         # focus on window
    window.Element('input').SetFocus()    # focus on field
    event, values = window.read()
    window.close()
    return values['input']