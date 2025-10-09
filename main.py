import math
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
class DrawTrapezoid:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(self.root)
        self.root.geometry("500x600")
        self.label_A = ttk.Label(self.frame, text="Вершина A    x:")
        self.label_A.grid(column=0, row=0, padx="10", pady="10")
        self.label_B = ttk.Label(self.frame, text="Вершина B    x:")
        self.label_B.grid(column=0, row=1, padx="10", pady="10")
        self.label_C = ttk.Label(self.frame, text="Вершина C    x:")
        self.label_C.grid(column=0, row=2, padx="10", pady="10")
        self.label_line = ttk.Label(self.frame, text="Длина ср. линии")
        self.label_line.grid(column=0, row=3, padx="10", pady="10")
        self.entry_Ax = ttk.Entry(self.frame, width=4)
        self.entry_Ax.grid(column=1, row=0)
        self.entry_Bx = ttk.Entry(self.frame, width=4)
        self.entry_Bx.grid(column=1, row=1)
        self.entry_Cx = ttk.Entry(self.frame, width=4)
        self.entry_Cx.grid(column=1, row=2)
        self.entry_length = ttk.Entry(self.frame, width=4)
        self.entry_length.grid(column=1, row=3)
        self.label_Ay = ttk.Label(self.frame, text="y:")
        self.label_By = ttk.Label(self.frame, text="y:")
        self.label_Cy = ttk.Label(self.frame, text="y:")
        self.label_Ay.grid(column=2, row=0, padx="5")
        self.label_By.grid(column=2, row=1, padx="5")
        self.label_Cy.grid(column=2, row=2, padx="5")
        self.entry_Ay = ttk.Entry(self.frame, width=4)
        self.entry_Ay.grid(column=3, row=0)
        self.entry_By = ttk.Entry(self.frame, width=4)
        self.entry_By.grid(column=3, row=1)
        self.entry_Cy = ttk.Entry(self.frame, width=4)
        self.entry_Cy.grid(column=3, row=2)
        self.button_load = ttk.Button(self.frame, text="Загрузить из svg", command=self.read_svg)
        self.button_load.grid(column=4, row=0, padx="30")
        self.button_create = ttk.Button(self.frame, text="Создать", command=self.create_trapezoid)
        self.button_create.grid(column=4, row=1, padx="30")
        self.button_save = ttk.Button(self.frame, text="Сохранить", command=self.save)
        self.button_save.grid(column=4, row=2, padx="30")
        self.frame.pack()
        self.width = 200
        self.height = 200
        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_cda = tk.Canvas(self.canvas_frame, width=self.width, height=self.height, bg="white")
        self.canvas_brezf = tk.Canvas(self.canvas_frame, width=self.width, height=self.height, bg="white")
        self.canvas_brezi = tk.Canvas(self.canvas_frame, width=self.width, height=self.height, bg="white")
        self.canvas_python = tk.Canvas(self.canvas_frame, width=self.width, height=self.height, bg="white")
        self.canvas_cda.grid(column=0, row=0)
        self.canvas_brezf.grid(column=0, row=1)
        self.canvas_brezi.grid(column=1, row=0)
        self.canvas_python.grid(column=1, row=1)
        self.canvas_frame.pack()
        self.pbm_set = set()

    def read_svg(self):
        file_path = filedialog.askopenfilename(
            title="Выберите SVG файл",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
        )
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
        coords = lines[1].split()
        A = tuple(map(float, coords[0].split(',')))
        B = tuple(map(float, coords[1].split(',')))
        C = tuple(map(float, coords[2].split(',')))
        length = float(lines[2])
        self.entry_Ax.delete(0, "end")
        self.entry_Ay.delete(0, "end")
        self.entry_Bx.delete(0, "end")
        self.entry_By.delete(0, "end")
        self.entry_Cx.delete(0, "end")
        self.entry_Cy.delete(0, "end")
        self.entry_length.delete(0, "end")

        self.entry_Ax.insert(0, str(A[0]))
        self.entry_Ay.insert(0, str(A[1]))
        self.entry_Bx.insert(0, str(B[0]))
        self.entry_By.insert(0, str(B[1]))
        self.entry_Cx.insert(0, str(C[0]))
        self.entry_Cy.insert(0, str(C[1]))
        self.entry_length.insert(0, str(length))

        showinfo("Успех", "Данные из SVG успешно загружены.")
    def get_values(self):
        try:
            Ax = float(self.entry_Ax.get())
            Ay = float(self.entry_Ay.get())
            Bx = float(self.entry_Bx.get())
            By = float(self.entry_By.get())
            Cx = float(self.entry_Cx.get())
            Cy = float(self.entry_Cy.get())
            length = float(self.entry_length.get())
            return (Ax, Ay), (Bx, By), (Cx, Cy), length
        except ValueError:
            return None

    def calculate_top(self):
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        A, B, C, length = self.get_values()
        len_AB = math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)
        len_CD = 2 * length - len_AB
        e = ((B[0]-A[0]) / len_AB, (B[1]-A[1]) / len_AB)
        vec = (e[0] * len_CD, e[1] * len_CD)
        v1 = (C[0] + vec[0], C[1] + vec[1])
        v2 = (C[0] - vec[0], C[1] - vec[1])
        D = v1 if cross(A, B, C) * cross(B, C, v1) > 0 else v2
        return [A, B, C, D]

    def sign(self, a):
        if a > 0:
            return 1
        elif a == 0:
            return 0
        else:
            return -1

    def cda(self, s, e):
        if s[0] - e[0] == 0 and s[1] - e[1] == 0:
            return

        L = abs(e[0] - s[0]) if abs(e[0] - s[0]) >= abs(e[1] - s[1]) else abs(e[1] - s[1])
        dx = (e[0] - s[0]) / L
        dy = (e[1] - s[1]) / L
        x = s[0] + 0.5 * self.sign(dx)
        y = s[1] + 0.5 * self.sign(dy)
        for i in range(1, int(L) + 1):
            self.canvas_cda.create_oval(math.floor(x), math.floor(y), math.floor(x), math.floor(y), fill="black")
            self.pbm_set.add((math.floor(x), math.floor(y)))
            x = x + dx
            y = y + dy

    def brezf(self, s, e):
        if s[0] - e[0] == 0 and s[1] - e[1] == 0:
            return

        dx, dy = e[0] - s[0], e[1] - s[1]
        sx, sy = self.sign(dx), self.sign(dy)
        dx, dy = abs(dx), abs(dy)
        flag = 0
        if dy > dx:
            dx, dy = dy, dx
            flag = 1
        f = dy/dx - 0.5
        x, y = s[0], s[1]
        for i in range(int(dx) + 1):
            self.canvas_brezf.create_oval(math.floor(x), math.floor(y), math.floor(x), math.floor(y), fill="black")
            if f >= 0:
                if flag:
                    x += sx
                else:
                    y += sy
                f -= 1
            if flag:
                y += sy
            else:
                x += sx
            f += dy/dx

    def brezi(self, s, e):
        if s[0] - e[0] == 0 and s[1] - e[1] == 0:
            return

        sx = self.sign(e[0] - s[0])
        sy = self.sign(e[1] - s[1])
        dx = abs(e[0] - s[0])
        dy = abs(e[1] - s[1])
        x = s[0]
        y = s[1]
        flag = 0
        if dy > dx:
            dx, dy = dy, dx
            flag = 1
        f = 2 * dy - dx
        for i in range(int(dx) + 1):
            self.canvas_brezi.create_oval(math.floor(x), math.floor(y), math.floor(x), math.floor(y), fill="black")
            if f >= 0:
                if flag:
                    x += sx
                else:
                    y += sy
                f = f - 2 * dx
            if flag:
                y += sy
            else:
                x += sx
            f = f + 2*dy

    def python_line(self, s, e):
        self.canvas_python.create_line(s[0], s[1], e[0], e[1], fill="black")

    def create_trapezoid(self):
        tops = self.calculate_top()
        self.canvas_python.delete("all")
        self.canvas_cda.delete("all")
        self.canvas_brezf.delete("all")
        self.canvas_brezi.delete("all")
        self.pbm_set.clear()
        for i in range(-1, len(tops) - 1):
            self.cda(tops[i], tops[i + 1])
            self.brezf(tops[i], tops[i + 1])
            self.brezi(tops[i], tops[i + 1])
            self.python_line(tops[i], tops[i + 1])
        
    def save(self):
        if len(self.pbm_set) == 0:
            print("Нет данных для сохранения!")
            return

        file_path = filedialog.asksaveasfilename(
            title="Сохранить PBM файл",
            defaultextension=".pbm",
            filetypes=[("PBM files", "*.pbm")]
        )
        if not file_path:
            return
        with open(file_path, 'w') as file:
            file.write("P1\n")
            file.write(f"{self.width} {self.height}\n")
            for y in range(self.height):
                for x in range(self.width):
                    value = 1 if (x, y) in self.pbm_set else 0
                    file.write(f"{value} ")
                file.write("\n")
        showinfo("Успех", "PBM файл успешно сохранен")

def main():
    root = tk.Tk()
    app = DrawTrapezoid(root)
    root.mainloop()

if __name__ == "__main__":
    main()
