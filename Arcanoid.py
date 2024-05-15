import pygame
from button import ImageButton
from pygame.locals import *

pygame.init()

WIDTH = 600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arcanoid')

#Шрифта
font = pygame.font.SysFont('Constantia', 30)
#Цвет
bg = (234, 218, 184)
#Цвет блока 
block1 = (212, 116, 121)
block2 = (178, 34, 34)
block3 = (139, 0, 0)
#Цвет платформы
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)
#Цвет текста 
text_col = (78, 81, 139)



#Переменные
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60


#Вывод текста на экран 
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))



class wall():
	def __init__(self):
		self.width = WIDTH // cols
		self.height = 50

	def create_wall(self):
		self.blocks = []
		#Список для блоков
		block_individual = []
		for row in range(rows):
			#Сброс списка блоков
			block_row = []
			#Обход по строкам
			for col in range(cols):
				#Строение блоков
				block_x = col * self.width
				block_y = row * self.height
				rect = pygame.Rect(block_x, block_y, self.width, self.height)
				#Прочность блоков
				if row < 2:
					strength = 3
				elif row < 4:
					strength = 2
				elif row < 6:
					strength = 1
				#Список для хранения цвета и прямоугольника
				block_individual = [rect, strength]
				#Добавление блока в список
				block_row.append(block_individual)
			#добавление строки в основной список
			self.blocks.append(block_row)


	def draw_wall(self):
		for row in self.blocks:
			for block in row:
				#Цвет в зависимости от прочности
				if block[1] == 3:
					block_col = block3
				elif block[1] == 2:
					block_col = block2
				elif block[1] == 1:
					block_col = block1
				pygame.draw.rect(screen, block_col, block[0])
				pygame.draw.rect(screen, bg, (block[0]), 2)



class paddle():
	def __init__(self):
		self.reset()


	def move(self):
		#Направление движения 
		self.direction = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0 or key[pygame.K_a] and self.rect.left > 0:
			self.rect.x -= self.speed
			self.direction = -1
		if key[pygame.K_RIGHT] and self.rect.right < WIDTH or key[pygame.K_d] and self.rect.right < WIDTH:
			self.rect.x += self.speed
			self.direction = 1

	def draw(self):
		pygame.draw.rect(screen, paddle_col, self.rect)
		pygame.draw.rect(screen, paddle_outline, self.rect, )


	def reset(self):
		#Переменные платформы 
		self.height = 20
		self.width = int(WIDTH / cols)
		self.x = int((WIDTH / 2) - (self.width / 2))
		self.y = HEIGHT - (self.height * 2)
		self.speed = 10
		self.rect = Rect(self.x, self.y, self.width, self.height)
		self.direction = 0



class game_ball():
	def __init__(self, x, y):
		self.reset(x, y)


	def move(self):

		#столкновение
		collision_thresh = 5

		#проверка разрушена стена или нет
		wall_destroyed = 1
		row_count = 0
		for row in wall.blocks:
			item_count = 0
			for item in row:
				#проверка столкновения
				if self.rect.colliderect(item[0]):
					#проверка столкновения в верху
					if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
						self.speed_y *= -1
					#проверка столкновения внизу 
					if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
						self.speed_y *= -1						
					#проверка столкновения слева 
					if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
						self.speed_x *= -1
					#проверка столкновения справа
					if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
						self.speed_x *= -1
					#уменьшение прочности блока 
					if wall.blocks[row_count][item_count][1] > 1:
						wall.blocks[row_count][item_count][1] -= 1
					else:
						wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

				#проверка на нахождение блока 
				if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
					wall_destroyed = 0
				item_count += 1
			row_count += 1
		#проверка на разрушения стены 
		if wall_destroyed == 1:
			self.game_over = 1



		#проверка столкновения 
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speed_x *= -1

		#проверка столкновения с верхней или нижней частью экрана 
		if self.rect.top < 0:
			self.speed_y *= -1
		if self.rect.bottom > HEIGHT:
			self.game_over = -1


		#проверка столкновения с платформой 
		if self.rect.colliderect(player_paddle):
			#проверка столкновения вверху 
			if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
				self.speed_y *= -1
				self.speed_x += player_paddle.direction
				if self.speed_x > self.speed_max:
					self.speed_x = self.speed_max
				elif self.speed_x < 0 and self.speed_x < -self.speed_max:
					self.speed_x = -self.speed_max
			else:
				self.speed_x *= -1



		self.rect.x += self.speed_x
		self.rect.y += self.speed_y

		return self.game_over


	def draw(self):
		pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
		pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)



	def reset(self, x, y):
		self.ball_rad = 10
		self.x = x - self.ball_rad
		self.y = y
		self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
		self.speed_x = 4
		self.speed_y = -4
		self.speed_max = 5
		self.game_over = 0



#создание стены 
wall = wall()
wall.create_wall()

#создание платформы 
player_paddle = paddle()


#создание шара 
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

def game():
	live_ball = False
	game_over = 0

	running = True
	while running:

		clock.tick(fps)
		
		screen.fill(bg)

		#отрисовка всех объектов
		wall.draw_wall()
		player_paddle.draw()
		ball.draw()

		if live_ball:
			#отрисовка платформы 
			player_paddle.move()
			#отрисовка шара 
			game_over = ball.move()
			if game_over != 0:
				live_ball = False


		#текст
		if not live_ball:
			if game_over == 1:
				draw_text('YOU WON!', font, text_col, 240, HEIGHT // 2 + 50)
			elif game_over == -1:
				draw_text('YOU LOST!', font, text_col, 240, HEIGHT // 2 + 50)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
				live_ball = True
				ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
				player_paddle.reset()
				wall.create_wall()

		pygame.display.update()

def main_menu():
	start_button = ImageButton(WIDTH/2-(252/2), 150, 252, 74, "", "Play1.png", "Play2.png", "Button.mp3")
	exit_button = ImageButton(WIDTH/2-(252/2), 250, 252, 74, "", "Quit1.png", "Quit2.png", "Button.mp3")

	running = True
	while running:
		screen.fill((245, 245, 220))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
			
			if event.type == pygame.USEREVENT and event.button == start_button:
				game()

			if event.type == pygame.USEREVENT and event.button == exit_button:
				running = False
				pygame.quit()

			for btn in [start_button, exit_button]:
				btn.handle_event(event)

		for btn in [start_button, exit_button]:
			btn.check_hover(pygame.mouse.get_pos())
			btn.draw(screen)

		pygame.display.flip()

if __name__ == "__main__":
    main_menu()
