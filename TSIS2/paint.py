import pygame
import sys
import datetime
import os

pygame.init()

# Window settings
WIDTH = 1000
HEIGHT = 700
TOOLBAR_HEIGHT = 120
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Application")

clock = pygame.time.Clock()

# Canvas
canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill((255, 255, 255))

# Colors
colors = {
    "Black": (0, 0, 0),
    "Red": (255, 0, 0),
    "Green": (0, 180, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Orange": (255, 165, 0),
    "White": (255, 255, 255)
}

selected_color = colors["Black"]

# Brush sizes
brush_sizes = [2, 5, 10]
brush_size = 5

# Tools
tools = [
    "Pencil",
    "Line",
    "Rectangle",
    "Circle",
    "Square",
    "Right Triangle",
    "Equilateral Triangle",
    "Rhombus",
    "Fill",
    "Text"
]

current_tool = "Pencil"

# Drawing states
drawing = False
last_pos = None
shape_start = None
shape_end = None

# Text states
text_active = False
text_input = ""
text_position = None
text_font = pygame.font.SysFont("Arial", 24)

# Buttons
color_buttons = {}
tool_buttons = {}
size_buttons = {}

# Color buttons
x = 10

for name, color in colors.items():
    rect = pygame.Rect(x, 10, 30, 30)
    color_buttons[name] = rect
    x += 35

# Clear button
clear_button = pygame.Rect(280, 10, 90, 35)

# Brush size buttons
for i, size in enumerate(brush_sizes):
    rect = pygame.Rect(400 + i * 55, 10, 45, 35)
    size_buttons[size] = rect

# Tool buttons
for i, tool in enumerate(tools):
    rect = pygame.Rect(10 + i * 98, 60, 92, 40)
    tool_buttons[tool] = rect


def canvas_position(pos):
    """Convert screen coordinates to canvas coordinates."""
    x, y = pos

    if y < TOOLBAR_HEIGHT:
        return None

    return (x, y - TOOLBAR_HEIGHT)


def get_rect(start, end):
    """Create a normalized rectangle from two points."""
    x1, y1 = start
    x2, y2 = end

    return pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )


def draw_shape(surface, tool, start, end, color, width):
    """Draw a shape using two points."""

    rect = get_rect(start, end)

    if tool == "Line":
        pygame.draw.line(surface, color, start, end, width)

    elif tool == "Rectangle":
        pygame.draw.rect(surface, color, rect, width)

    elif tool == "Circle":
        pygame.draw.ellipse(surface, color, rect, width)

    elif tool == "Square":
        side = min(rect.width, rect.height)

        square = pygame.Rect(
            rect.x,
            rect.y,
            side,
            side
        )

        pygame.draw.rect(surface, color, square, width)

    elif tool == "Right Triangle":
        points = [
            start,
            (end[0], start[1]),
            end
        ]

        pygame.draw.polygon(surface, color, points, width)

    elif tool == "Equilateral Triangle":
        left = min(start[0], end[0])
        right = max(start[0], end[0])

        side = right - left
        tri_height = int(side * 0.866)

        bottom = max(start[1], end[1])
        top = bottom - tri_height

        points = [
            ((left + right) // 2, top),
            (left, bottom),
            (right, bottom)
        ]

        pygame.draw.polygon(surface, color, points, width)

    elif tool == "Rhombus":
        points = [
            (rect.centerx, rect.top),
            (rect.right, rect.centery),
            (rect.centerx, rect.bottom),
            (rect.left, rect.centery)
        ]

        pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, new_color):
    """Fill connected pixels of the same color."""

    x, y = start_pos

    if not (0 <= x < surface.get_width()
            and 0 <= y < surface.get_height()):
        return

    target_color = surface.get_at((x, y))[:3]
    new_color = tuple(new_color[:3])

    if target_color == new_color:
        return

    stack = [(x, y)]
    visited = {(x, y)}

    while stack:
        px, py = stack.pop()

        if surface.get_at((px, py))[:3] != target_color:
            continue

        surface.set_at((px, py), new_color)

        neighbors = [
            (px + 1, py),
            (px - 1, py),
            (px, py + 1),
            (px, py - 1)
        ]

        for nx, ny in neighbors:
            if (
                0 <= nx < surface.get_width()
                and 0 <= ny < surface.get_height()
                and (nx, ny) not in visited
                and surface.get_at((nx, ny))[:3] == target_color
            ):
                visited.add((nx, ny))
                stack.append((nx, ny))

def save_canvas():
    script_folder = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_folder, "saved_drawings")

    os.makedirs(folder, exist_ok=True)

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"drawing_{current_time}.png"
    filepath = os.path.join(folder, filename)

    pygame.image.save(canvas, filepath)
    print(f"Drawing saved: {filepath}")               

def draw_toolbar():
    """Draw the toolbar and all buttons."""

    pygame.draw.rect(
        screen,
        (220, 220, 220),
        (0, 0, WIDTH, TOOLBAR_HEIGHT)
    )

    # Color buttons
    for name, rect in color_buttons.items():
        pygame.draw.rect(screen, colors[name], rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        if selected_color == colors[name]:
            pygame.draw.rect(screen, (0, 0, 0), rect.inflate(4, 4), 2)

    # Clear button
    pygame.draw.rect(screen, (190, 190, 190), clear_button)
    pygame.draw.rect(screen, (0, 0, 0), clear_button, 2)

    clear_text = pygame.font.SysFont("Arial", 20).render(
        "Clear", True, (0, 0, 0)
    )
    screen.blit(clear_text, (clear_button.x + 18, clear_button.y + 7))

    # Brush sizes
    font = pygame.font.SysFont("Arial", 18)

    for size, rect in size_buttons.items():
        button_color = (160, 160, 160)

        if brush_size == size:
            button_color = (120, 180, 220)

        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        size_text = font.render(str(size), True, (0, 0, 0))
        screen.blit(
            size_text,
            (rect.centerx - size_text.get_width() // 2,
             rect.centery - size_text.get_height() // 2)
        )

    # Tool buttons
    tool_font = pygame.font.SysFont("Arial", 13)

    for tool, rect in tool_buttons.items():
        button_color = (180, 180, 180)

        if current_tool == tool:
            button_color = (120, 180, 220)

        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        label = tool_font.render(tool, True, (0, 0, 0))

        screen.blit(
            label,
            (rect.centerx - label.get_width() // 2,
             rect.centery - label.get_height() // 2)
        )


running = True

while running:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Keyboard
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            if text_active:

                if event.key == pygame.K_RETURN:
                    if text_input:
                        rendered_text = text_font.render(
                            text_input, True, selected_color
                        )
                        canvas.blit(rendered_text, text_position)

                    text_active = False
                    text_input = ""
                    text_position = None

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_input = ""
                    text_position = None

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                elif event.unicode.isprintable():
                    text_input += event.unicode

            else:
                if event.key == pygame.K_1:
                    brush_size = 2

                elif event.key == pygame.K_2:
                    brush_size = 5

                elif event.key == pygame.K_3:
                    brush_size = 10

        # Mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mouse_pos = event.pos

            # Toolbar click
            if mouse_pos[1] < TOOLBAR_HEIGHT:

                # Select color
                for name, rect in color_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        selected_color = colors[name]

                # Clear canvas
                if clear_button.collidepoint(mouse_pos):
                    canvas.fill((255, 255, 255))

                    text_active = False
                    text_input = ""
                    text_position = None

                # Select brush size
                for size, rect in size_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        brush_size = size

                # Select tool
                for tool, rect in tool_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        current_tool = tool

            # Canvas click
            else:
                pos = canvas_position(mouse_pos)

                if pos is not None and not text_active:

                    # Fill tool
                    if current_tool == "Fill":
                        flood_fill(canvas, pos, selected_color)

                    # Text tool
                    elif current_tool == "Text":
                        text_active = True
                        text_input = ""
                        text_position = pos

                    # Drawing tools
                    else:
                        drawing = True
                        shape_start = pos
                        shape_end = pos
                        last_pos = pos

                        # Pencil draws a dot on click
                        if current_tool == "Pencil":
                            pygame.draw.circle(
                                canvas,
                                selected_color,
                                pos,
                                max(1, brush_size // 2)
                            )

        # Mouse movement
        if event.type == pygame.MOUSEMOTION:

            mouse_pos = event.pos
            pos = canvas_position(mouse_pos)

            if drawing and pos is not None:

                if current_tool == "Pencil":
                    pygame.draw.line(
                        canvas,
                        selected_color,
                        last_pos,
                        pos,
                        brush_size
                    )
                    last_pos = pos

                else:
                    shape_end = pos

        # Mouse button up
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            if drawing:

                mouse_pos = event.pos
                pos = canvas_position(mouse_pos)

                if pos is not None:

                    if current_tool == "Line":
                        pygame.draw.line(
                            canvas,
                            selected_color,
                            shape_start,
                            pos,
                            brush_size
                        )

                    elif current_tool not in ["Pencil", "Fill", "Text"]:
                        draw_shape(
                            canvas,
                            current_tool,
                            shape_start,
                            pos,
                            selected_color,
                            brush_size
                        )

            drawing = False
            shape_start = None
            shape_end = None
            last_pos = None

    # Draw canvas
    screen.fill((255, 255, 255))
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Shape preview
    if drawing and shape_start is not None and shape_end is not None:

        if current_tool == "Line":
            preview_start = (
                shape_start[0],
                shape_start[1] + TOOLBAR_HEIGHT
            )
            preview_end = (
                shape_end[0],
                shape_end[1] + TOOLBAR_HEIGHT
            )

            pygame.draw.line(
                screen,
                selected_color,
                preview_start,
                preview_end,
                brush_size
            )

        elif current_tool in [
            "Rectangle",
            "Circle",
            "Square",
            "Right Triangle",
            "Equilateral Triangle",
            "Rhombus"
        ]:
            preview_start = (
                shape_start[0],
                shape_start[1] + TOOLBAR_HEIGHT
            )
            preview_end = (
                shape_end[0],
                shape_end[1] + TOOLBAR_HEIGHT
            )

            draw_shape(
                screen,
                current_tool,
                preview_start,
                preview_end,
                selected_color,
                brush_size
            )

    # Text preview
    if text_active and text_position is not None:

        preview_text = text_font.render(
            text_input, True, selected_color
        )

        preview_screen_pos = (
            text_position[0],
            text_position[1] + TOOLBAR_HEIGHT
        )

        screen.blit(preview_text, preview_screen_pos)

        # Cursor
        cursor_x = preview_screen_pos[0] + preview_text.get_width()
        cursor_y = preview_screen_pos[1]

        pygame.draw.line(
            screen,
            selected_color,
            (cursor_x, cursor_y),
            (cursor_x, cursor_y + 25),
            2
        )

    # Toolbar
    draw_toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
