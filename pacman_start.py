import pygame
import sys
import menu

pygame.init()
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'


class TextBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = pygame.font.Font("gothic.ttf", 100)
        self.image = self.font.render("Enter your name", False, [105, 0, 21])
        self.rect = self.image.get_rect()

    def add_chr(self, char):
        global shiftDown
        if char in validChars and not shiftDown:
            self.text += char
        elif char in validChars and shiftDown:
            self.text += shiftChars[validChars.index(char)]
        self.update()

    def update(self):
        old_rect_pos = self.rect.center
        self.image = self.font.render(self.text, False, [105, 0, 21])
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos


screen = pygame.display.set_mode([800, 800])
textBox = TextBox()
shiftDown = False
textBox.rect.center = [400, 400]


running = True
while running:
    screen.fill([0, 0, 0])
    screen.blit(textBox.image, textBox.rect)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYUP:
            if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                shiftDown = False
        if e.type == pygame.KEYDOWN:
            textBox.add_chr(pygame.key.name(e.key))
            if e.key == pygame.K_SPACE:
                textBox.text += " "
                textBox.update()
            if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                shiftDown = True
            if e.key == pygame.K_BACKSPACE:
                textBox.text = textBox.text[:-1]
                textBox.update()
            if e.key == pygame.K_RETURN:
                if len(textBox.text) > 0:
                    running = False
                else:
                    old_rect_pos = textBox.rect.center
                    textBox.image = textBox.font.render("Enter your name", False, [105, 0, 21])
                    textBox.rect = textBox.image.get_rect()
                    textBox.rect.center = old_rect_pos

name = textBox.text
menu.mainloop(name)
