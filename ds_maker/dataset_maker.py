import pygame
import sys
import mss
import base64
import json
import random

def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No controller detected. Did you install drivers?")
        return

    joystick = pygame.joystick.Joystick(0) # change for different controllers
    joystick.init()

    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Rotation")

    font = pygame.font.Font(None, 36)

    running = True
    frame_counter = 0
    frames = []
    with mss.mss() as sct:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            rotation_angle = joystick.get_axis(0) * 135 # 135 signifies half of the input angle of the wheel i was using. (racing wheel apex by hori, which is 270 deg)
            L2_VAL = (joystick.get_axis(4) + 1) * 127.5
            R2_VAL = (joystick.get_axis(5) + 1) * 127.5

            screen_shot = sct.shot()

            with open(screen_shot, "rb") as image_file:
                base64_encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

            frame_data = {
                "base64_image": base64_encoded_image,
                "rotation_angle": rotation_angle,
                "L2_value": f"{L2_VAL:.2f}",
                "R2_value": f"{R2_VAL:.2f}",
            }

            frames.append(frame_data)
            frame_counter += 1
            jsont=random.randint(0,100000000)
            if frame_counter == 5:
                with open(f"dataset/{jsont}.json", "w") as json_file:
                    json.dump(frames, json_file, indent=4)
                frame_counter = 0
                frames = []

            screen.fill((0, 0, 0))
            rotation_text = font.render(f"Rotation: {rotation_angle:.2f} degrees", True, (255, 255, 255))
            L2_TEXT = font.render(f"L2: {L2_VAL:.2f}", True, (255, 255, 255))
            R2_TEXT = font.render(f"R2: {R2_VAL:.2f}", True, (255, 255, 255))
            FRAME_TEXT = font.render(f"FRAME: {frame_counter}", True, (255, 255, 255))
            JSON_TEXT = font.render(f"JSON FILE: {jsont}", True, (255, 255, 255))
            screen.blit(rotation_text, (50, 50))
            screen.blit(L2_TEXT, (50, 100))
            screen.blit(R2_TEXT, (50, 150))
            screen.blit(FRAME_TEXT, (50, 200))
            screen.blit(JSON_TEXT, (50, 250))
            pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
