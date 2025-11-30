"""
systems.audio - module de gestion de l'audio

EwoFluffy - BrokeTeam - 2025
"""

import pygame.mixer

from systems.logging import Logger
from systems.config import config


class AudioEngine:
    """
    AudioEngine - Moteur audio de BrokeEngine

    Objet de moteur audio, une instance peux être créée dans chaque objet Scene et permet de diffuser
    du son dans le jeu.
    """

    def __init__(self) -> None:
        self.logger: Logger = Logger("systems.audio")

        self.current_volume: float = config.audio.volume.master
        self.requested_volume: float = self.current_volume

        pygame.mixer.init()

        self.logger.success(f"New AudioEngine initialised : {self}")

    def play_file(self, file_path: str, loop=False) -> None:
        """
        play_file - Jouer un son ou une musique instantanément
        ---
        params :
            - file_path : str = Chemin d'accès du fichier sur le disque dur
            - loop : bool = définir sur vrai permet au son de se jouer en boucle
            jusqu'à ce qu'un nouveau son soit joué
        """

        pygame.mixer.music.load(file_path)
        if not pygame.mixer.music.get_busy():
            self.logger.log(f"Playing audio file {file_path} with {loop=}")
            pygame.mixer.music.play(-1 if loop else 0)
        else:
            self.logger.error("AudioEngine busy, cannot play music file")

    def set_volume(self, volume: float) -> None:
        """
        set_volume - Changer le volume du son avec un effet de fondu fluide
        ---
        params:
            - volume: float = Volume final du son
        """

        self.logger.log(
            f"Volume change requested from {self.current_volume} to {volume}"
        )
        self.requested_volume = volume

    def toggle(self, loop: bool = False) -> bool:
        """
        toggle - Basculer le status du son
        ---
        params:
            - loop: bool = Rejouer le son en boucle si le mode est reprise
        """

        self.logger.log("Toggling music state")
        if self.state():
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(-1 if loop else 0)

        return self.state()

    def stop(self) -> None:
        """
        stop - Arrêter le son en cour de diffusion
        """

        self.logger.log("Stopping music")
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            self.logger.error("Music not playing, cannot stop")

    def play(self, loop: bool = False) -> None:
        """
        play - Mettre le son en route
        ---
        params:
            - loop: bool = Définir le mode boucle
        """

        self.logger.log("Playing loaded music")
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1 if loop else 0)
        else:
            self.logger.warn("AudioEngine busy, stopping the current music")
            pygame.mixer.music.stop()

    def move(self, pos: int) -> None:
        """
        move - Se déplacer temporellement dans le son actuellement diffusé
        ---
        params:
            - pos: int = Position en seconde dans le son
        """

        self.logger.log(f"Moving music time to {pos}")
        if self.state():
            pygame.mixer.music.set_pos(pos)

    def update(self) -> None:
        """
        update - Fonction executée à chaque frames
        """

        if self.current_volume < self.requested_volume:
            self.current_volume += 0.01
            pygame.mixer.music.set_volume(self.current_volume)
        elif self.current_volume > self.requested_volume:
            self.current_volume -= 0.01
            pygame.mixer.music.set_volume(self.current_volume)

    @staticmethod
    def state() -> bool:
        """
        state - Retourner le status actuel du son
        """

        return pygame.mixer.music.get_busy()
