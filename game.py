import pygame
import random
import sys
import gamesetting

pygame.init()

# screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Underwater Treasure Hurt")

# pic
diver_img = pygame.image.load("image/diver.bmp")  
octopus_img = pygame.image.load("image/octopus.bmp")  
shark_img = pygame.image.load("image/shark.bmp")  
bubble_img = pygame.image.load("image/bubbles.bmp")  

treasure_img = pygame.image.load("image/treasure.bmp")  
background_img = pygame.image.load("image/background.bmp")  

# small pic
diver_img = pygame.transform.scale(diver_img, (50, 50))
octopus_img = pygame.transform.scale(octopus_img, (50, 50))
shark_img = pygame.transform.scale(shark_img, (70, 50))
big_octopus_img = pygame.transform.scale(octopus_img, (100, 100))
big_shark_img = pygame.transform.scale(shark_img, (120, 80))
treasure_img = pygame.transform.scale(treasure_img, (50, 50))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bubble_img = pygame.transform.scale(bubble_img, (10, 10))  
big_bubble_img = pygame.transform.scale(bubble_img, (50, 50))

# 
clock = pygame.time.Clock()
font = pygame.font.SysFont("None", 24)

# player
player = {"x": 50, "y": 300, "speed": 5, "lives": 300000, "score": 0}


def generate_enemy():
    enemies = []
    for _ in range(5):
        while True:
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)

         
            overlap = False
            for enemy in enemies:
                if abs(enemy["x"] - x) < 100 and abs(enemy["y"] - y) < 60:  
                    overlap = True
                    break

            if not overlap:
                enemies.append({
                    "x": x,
                    "y": y,
                    "speed_x": random.choice([-1, 1]),  
                    "speed_y": random.choice([-1, 1]),  
                    "type": "small",
                    "health": "1"
                })
                break
    return enemies


enemies = generate_enemy()

# big shark and big octupus  move range
bosses = [
    {"x": SCREEN_WIDTH - 200, "y": 200, "type": "big_octopus", "health": 2, "move_range": 50},
    {"x": SCREEN_WIDTH - 200, "y": 400, "type": "big_shark", "health": 3, "move_range": 50}
]

# treasure
treasure = {"x": SCREEN_WIDTH - 100, "y": SCREEN_HEIGHT // 2}

# tiem
time_remaining = 60

# bubbles
bubbles = []

# text
def draw_text(text, x, y, color):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# bump
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# great new bubbles
def generate_bubbles():
    global bubbles
    bubbles = []
    for _ in range(20):
        bubble_type = random.choice(["small", "large"])  
        bubble = {
            "x": random.randint(50, SCREEN_WIDTH - 50),
            "y": random.randint(50, SCREEN_HEIGHT - 50),
            "type": bubble_type
        }
        bubbles.append(bubble)

# while
def main():
    global time_remaining

    running = True
    victory = False
    generate_bubbles()  

    while running:
        screen.blit(background_img, (0, 0))
        draw_text(f"time: {int(time_remaining)}s", 10, 10,gamesetting. WHITE)
        draw_text(f"life: {player['lives']}", 10, 40, gamesetting.WHITE)

        # event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # up ,down ,left ,right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player["y"] > 0:
            player["y"] -= player["speed"]
        if keys[pygame.K_DOWN] and player["y"] < SCREEN_HEIGHT - 50:
            player["y"] += player["speed"]
        if keys[pygame.K_LEFT] and player["x"] > 0:
            player["x"] -= player["speed"]
        if keys[pygame.K_RIGHT] and player["x"] < SCREEN_WIDTH - 50:
            player["x"] += player["speed"]

        # draw diver
        screen.blit(diver_img, (player["x"], player["y"]))

        # draw enemy
        for enemy in enemies:
            if enemy["type"] == "small":
                screen.blit(octopus_img if random.choice([True, False]) else shark_img, (enemy["x"], enemy["y"]))

            enemy["x"] += enemy["speed_x"]
            enemy["y"] += enemy["speed_y"]

            # bump check
            if check_collision(pygame.Rect(player["x"], player["y"], 50, 50), pygame.Rect(enemy["x"], enemy["y"], 50, 50)):
                player["lives"] -= 1
                if player["lives"] <= 0:
                    running = False

            # boundary bounce 边界反弹
            if enemy["x"] <= 0 or enemy["x"] >= SCREEN_WIDTH - 50:
                enemy["speed_x"] *= -1
            if enemy["y"] <= 0 or enemy["y"] >= SCREEN_HEIGHT - 50:
                enemy["speed_y"] *= -1

    
        for boss in bosses:
            if boss["type"] == "big_octopus":
                screen.blit(big_octopus_img, (boss["x"], boss["y"]))
                boss["x"] += random.randint(-boss["move_range"], boss["move_range"])
                boss["y"] += random.randint(-boss["move_range"], boss["move_range"])
            elif boss["type"] == "big_shark":
                screen.blit(big_shark_img, (boss["x"], boss["y"]))
                boss["x"] += random.randint(-boss["move_range"], boss["move_range"])
                boss["y"] += random.randint(-boss["move_range"], boss["move_range"])

  



        # draw bubbles
        for bubble in bubbles:
            screen.blit(bubble_img, (bubble["x"], bubble["y"]))

         
            if check_collision(pygame.Rect(player["x"], player["y"], 50, 50), pygame.Rect(bubble["x"], bubble["y"], 30, 30)):
                if bubble["type"] == "small":
                    time_remaining += 100 
                elif bubble["type"] == "large":
                    time_remaining += 150  
                bubbles.remove(bubble)

         
        if len(bubbles) < 5:
            generate_bubbles()

        # draw treasure
        screen.blit(treasure_img, (treasure["x"], treasure["y"]))

        # time function
        time_remaining -= 1 / 60
        if time_remaining <= 0:
            running = False

     
        if check_collision(pygame.Rect(player["x"], player["y"], 50, 50), pygame.Rect(treasure["x"], treasure["y"], 50, 50)):
            victory = True
            running = False

        pygame.display.flip()
        clock.tick(60)

    # game over show the result
    screen.blit(background_img, (0, 0))
    if victory:
        draw_text("Victory!", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, gamesetting.Yellow)
    else:
        draw_text("Game Over!", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, gamesetting.RED)
    
    pygame.display.flip()
    pygame.time.wait(5000)  # 暂停5秒

    pygame.quit()


main()
