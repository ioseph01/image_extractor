from PIL import Image
import os
import pygame
import utils
import sys

RENDER_SCALE = 2.0



# TODO:
# Create Folder 
# Select Folder
# Auto Name 
# Render Past Selections on the Proper Screen, it is static when trying to move


class Editor:
    
    def __init__(self, fileName, tile_size=16):

        self.dim = Image.open(fileName).size
        
        pygame.init()
        pygame.display.set_caption("Editor")
        self.screen = pygame.display.set_mode((self.dim[0] * 8, self.dim[1] * 8))
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface(self.dim)
        self.fileName = fileName
        
        
        self.movement = [False, False, False, False]
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', self.dim[0] // 10)
        self.background = utils.load_image(fileName)
        
        
        self.scroll = [0,0]
        self.tile_size = tile_size
        self.background = pygame.transform.scale(utils.load_image(fileName), self.dim)
        
        self.screen2 = pygame.Surface(self.dim)
        
        self.selecting = False
        self.click_history = [(0,0), (0,0)]
        
        self.selection_history = []
        
        self.folder_button = (self.dim[0] * 8 - 69 - 10,0,32, 32)
        self.save_button = (self.dim[0] * 8 - 32 - 10,0,32, 32)
        self.selection_size = [0,0]

    def text(self, x, y, z=0):
        return self.my_font.render(f'({x}, {y}, {z})', False, (255,255,255))
        

    


    
    def run(self):
        while True:
            
            self.display.fill((0,0,0))
            self.scroll[0] -= (self.movement[1] - self.movement[0])
            self.scroll[1] -= (self.movement[3] - self.movement[2])

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))            
            self.display.blit(self.background, (self.scroll))

            mpos = pygame.mouse.get_pos()
            tile_pos = (int((mpos[0] + self.scroll[0])), int((mpos[1] + self.scroll[1]) ))
            
            # pygame.draw.rect(self.display, (255,0,0), pygame.Rect(tile_pos[0] // 8, tile_pos[1] // 8, 1,1))
  
            if self.shift:
                for rect in self.selection_history:
                    print(self.scroll)
                    r = ((rect[0] + self.scroll[0]), (rect[1] + self.scroll[1]), abs(rect[2] - rect[0]), abs(rect[3] - rect[1]))
                    pygame.draw.rect(self.display, (0,255,0), r, 1)
            
            if self.selecting:
                
                self.click_history[1] = (mpos[0] // 8, mpos[1] // 8)
                temp = [(min(self.click_history[0][0], self.click_history[1][0]), min(self.click_history[0][1], self.click_history[1][1])), (max(self.click_history[0][0], self.click_history[1][0]), max(self.click_history[0][1], self.click_history[1][1]))]
                
                pygame.draw.rect(self.display, (255,0,0), (*temp[0],  (temp[1][0] - temp[0][0]), (temp[1][1] - temp[0][1]) ), 1)
                self.selection_size = [temp[1][1] - temp[0][1], temp[1][0] - temp[0][0]]        
                self.display.blit(self.my_font.render(f'{max(self.selection_size[0] - 2, 0)} x {max(0,self.selection_size[1] - 2)}', False, (255,255,255)), (0, self.dim[0] // 10))
    
            
            self.display.blit(self.text(*tile_pos), (0, 0))


            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        
                        if not self.selecting:
                            self.click_history[0] = (mpos[0] // 8, mpos[1] // 8)
                            self.selecting = not self.selecting
                        
                        elif abs(self.click_history[0][0] - self.click_history[1][0]) > 2 and abs(self.click_history[0][1] - self.click_history[1][1]) > 2:
                            print(self.click_history)
                            im = Image.open(self.fileName)
                            print(self.click_history)
                            self.click_history = [(min(self.click_history[0][0], self.click_history[1][0]), min(self.click_history[0][1], self.click_history[1][1])), (max(self.click_history[0][0], self.click_history[1][0]), max(self.click_history[0][1], self.click_history[1][1]))]
                
                            im_crop = im.copy().crop((self.click_history[0][0] + 1, self.click_history[0][1] + 1,  self.click_history[1][0] - 1, self.click_history[1][1] - 1))
                            im_crop.save("C:/Users/Administrator/Documents/port/cropped.png", format="PNG")
                            
                            entry = [ (self.click_history[0][0] - self.scroll[0], self.click_history[0][1] - self.scroll[1]),  (self.click_history[1][0] - self.scroll[0], self.click_history[1][1] - self.scroll[1]) ]
                            entry.sort()
                            print(entry)
                            self.selection_history += [(*entry[0], *entry[1])]
                            self.selecting = not self.selecting
                        # if not self.ongrid:
                        #     self.tilemap.offgrid_tiles.append({'type':self.tile_list[self.tile_group], 'variant':self.tile_variant,'pos':(mpos[0] + self.scroll[0], mpos[1] + self.scroll[1], self.z)})
                    if event.button == 3:
                        self.selecting = False
                        self.right_clicking = True
                    # if self.shift:
                    #     if event.button == 4 or pygame.key == pygame.K_UP:
                    #         self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                    #     if event.button == 5:
                    #         self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    # else:
                    # if event.button == 4:
                    #     self.scale += .1
                    #     # self.tile_variant = 0
                    # if event.button == 5:
                    #     self.scale = max(self.scale - .1, .001)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button ==  3:
                        self.right_clicking = False
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = not self.shift
                    # if event.key == pygame.K_g:
                    #     self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_f:
                        self.z = max(-10, self.z - 1)
                    if event.key == pygame.K_r:
                        self.z += 1
                    # if self.shift and event.key == pygame.K_UP:
                    #     self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    # elif event.key == pygame.K_UP:
                    #     self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                 
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            
            pygame.draw.rect(self.screen, (0,0,255), self.folder_button)
            pygame.draw.rect(self.screen, (0,255,255), self.save_button)
            pygame.display.update()
            self.clock.tick(60)
    


game = Editor("sprites.png", 8)
game.run()


        
