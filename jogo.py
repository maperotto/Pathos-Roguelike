import pgzrun
import math
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "NOX ROGUELIKE"
CELL_SIZE = 16
GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE

mode = "MENU"
level = 1
enemies = []
walls = []
floor_tiles = []
camera_x = 0
camera_y = 0
anim_frame = 0
anim_counter = 0
damage_cooldown = 0
player_hurt_flash = 0
attack_animation = 0
attack_direction = "right"
music_enabled = True
sounds_enabled = True
attack_cooldown = 0
stamina = 0
max_stamina = 300
special_attack_animation = 0
special_ready = False
stamina_flash = 0
projectiles = []
menu_selected = 0
menu_options = ["PLAY", "CONTROLS", "MUSIC", "EXIT"]
life_sound_playing = False

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 0.5
        self.lifetime = 60
        self.frame = 0
        self.damaged_enemies = set()
        
    def update(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        
        self.lifetime -= 1
        self.frame = min(60, int((60 - self.lifetime)))
        grid_x = int(self.x)
        grid_y = int(self.y)
        
        if (grid_x, grid_y) in walls:
            return False
        if self.lifetime <= 0:
            return False
        if grid_x < 0 or grid_x >= GRID_W or grid_y < 0 or grid_y >= GRID_H:
            return False
        
        for e in enemies[:]:
            if e not in self.damaged_enemies:
                dx = abs(e.x - self.x)
                dy = abs(e.y - self.y)
                dist = math.sqrt(dx * dx + dy * dy)
                if dist <= 1.5:
                    e.hp -= 200
                    self.damaged_enemies.add(e)
                    if e.is_boss:
                        e.move_cooldown = 0
                    if e.hp <= 0:
                        enemies.remove(e)
                        player.hp = min(player.max_hp, player.hp + 15)
        return True
    
    def draw(self):
        px = (self.x * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2
        py = (self.y * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
        
        frame_num = min(60, self.frame)
        if frame_num > 0:
            try:
                fireball = Actor(f"fireball_special_{frame_num}")
                fireball.center = (px, py)
                fireball.draw()
            except:
                screen.draw.filled_circle((int(px), int(py)), 15, (255, 100, 0))
                screen.draw.filled_circle((int(px), int(py)), 10, (255, 200, 0))

class Hero:
    def __init__(self):
        self.x = 3
        self.y = 3
        self.hp = 100
        self.max_hp = 100
        self.frame = 0
        self.facing = "right"
        self.moving = False
        self.attacking = False
        self.special_attacking = False
        
    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
            if (nx, ny) not in walls:
                enemy_at_pos = False
                for e in enemies:
                    if e.x == nx and e.y == ny:
                        enemy_at_pos = True
                        break
                if not enemy_at_pos:
                    self.x, self.y = nx, ny
                    self.moving = True
                    if dx > 0:
                        self.facing = "right"
                    elif dx < 0:
                        self.facing = "left"
                    elif dy < 0:
                        self.facing = "up"
                    elif dy > 0:
                        self.facing = "down"
                    return True
        return False
            
    def attack(self):
        global attack_animation, attack_direction, attack_cooldown
        if attack_cooldown > 0:
            return False
        
        attack_range = 3
        attack_direction = self.facing
        attack_animation = 15
        attack_cooldown = 30
        self.attacking = True
        
        if sounds_enabled:
            try:
                sounds.blazing_fire.play()
            except:
                pass
        
        killed_any = False
        for e in enemies[:]:
            dx = e.x - self.x
            dy = e.y - self.y
            dist = abs(dx) + abs(dy)
            
            in_direction = False
            if self.facing == "right" and dx > 0 and abs(dy) <= 1:
                in_direction = True
            elif self.facing == "left" and dx < 0 and abs(dy) <= 1:
                in_direction = True
            elif self.facing == "up" and dy < 0 and abs(dx) <= 1:
                in_direction = True
            elif self.facing == "down" and dy > 0 and abs(dx) <= 1:
                in_direction = True
            
            if dist <= attack_range and in_direction:
                e.hp -= 30
                if e.hp <= 0:
                    enemies.remove(e)
                    self.hp = min(self.max_hp, self.hp + 10)
                    killed_any = True
        return killed_any
    
    def special_attack(self):
        global special_attack_animation, attack_direction, stamina, special_ready, projectiles
        if not special_ready:
            return False
        
        attack_direction = self.facing
        special_attack_animation = 20
        self.special_attacking = True
        stamina = 0
        special_ready = False
        projectiles.append(Projectile(self.x, self.y, self.facing))
        
        if sounds_enabled:
            try:
                sounds.special_attack.play()
            except:
                pass
        return True

    def draw(self):
        if self.special_attacking and special_attack_animation > 10:
            sprite_name = "sprite_weapon_staff_atk_fire_" + str(min(4, self.frame))
        elif self.attacking and attack_animation > 10:
            sprite_name = "sprite_weapon_staff_atk_fire_" + str(min(4, self.frame))
        elif self.moving:
            sprite_name = "sprite_weapon_staff_run_" + str(self.frame)
        else:
            sprite_name = "sprite_weapon_staff_idle_" + str(self.frame)
        
        px = (self.x * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2
        py = (self.y * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
        
        actor = Actor(sprite_name)
        actor.topleft = (px, py)
        
        if player_hurt_flash > 0 and player_hurt_flash % 2 == 0:
            screen.draw.filled_rect(Rect(px, py, CELL_SIZE, CELL_SIZE), (255, 0, 0, 100))
        
        actor.draw()
        
        staff_length = 10
        center_x = px + CELL_SIZE // 2
        center_y = py + CELL_SIZE // 2
        
        if self.facing == "right":
            staff_x1 = center_x + 10
            staff_y1 = center_y - staff_length // 2
            staff_x2 = center_x + 10
            staff_y2 = center_y + staff_length // 2
        elif self.facing == "left":
            staff_x1 = center_x - 10
            staff_y1 = center_y - staff_length // 2
            staff_x2 = center_x - 10
            staff_y2 = center_y + staff_length // 2
        elif self.facing == "up":
            staff_x1 = center_x - staff_length // 2
            staff_y1 = center_y - 10
            staff_x2 = center_x + staff_length // 2
            staff_y2 = center_y - 10
        else:
            staff_x1 = center_x - staff_length // 2
            staff_y1 = center_y + 10
            staff_x2 = center_x + staff_length // 2
            staff_y2 = center_y + 10
        
        screen.draw.line((staff_x1, staff_y1), (staff_x2, staff_y2), (200, 200, 255))
        
        if attack_animation > 0:
            center_x, center_y = px + CELL_SIZE // 2, py + CELL_SIZE // 2
            
            if attack_direction == "right": attack_x, attack_y = center_x + 20, center_y
            elif attack_direction == "left": attack_x, attack_y = center_x - 20, center_y
            elif attack_direction == "up": attack_x, attack_y = center_x, center_y - 20
            else: attack_x, attack_y = center_x, center_y + 20
            
            frame_num = min(60, int((15 - attack_animation) * 4))
            if frame_num > 0:
                try:
                    fireball = Actor(f"fireball_normal_{frame_num}")
                    fireball.center = (attack_x, attack_y)
                    fireball.draw()
                except:
                    screen.draw.filled_circle((attack_x, attack_y), int(attack_animation * 1.5), (255, 100, 0))
                    screen.draw.filled_circle((attack_x, attack_y), int(attack_animation * 0.8), (255, 200, 0))

class Enemy:
    def __init__(self, x, y, enemy_type="goblin"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.frame = 0
        self.facing = "right"
        self.move_cooldown = 0
        self.has_run_anim = enemy_type in ["goblin", "chort", "orc_warrior", "masked_orc", "big_demon"]
        
        if enemy_type == "big_demon":
            self.hp = 600
            self.max_hp = 600
            self.is_boss = True
        else:
            self.hp = 80
            self.max_hp = 80
            self.is_boss = False

    def update(self):
        global damage_cooldown, player_hurt_flash
        if self.move_cooldown > 0: self.move_cooldown -= 1
        
        dist = abs(self.x - player.x) + abs(self.y - player.y)
        
        if dist < 10 and self.move_cooldown == 0:
            self.move_cooldown = 15
            dx, dy = 0, 0
            
            if player.x > self.x: dx, self.facing = 1, "right"
            elif player.x < self.x: dx, self.facing = -1, "left"
            if player.y > self.y: dy = 1
            elif player.y < self.y: dy = -1
            
            if random.randint(0, 1) == 0: nx, ny = self.x + dx, self.y
            else: nx, ny = self.x, self.y + dy
            
            if 0 <= nx < GRID_W and 0 <= ny < GRID_H and (nx, ny) not in walls:
                if not (nx == player.x and ny == player.y):
                    self.x, self.y = nx, ny
        elif self.move_cooldown == 0:
            if random.randint(0, 100) < 2:
                self.move_cooldown = 20
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                nx, ny = self.x + dx, self.y + dy
                
                if 0 <= nx < GRID_W and 0 <= ny < GRID_H and (nx, ny) not in walls:
                    if not (nx == player.x and ny == player.y):
                        self.x, self.y = nx, ny
                        if dx > 0: self.facing = "right"
                        elif dx < 0: self.facing = "left"
        
        if dist <= 1 and damage_cooldown <= 0:
            damage = 20 if self.is_boss else 10
            player.hp -= damage
            damage_cooldown = 30
            player_hurt_flash = 10
            if sounds_enabled:
                try:
                    sounds.monster_attack_sound.play()
                except:
                    pass

    def draw(self):
        if self.has_run_anim and self.move_cooldown > 0:
            sprite_name = f"{self.type}_run_anim_f{self.frame}"
        elif self.has_run_anim:
            sprite_name = f"{self.type}_idle_anim_f{self.frame}"
        else:
            sprite_name = f"{self.type}_anim_f{self.frame}"
        
        px = (self.x * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2
        py = (self.y * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
        
        actor = Actor(sprite_name)
        actor.topleft = (px, py)
        actor.draw()
        
        if self.is_boss:
            hp_percent = self.hp / self.max_hp
            draw_bar(px - 10, py - 10, 64, 6, hp_percent, "black", "purple")

player = Hero()
decorations = []
sounds_initialized = False

def init_sounds():
    global sounds_initialized
    if not sounds_initialized:
        try:
            sounds.blazing_fire.set_volume(0.3)
            sounds.special_attack.set_volume(0.4)
            sounds.monster_attack_sound.set_volume(0.3)
            sounds.death_sound.set_volume(0.5)
            sounds.life_sound.set_volume(1.0)
            music.set_volume(0.10)
            sounds_initialized = True
        except: sounds_initialized = True

def draw_bar(x, y, width, height, percent, color_bg, color_fill):
    screen.draw.filled_rect(Rect(x, y, width, height), color_bg)
    screen.draw.filled_rect(Rect(x + 2, y + 2, int((width - 4) * percent), height - 4), color_fill)
    screen.draw.rect(Rect(x, y, width, height), "white")

def reset_game():
    global mode, level, damage_cooldown, player_hurt_flash, attack_animation, attack_cooldown, special_attack_animation, stamina, special_ready, stamina_flash, projectiles, camera_x, camera_y
    level = 1
    damage_cooldown, player_hurt_flash, attack_animation, attack_cooldown = 0, 0, 0, 0
    special_attack_animation, stamina, stamina_flash = 0, 0, 0
    special_ready = False
    projectiles = []
    camera_x, camera_y = 0, 0
    player.hp = player.max_hp
    player.x, player.y = 3, 3
    setup_level(level)

def generate_dungeon():
    global floor_tiles, walls, GRID_W, GRID_H, decorations
    floor_tiles, walls, decorations = [], [], []
    GRID_W, GRID_H = int((WIDTH // CELL_SIZE) * 1.1), int((HEIGHT // CELL_SIZE) * 0.85)
    
    for y in range(GRID_H):
        for x in range(GRID_W):
            floor_tiles.append((x, y, f"floor_{random.choice([1, 2, 3])}"))
    
    for x in range(GRID_W):
        walls.append((x, 0))
        walls.append((x, GRID_H - 1))
    for y in range(GRID_H):
        walls.append((0, y))
        walls.append((GRID_W - 1, y))
    
    for _ in range(15):
        dec_x, dec_y = random.randint(6, GRID_W - 6), random.randint(2, GRID_H - 3)
        if (dec_x, dec_y) not in walls: decorations.append((dec_x, dec_y, "column"))

def setup_level(lvl):
    global enemies, player, projectiles
    enemies, projectiles = [], []
    generate_dungeon()
    player.x, player.y = 3, GRID_H // 2
    
    if lvl == 1:
        enemy_list = ["goblin"] * 4 + ["muddy"] * 2 + ["swampy"] * 2
    elif lvl == 2:
        enemy_list = ["goblin"] * 3 + ["chort"] * 4 + ["masked_orc"] * 3 + ["orc_warrior"] * 2
    else:
        enemy_list = ["goblin"] * 2 + ["chort"] * 2 + ["muddy"] * 1 + ["swampy"] * 1 + ["masked_orc"] * 2 + ["orc_warrior"] * 2
    
    for e_type in enemy_list:
        for tentativa in range(20):
            ex = random.randint(12, GRID_W - 8)
            ey = random.randint(GRID_H // 2 - 5, GRID_H // 2 + 5)
            if (ex, ey) not in walls and abs(ex - player.x) + abs(ey - player.y) > 8:
                enemies.append(Enemy(ex, ey, e_type))
                break
    
    if lvl == 3: enemies.append(Enemy(GRID_W - 6, GRID_H // 2, "big_demon"))

def draw():
    global anim_frame, anim_counter
    screen.clear()
    screen.fill((20, 12, 28))
    
    if mode == "MENU":
        screen.draw.text("NOX", center=(WIDTH//2, 120), fontsize=70, color="#8B0000")
        screen.draw.text("ROGUELIKE", center=(WIDTH//2, 180), fontsize=50, color="#A9A9A9")
        for i in range(3):
            screen.draw.filled_circle((WIDTH//2 - 200 + i*30, 230), 2, (100, 50, 50))
        
        start_y, spacing = 300, 50
        for i, option in enumerate(menu_options):
            y_pos = start_y + i * spacing
            arrow_color = (200, 0, 0) if i == menu_selected else (50, 50, 50)
            text_color = (255, 200, 200) if i == menu_selected else (150, 150, 150)
            screen.draw.text(">", (100, y_pos), fontsize=35, color=arrow_color)
            display_text = f"MUSIC: {'ON' if music_enabled else 'OFF'}" if option == "MUSIC" else option
            screen.draw.text(display_text, (140, y_pos), fontsize=35, color=text_color)
    
    elif mode == "CONTROLS":
        screen.draw.text("CONTROLS", center=(WIDTH//2, 80), fontsize=50, color="#8B0000")
        commands = [("ARROWS / WASD", "Move character"), ("SPACE", "Normal attack"), ("Q", "Special attack (when ready)"), ("ESC", "Exit game")]
        start_y = 200
        for i, (key, desc) in enumerate(commands):
            y = start_y + i * 70
            screen.draw.text(key, (150, y), fontsize=30, color="#FFD700")
            screen.draw.text(desc, (150, y + 30), fontsize=22, color="#A9A9A9")
        screen.draw.text("Press ESC to return", center=(WIDTH//2, 530), fontsize=25, color="#666666")
        
    elif mode == "GAME":
        for tx, ty, tile_name in floor_tiles:
            px, py = (tx * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2, (ty * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
            if -CELL_SIZE < px < WIDTH and -CELL_SIZE < py < HEIGHT:
                actor = Actor(tile_name); actor.topleft = (px, py); actor.draw()
        for wx, wy in walls:
            px, py = (wx * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2, (wy * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
            if -CELL_SIZE < px < WIDTH and -CELL_SIZE < py < HEIGHT:
                actor = Actor("wall_mid"); actor.topleft = (px, py); actor.draw()
        for dx, dy, dec_type in decorations:
            px, py = (dx * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2, (dy * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
            if -CELL_SIZE < px < WIDTH and -CELL_SIZE < py < HEIGHT:
                actor = Actor(dec_type); actor.topleft = (px, py); actor.draw()
        for e in enemies[:]: e.draw()
        for proj in projectiles: proj.draw()
        player.draw()
        screen.draw.text(f"Level: {level}", (10, 10), fontsize=25, color="white")
        hp_percent = player.hp / player.max_hp
        draw_bar(10, 40, 200, 20, hp_percent, "black", "green")
        screen.draw.text(f"HP: {int(player.hp)}/{player.max_hp}", (15, 43), fontsize=16, color="white")
        stamina_percent = stamina / max_stamina
        stamina_color = (0, 200, 255) if special_ready and stamina_flash % 20 < 10 else "blue"
        draw_bar(10, 65, 200, 15, stamina_percent, "black", stamina_color)
        if special_ready:
            flash_color = "yellow" if stamina_flash % 20 < 10 else "white"
            screen.draw.text("PRESS Q - SPECIAL ATTACK!", (225, 65), fontsize=20, color=flash_color)
        screen.draw.text(f"Enemies: {len(enemies)}", (10, 90), fontsize=20, color="yellow")
        
    elif mode == "WIN":
        screen.draw.text("VICTORY", center=(WIDTH//2, 150), fontsize=80, color="#FFD700")
        screen.draw.text("NOX", center=(WIDTH//2, 220), fontsize=50, color="#8B0000")
        for i in range(5): screen.draw.filled_circle((WIDTH//2 - 240 + i*120, 270), 3, (255, 215, 0))
        screen.draw.text("You conquered all dungeons!", center=(WIDTH//2, 330), fontsize=28, color="#A9A9A9")
        screen.draw.text("The kingdom is safe from darkness.", center=(WIDTH//2, 370), fontsize=22, color="#808080")
        screen.draw.text("Press R to play again", center=(WIDTH//2, 460), fontsize=25, color="#666666")
        screen.draw.text("Press ESC to exit", center=(WIDTH//2, 500), fontsize=20, color="#555555")
    
    elif mode == "GAME_OVER":
        screen.draw.text("GAME OVER", center=(WIDTH//2, 140), fontsize=70, color="#8B0000")
        for i in range(7):
            y_offset = 200 + i * 8
            alpha = 100 - i * 12
            screen.draw.line((WIDTH//2 - 250, y_offset), (WIDTH//2 + 250, y_offset), (139, 0, 0))
        screen.draw.text("Darkness has prevailed...", center=(WIDTH//2, 300), fontsize=30, color="#A9A9A9")
        screen.draw.text("† ☠ †", center=(WIDTH//2, 360), fontsize=35, color="#696969")
        screen.draw.text("Press R to try again", center=(WIDTH//2, 450), fontsize=25, color="#888888")
        screen.draw.text("Press ESC to give up", center=(WIDTH//2, 490), fontsize=20, color="#666666")

def update():
    global mode, level, camera_x, camera_y, anim_frame, anim_counter, damage_cooldown, player_hurt_flash, attack_animation, attack_cooldown, stamina, max_stamina, special_attack_animation, special_ready, stamina_flash, projectiles, life_sound_playing
    
    init_sounds()
    
    if music_enabled:
        try:
            if not music.is_playing("battle_sound"):
                music.play("battle_sound")
        except:
            pass
    else:
        try:
            music.stop()
        except:
            pass
    
    if mode == "GAME":
        hp_percent = player.hp / player.max_hp
        
        if hp_percent <= 0.3 and sounds_enabled:
            if not life_sound_playing:
                try:
                    sounds.life_sound.play(-1)
                    life_sound_playing = True
                except:
                    pass
        else:
            if life_sound_playing:
                try:
                    sounds.life_sound.stop()
                    life_sound_playing = False
                except:
                    pass
        
        if damage_cooldown > 0:
            damage_cooldown -= 1
        if player_hurt_flash > 0:
            player_hurt_flash -= 1
        if attack_animation > 0:
            attack_animation -= 1
            if attack_animation == 0:
                player.attacking = False
        
        if attack_cooldown > 0:
            attack_cooldown -= 1
        
        if special_attack_animation > 0:
            special_attack_animation -= 1
            if special_attack_animation == 0:
                player.special_attacking = False
        
        if stamina < max_stamina:
            stamina += 1
            if stamina >= max_stamina:
                special_ready = True
        
        if special_ready:
            stamina_flash += 1
        
        for proj in projectiles[:]:
            if not proj.update():
                projectiles.remove(proj)
        
        target_cam_x = player.x * CELL_SIZE
        target_cam_y = player.y * CELL_SIZE
        camera_x += (target_cam_x - camera_x) * 0.1
        camera_y += (target_cam_y - camera_y) * 0.1
        
        anim_counter += 1
        if anim_counter >= 10:
            anim_counter = 0
            anim_frame = (anim_frame + 1) % 4
            player.frame = anim_frame
            for e in enemies:
                e.frame = anim_frame
        
        player.moving = False
        
        for e in enemies[:]:
            e.update()
        
        for e in [e for e in enemies if e.hp <= 0]:
            if e in enemies:
                enemies.remove(e)
        
        if len(enemies) == 0:
            if level < 3:
                level += 1
                setup_level(level)
                player.hp = min(player.max_hp, player.hp + 30)
            else:
                mode = "WIN"
                if life_sound_playing:
                    try: sounds.life_sound.stop(); life_sound_playing = False
                    except: pass
        if player.hp <= 0:
            mode = "GAME_OVER"
            if life_sound_playing:
                try: sounds.life_sound.stop(); life_sound_playing = False
                except: pass
            if sounds_enabled:
                try: sounds.death_sound.play()
                except: pass

def on_mouse_down(pos):
    global mode, menu_selected, music_enabled
    if mode == "MENU":
        start_y = 300
        spacing = 50
        for i, option in enumerate(menu_options):
            y_pos = start_y + i * spacing
            option_rect = Rect(100, y_pos - 5, 400, 40)
            if option_rect.collidepoint(pos):
                menu_selected = i
                if menu_options[menu_selected] == "PLAY":
                    mode = "GAME"
                    reset_game()
                    if music_enabled:
                        try: music.play("battle_sound")
                        except: pass
                elif menu_options[menu_selected] == "CONTROLS": mode = "CONTROLS"
                elif menu_options[menu_selected] == "MUSIC":
                    music_enabled = not music_enabled
                    if not music_enabled:
                        try: music.stop()
                        except: pass
                    else:
                        try: music.play("battle_sound")
                        except: pass
                elif menu_options[menu_selected] == "EXIT": exit()
                break

def on_key_down(key):
    global mode, menu_selected, music_enabled
    if mode == "MENU":
        if key == keys.UP or key == keys.W:
            menu_selected = (menu_selected - 1) % len(menu_options)
        elif key == keys.DOWN or key == keys.S:
            menu_selected = (menu_selected + 1) % len(menu_options)
        
        elif key == keys.RETURN or key == keys.SPACE:
            if menu_options[menu_selected] == "PLAY":
                mode = "GAME"
                reset_game()
                if music_enabled:
                    try:
                        music.play("battle_sound")
                    except:
                        pass
            
            elif menu_options[menu_selected] == "CONTROLS":
                mode = "CONTROLS"
            
            elif menu_options[menu_selected] == "MUSIC":
                music_enabled = not music_enabled
                if not music_enabled:
                    try:
                        music.stop()
                    except:
                        pass
                else:
                    try:
                        music.play("battle_sound")
                    except:
                        pass
            
            elif menu_options[menu_selected] == "EXIT":
                exit()
    
    elif mode == "CONTROLS":
        if key == keys.ESCAPE:
            mode = "MENU"
    
    elif mode == "GAME":
        if key == keys.LEFT or key == keys.A:
            player.move(-1, 0)
        elif key == keys.RIGHT or key == keys.D:
            player.move(1, 0)
        elif key == keys.UP or key == keys.W:
            player.move(0, -1)
        elif key == keys.DOWN or key == keys.S:
            player.move(0, 1)
        elif key == keys.SPACE:
            player.attack()
        elif key == keys.Q:
            player.special_attack()
    
    elif mode == "GAME_OVER" or mode == "WIN":
        if key == keys.R:
            mode = "MENU"
            menu_selected = 0
        elif key == keys.ESCAPE:
            exit()

pgzrun.go()