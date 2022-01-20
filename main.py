import pygame
from math import floor
from pygame.locals import *

def main():
    pygame.init()

    world = World([1200, 1200])

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                clicked_box = world.grid.nodes[
                    floor(pos[0] / world.grid.box_width)
                ][
                    floor(pos[1] / world.grid.box_height)
                ]
                
                clicked_box.alive = not clicked_box.alive
            if event.type == pygame.KEYUP:
                world.started = True

        world.update()
        if world.started:
            world.conway_generation()

class World:
    def __init__(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.fps = 0.25
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(self.fps)
        self.grid = Grid(60, 60, size)
        self.started = False

    def update(self):
        self.screen.fill((0, 0, 0))

        for row in self.grid.nodes:
            for node in row:
                node.display(self)
        
        pygame.display.flip()
    
    def conway_generation(self):
        self.grid.prev_nodes = [
            [
                Rectangle(
                    x=cell.x,
                    y=cell.y,
                    width=cell.width,
                    height=cell.height,
                    alive=cell.alive
                ) for cell in self.grid.nodes[i]
            ]
            for i in range(len(self.grid.nodes))
        ]
        for i, row in enumerate(self.grid.nodes):
            for j, node in enumerate(row):
                self.conway_rules(self.grid.prev_nodes[i][j], node, self.count_neighbors(i, j))

    def count_neighbors(self, i, j):
        neighbor_count = 0
        neighbors = []

        for k in range(i - 1, i + 2):
            for l in range(j - 1, j + 2):
                if (not (k == i and 
                    l == j) and 
                    k >= 0 and 
                    k < len(self.grid.prev_nodes) and 
                    l >= 0 and 
                    l < len(self.grid.prev_nodes[0]) and 
                    self.grid.prev_nodes[k][l].alive
                ):
                    neighbors.append((k, l))
                    neighbor_count += 1
        return neighbor_count

    def conway_rules(self, prev_cell, cell, neighbor_count):
        if not prev_cell.alive and neighbor_count == 3:
            cell.alive = True
        elif prev_cell.alive and neighbor_count not in [2,3]:
            cell.alive = False

class Grid:
    def __init__(self, rows, columns, world_size):
        self.rows = rows
        self.columns = columns
        self.box_width = world_size[0] / self.columns
        self.box_height = world_size[1] / self.rows
        self.nodes = self.fill_grid()
        self.prev_nodes = self.nodes
    
    def fill_grid(self):
        nodes = []

        for i in range(self.columns):
            row_nodes = []
            for j in range(self.rows):
                box = Rectangle(i*self.box_width, j*self.box_height, self.box_width, self.box_height)
                row_nodes.append(box)
            nodes.append(row_nodes)

        return nodes

class Rectangle:
    def __init__(self, x, y, width, height, alive=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = 0.5
        self.color = Color(255,255,255)
        self.alive = alive

    def display(self, world):
        border = pygame.Rect(self.x, self.y, self.width, self.height)
        inner_rect = pygame.Rect(self.x + self.border, self.y + self.border, self.width - self.border * 2, self.height - self.border * 2)
        pygame.draw.rect(world.screen, self.color, border, 0)
        if not self.alive:
            pygame.draw.rect(world.screen, Color(0,0,0), inner_rect, 0)


if __name__ == "__main__":
    main()
