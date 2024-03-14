from tkinter import filedialog
import pygame,sys,os
import pygame.gfxdraw

# it's better when you go fullscreen
pygame.init()
width, height = 640,480

pygame.display.set_caption("File hex viewer")
display = pygame.display.set_mode((width,height),pygame.RESIZABLE)

array = []

def file_dialog():
    global array, open_file
    open_file = filedialog.askopenfilename(defaultextension='*.*', title="Open")

    with open(open_file, 'rb') as file:     # getting hex value from the file
        array = list(map(''.join, zip(*[iter(file.read().hex())]*2)))

file_dialog()

clock = pygame.time.Clock()


# square surface
class Square:
    def __init__(self, color, column, row):
        self.image = pygame.surface.Surface((20,20))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = column * 20
        self.rect.y = row * 20
        pygame.draw.rect(display, color, (self.rect.x, self.rect.y, 20, 20))
        self.handle_event()
    
    def handle_event(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse[0], mouse[1]):
            data_text = pygame.font.SysFont('Courier', 20).render(f"      {self.color}\n      {tuple(hex(i) for i in self.color)}", True, (255,255,255))
            display.blit(data_text, (pygame.display.get_window_size()[0]-770, 200))

# open file button
open_button_rect = pygame.Rect(pygame.display.get_window_size()[0]+520,320,60,30)
open_button_text = pygame.font.SysFont('Courier', 15).render("Open", True, (255,255,255))

run = True    
y = 0


# main loop
while run:
    display.fill((0,0,0))

    mouse = pygame.mouse.get_pos()
    
    # ignore this, this is just some text you can see on the right side of the window
    size_text = pygame.font.SysFont('Courier', 20).render(f"Size: {str(os.path.getsize(open_file))} Bytes", True, (255,255,255))
    filename_text = pygame.font.SysFont('Courier',20).render(f"File: {str(open_file)}", True, (255,255,255))

    display.blit(size_text, (pygame.display.get_window_size()[0]-770, 70))
    display.blit(filename_text, (pygame.display.get_window_size()[0]-770, 20))
    display.blit(open_button_text, (pygame.display.get_window_size()[0]-428,325))

    pygame.gfxdraw.rectangle(display, open_button_rect, (255,255,255))

    if pygame.display.get_window_size() != (width,height):
        pygame.gfxdraw.vline(display, pygame.display.get_window_size()[0]-800, pygame.display.get_window_size()[1], 0, (255,255,255))
    else:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                y += 5
            if event.button == 4:
                y -= 5

        if open_button_rect.collidepoint(mouse[0],mouse[1]) and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                file_dialog()

    for i, color in enumerate(zip(*[iter(array)]*3)):
        row = i // (width // 20) - y
        column = i % (width // 20)
        Square(tuple(int(i, 16) for i in color), column, row)


    clock.tick(60)
    pygame.display.flip()
