def mandelbrot_escape_iter(c: complex, max_iter: int = 80) -> int:
    """c noktası kaçıyorsa kaçıncı iterasyonda kaçtığını döner; kaçmazsa max_iter."""
    z = 0 + 0j
    for i in range(max_iter):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) > 4.0:  # |z|^2 > 4 => |z| > 2
            return i
    return max_iter


def iter_to_char(it: int, max_iter: int, palette: str = " .:-=+*#%@") -> str:
    """İterasyon sayısını palette içinden bir karaktere map eder."""
    if it >= max_iter:
        return " "  # içerideyse boş bırak (istersen '@' yap)
    # 0..max_iter-1 -> 0..len(palette)-1
    idx = int(it / max_iter * (len(palette) - 1))
    return palette[idx]


def print_mandelbrot_ascii(
    width: int = 120,
    height: int = 40,
    max_iter: int = 80,
    x_min: float = -2.2,
    x_max: float = 1.0,
    y_min: float = -1.2,
    y_max: float = 1.2,
    palette: str = " .:-=+*#%@"
) -> None:
    """Terminale ASCII Mandelbrot kümesi basar."""
    for row in range(height):
        # üstten alta doğru y
        y = y_max - (y_max - y_min) * row / (height - 1)
        line_chars = []
        for col in range(width):
            x = x_min + (x_max - x_min) * col / (width - 1)
            c = complex(x, y)
            it = mandelbrot_escape_iter(c, max_iter=max_iter)
            line_chars.append(iter_to_char(it, max_iter, palette))
        print("".join(line_chars))


# Çalıştır:
print_mandelbrot_ascii()
