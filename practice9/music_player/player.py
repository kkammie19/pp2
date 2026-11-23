
import pygame
import os


class MusicPlayer:
    def __init__(self, screen):
        self.screen = screen

        # Music folder path
        self.music_folder = os.path.join(
            os.path.dirname(__file__),
            "music"
        )

        # Playlist
        self.playlist = [
            os.path.join(self.music_folder, "song1.mp3"),
            os.path.join(self.music_folder, "song2.mp3")
        ]

        self.current_track = 0
        self.is_playing = False

        pygame.mixer.init()

        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 24)

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_track += 1

        if self.current_track >= len(self.playlist):
            self.current_track = 0

        self.play()

    def previous_track(self):
        self.current_track -= 1

        if self.current_track < 0:
            self.current_track = len(self.playlist) - 1

        self.play()

    def draw(self):
        self.screen.fill((30, 30, 30))

        title = self.font.render(
            "Music Player",
            True,
            (255, 255, 255)
        )

        track_name = os.path.basename(
            self.playlist[self.current_track]
        )

        track_text = self.small_font.render(
            f"Current track: {track_name}",
            True,
            (200, 200, 200)
        )

        status = "Playing" if self.is_playing else "Stopped"

        status_text = self.small_font.render(
            f"Status: {status}",
            True,
            (100, 255, 100) if self.is_playing else (255, 100, 100)
        )

        controls_text = self.small_font.render(
            "P: Play | S: Stop | N: Next | B: Previous | Q: Quit",
            True,
            (255, 255, 255)
        )

        self.screen.blit(title, (250, 100))
        self.screen.blit(track_text, (200, 250))
        self.screen.blit(status_text, (200, 310))
        self.screen.blit(controls_text, (50, 500))
