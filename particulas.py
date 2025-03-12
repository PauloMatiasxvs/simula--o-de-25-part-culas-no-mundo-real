import pygame
import random
import math

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de 25 Partículas")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Classe para representar uma partícula
class Particle:
    def __init__(self, x, y):
        self.x = x  # Posição x
        self.y = y  # Posição y
        self.radius = 10  # Raio da partícula
        self.vx = random.uniform(-3, 3)  # Velocidade inicial em x
        self.vy = random.uniform(-3, 3)  # Velocidade inicial em y
        self.mass = 1  # Massa (igual para todas)

    def update(self):
        # Atualiza a posição
        self.x += self.vx
        self.y += self.vy

        # Colisão com as bordas da tela
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy

    def draw(self):
        # Desenha a partícula como um círculo vermelho
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

# Função para calcular colisão entre duas partículas
def collide(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.sqrt(dx**2 + dy**2)

    # Verifica se há colisão
    if distance < p1.radius + p2.radius:
        # Normaliza o vetor de colisão
        nx = dx / distance if distance != 0 else 0
        ny = dy / distance if distance != 0 else 0

        # Calcula o impulso (colisão elástica)
        relative_vx = p1.vx - p2.vx
        relative_vy = p1.vy - p2.vy
        impulse = 2 * (relative_vx * nx + relative_vy * ny) / (p1.mass + p2.mass)

        # Atualiza as velocidades
        p1.vx -= impulse * p2.mass * nx
        p1.vy -= impulse * p2.mass * ny
        p2.vx += impulse * p1.mass * nx
        p2.vy += impulse * p1.mass * ny

        # Evita sobreposição movendo as partículas
        overlap = (p1.radius + p2.radius - distance) / 2
        p1.x -= overlap * nx
        p1.y -= overlap * ny
        p2.x += overlap * nx
        p2.y += overlap * ny

# Cria 25 partículas com posições iniciais aleatórias
particles = []
for _ in range(25):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    particles.append(Particle(x, y))

# Loop principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpa a tela
    screen.fill(WHITE)

    # Atualiza e desenha todas as partículas
    for particle in particles:
        particle.update()
        particle.draw()

    # Verifica colisões entre todas as partículas
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            collide(particles[i], particles[j])

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)  # Limita a 60 FPS

# Encerra o Pygame
pygame.quit()