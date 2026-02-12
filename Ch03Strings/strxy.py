# y = x ASCII grafiği (fonksiyon yok)

width = 41
height = 21

x_min, x_max = -10, 10
y_min, y_max = -10, 10

# boş alan
grid = [[" " for _ in range(width)] for _ in range(height)]

# eksenler
# y=0 satırı
y0_row = int(round((y_max - 0) / (y_max - y_min) * (height - 1)))
for c in range(width):
    grid[y0_row][c] = "-"

# x=0 sütunu
x0_col = int(round((0 - x_min) / (x_max - x_min) * (width - 1)))
for r in range(height):
    grid[r][x0_col] = "|"

grid[y0_row][x0_col] = "+"  # kesişim

# y=x çizgisi
for col in range(width):
    x = x_min + (x_max - x_min) * col / (width - 1)
    y = x
    row = int(round((y_max - y) / (y_max - y_min) * (height - 1)))
    if 0 <= row < height:
        grid[row][col] = "*"

# yazdır
for row in grid:
    print("".join(row))
