

def lohith():
    print('happy')
    captcha = get_captcha()
    if captcha == 'None':
        captcha = get_captcha()
    print(captcha)
    if(len(captcha) == 7):
        print('happiness')


def get_captcha():
    out = input('enter value:')
    if out == '200':
        return 'working'
    else:
        return 'None'


if __name__ == '__main__':
    lohith()