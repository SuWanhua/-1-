#  -*- coding: utf-8 -*-
#  alien_invasion.py  完整整合版（含外星人子弹 + 原功能标注）
import sys, time, pygame
from random import choice, randint           # 【新增 外星人子弹】
from pygame.sprite import Sprite

# -------------------- 通用工具 --------------------
class Settings:
    def __init__(self):
        # 屏幕
        self.screen_width, self.screen_height = 1200, 800
        self.bg_color = (230, 230, 230)
        # 飞船
        self.ship_limit = 3
        # 子弹
        self.bullet_width, self.bullet_height = 3, 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # 外星人
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        # 外星人子弹（新增）【新增 外星人子弹】
        self.alien_bullet_width = 5        # 【新增 外星人子弹】
        self.alien_bullet_height = 15      # 【新增 外星人子弹】
        self.alien_bullet_color = (255, 0, 0)  # 【新增 外星人子弹】
        self.alien_bullet_speed = 1.8      # 【新增 外星人子弹】
        self.alien_bullet_allowed = 10     # 【新增 外星人子弹】
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0          # 永不重置

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1


class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


# -------------------- 飞船 --------------------
class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)


# -------------------- 子弹 --------------------
class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


# -------------------- 外星人 --------------------
class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x


# -------------------- 外星人子弹（新增）【新增 外星人子弹】 --------------------
class AlienBullet(Sprite):                                              # 【新增 外星人子弹】
    def __init__(self, ai_game, alien):                                 # 【新增 外星人子弹】
        super().__init__()                                              # 【新增 外星人子弹】
        self.screen = ai_game.screen                                    # 【新增 外星人子弹】
        self.settings = ai_game.settings                                # 【新增 外星人子弹】
        self.color = self.settings.alien_bullet_color                   # 【新增 外星人子弹】
        self.rect = pygame.Rect(0, 0,                                  # 【新增 外星人子弹】
                                self.settings.alien_bullet_width,       # 【新增 外星人子弹】
                                self.settings.alien_bullet_height)      # 【新增 外星人子弹】
        self.rect.centerx = alien.rect.centerx                          # 【新增 外星人子弹】
        self.rect.bottom = alien.rect.bottom                            # 【新增 外星人子弹】
        self.y = float(self.rect.y)                                     # 【新增 外星人子弹】

    def update(self):                                                   # 【新增 外星人子弹】
        self.y += self.settings.alien_bullet_speed                      # 【新增 外星人子弹】
        self.rect.y = self.y                                            # 【新增 外星人子弹】

    def draw(self):                                                     # 【新增 外星人子弹】
        pygame.draw.rect(self.screen, self.color, self.rect)           # 【新增 外星人子弹】


# -------------------- 爆炸（原标注保留） --------------------
class Explosion(Sprite):  # 新增  爆炸
    def __init__(self, ai_game, center):  # 新增  爆炸
        super().__init__()  # 新增  爆炸
        self.screen = ai_game.screen  # 新增  爆炸
        self.alpha = 255  # 新增  爆炸
        self.max_scale = 2.5  # 新增  爆炸
        self.scale_step = 0.08  # 新增  爆炸
        self.fade_speed = 8  # 新增  爆炸
        try:  # 新增  爆炸
            self.orig_image = pygame.image.load('images/explosion0.bmp')  # 新增  爆炸
        except FileNotFoundError:  # 新增  爆炸
            self.orig_image = pygame.Surface((60, 60)).convert()  # 新增  爆炸
            self.orig_image.fill((255, 220, 0))  # 新增  爆炸
        self.orig_image.set_colorkey((0, 0, 0))  # 新增  爆炸
        self.image = self.orig_image.copy()  # 新增  爆炸
        self.rect = self.image.get_rect(center=center)  # 新增  爆炸
        self.scale = 1.0  # 新增  爆炸

    def update(self):  # 新增  爆炸
        self.scale += self.scale_step  # 新增  爆炸
        if self.scale >= self.max_scale:  # 新增  爆炸
            self.scale = self.max_scale  # 新增  爆炸
        w, h = self.orig_image.get_size()  # 新增  爆炸
        new_size = int(w * self.scale), int(h * self.scale)  # 新增  爆炸
        self.image = pygame.transform.scale(self.orig_image, new_size)  # 新增  爆炸
        self.rect = self.image.get_rect(center=self.rect.center)  # 新增  爆炸
        self.alpha = max(0, self.alpha - self.fade_speed)  # 新增  爆炸
        self.image.set_alpha(self.alpha)  # 新增  爆炸
        if self.alpha <= 0:  # 新增  爆炸
            self.kill()  # 新增  爆炸

    def draw(self, surface=None):  # 新增  爆炸
        surface = surface or self.screen  # 新增  爆炸
        surface.blit(self.image, self.rect)  # 新增  爆炸


# -------------------- 积分飞升（原标注保留） --------------------
class ScoreFloat(Sprite):  # 新增 积分飞升
    def __init__(self, ai_game, pos, value):  # 新增 积分飞升
        super().__init__()  # 新增 积分飞升
        self.screen = ai_game.screen  # 新增 积分飞升
        self.value = value  # 新增 积分飞升
        self.font = pygame.font.SysFont(None, 28)  # 新增 积分飞升
        self.image = self.font.render(f"+{value}", True, (250, 250, 0))  # 新增 积分飞升
        self.rect = self.image.get_rect(center=pos)  # 新增 积分飞升
        self.speed_y = -3  # 新增 积分飞升
        self.alpha = 255  # 新增 积分飞升
        self.fade_sp = 6  # 新增 积分飞升

    def update(self):  # 新增 积分飞升
        self.rect.y += self.speed_y  # 新增 积分飞升
        self.alpha = max(0, self.alpha - self.fade_sp)  # 新增 积分飞升
        self.image.set_alpha(self.alpha)  # 新增 积分飞升
        if self.alpha <= 0 or self.rect.y <= 0:  # 新增 积分飞升
            self.kill()  # 新增 积分飞升

    def draw(self, surface=None):  # 新增 积分飞升
        surface = surface or self.screen  # 新增 积分飞升
        surface.blit(self.image, self.rect)  # 新增 积分飞升


# -------------------- 记分牌 --------------------
class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        from ship import Ship
        self.ships = pygame.sprite.Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


# -------------------- 主游戏 --------------------
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                              self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()    # 新增  爆炸
        self.score_floats = pygame.sprite.Group()  # 新增 积分飞升
        self.alien_bullets = pygame.sprite.Group()  # 【新增 外星人子弹】

        self._create_fleet()
        self.game_active = False
        self.play_button = Button(self, "Play")

    # -------------------- 主循环 --------------------
    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()     # 【新增 外星人子弹】
                self.explosions.update()         # 新增  爆炸
                self.score_floats.update()       # 新增 积分飞升
            self._update_screen()
            self.clock.tick(60)

    # -------------------- 事件 --------------------
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            # 清空所有精灵组
            self.bullets.empty()
            self.aliens.empty()
            self.explosions.empty()      # 新增  爆炸
            self.score_floats.empty()    # 新增 积分飞升
            self.alien_bullets.empty()   # 【新增 外星人子弹】
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # -------------------- 子弹 --------------------
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                               True, True)
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    # 新增  爆炸
                    explosion = Explosion(self, alien.rect.center)
                    self.explosions.add(explosion)
                    # 新增 积分飞升
                    score_float = ScoreFloat(self, alien.rect.center,
                                           self.settings.alien_points)
                    self.score_floats.add(score_float)
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self.alien_bullets.empty()  # 【新增 外星人子弹】
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    # -------------------- 外星人子弹（新增） --------------------
    def _alien_shoot(self):                                            
        if len(self.alien_bullets) < self.settings.alien_bullet_allowed and self.aliens:  
            shooter = choice(self.aliens.sprites())                   
            bullet = AlienBullet(self, shooter)                       
            self.alien_bullets.add(bullet)                            

    def _update_alien_bullets(self):                                    
        self.alien_bullets.update()                                    
        for bullet in self.alien_bullets.copy():                      
            if bullet.rect.top >= self.settings.screen_height:          
                self.alien_bullets.remove(bullet)                      
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):  
            self._ship_hit()                                           

    # -------------------- 外星人 --------------------
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        # 随机发射（新增）【新增 外星人子弹】
        if randint(1, 1000) < 4:                                        # 【新增 外星人子弹】
            self._alien_shoot()                                           # 【新增 外星人子弹】
        # 撞飞船
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # 新增 飞船爆炸
            explosion = Explosion(self, self.ship.rect.center)
            self.explosions.add(explosion)

            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self.alien_bullets.empty()  # 【新增 外星人子弹】
            self._create_fleet()
            self.ship.center_ship()
            time.sleep(0.5)
        else:
            self._show_final_score()     # 新增 显示总分 2 秒
            self.game_active = False
            pygame.mouse.set_visible(True)

    # ---------- 新增：中央大字显示总分 2 秒 ----------
    def _show_final_score(self):  # 新增 显示总分 2 秒
        font = pygame.font.SysFont(None, 96)  # 新增 显示总分 2 秒
        text = font.render(f"总分 = {self.stats.score:,}", True, (30, 30, 30))  # 新增 显示总分 2 秒
        rect = text.get_rect(center=self.screen.get_rect().center)  # 新增 显示总分 2 秒
        self.screen.fill(self.settings.bg_color)  # 新增 显示总分 2 秒
        self.screen.blit(text, rect)  # 新增 显示总分 2 秒
        pygame.display.flip()  # 新增 显示总分 2 秒
        time.sleep(3)  # 新增 显示总分 2 秒

    # -------------------- 舰队 --------------------
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x, y):
        new_alien = Alien(self)
        new_alien.x = x
        new_alien.rect.x, new_alien.rect.y = x, y
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # -------------------- 绘制 --------------------
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.alien_bullets.sprites():  # 【新增 外星人子弹】
            bullet.draw()                             # 【新增 外星人子弹】
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)      # 新增  爆炸
        self.score_floats.draw(self.screen)    # 新增 积分飞升
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()