from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

import sys

import pygame

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        """Set game to display in FULLSCREEN mode"""
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()        
            self._update_screen()

    def _check_events(self):
        #Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_s:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False      

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        #if  len(self.bullets) < self.settings.bullets_allowed:
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        #Update position of bullets and remove old bullets.
        self.bullets.update()

        #Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Create a new alien and add to screen"""
        #Create an alien and find the number of aliens in a row.
        #Spacing b/n aliens is one alien width
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens_x = available_space_x // (2 * alien_width)

        #Create the first row of aliens
        for alien_number in range(number_of_aliens_x):
            self._create_alien(alien_number)


    def _create_alien(self,alien_number):
        """Create an alien and place it in a row."""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + ((2 * alien_width) * alien_number)
        alien.rect.x = alien.x
        self.aliens.add(alien)

        
    def _update_screen(self):
        #Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        #Draw alien to screen
        self.aliens.draw(self.screen)

        #Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == "__main__":
    #Make a game istance, and run the game.
    ai = AlienInvasion()
    ai.run_game()