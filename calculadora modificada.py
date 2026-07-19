import tkinter as tk
import math


class CalculadoraCientifica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.geometry("550x750")
        self.root.minsize(450, 650)
        self.root.configure(bg="#121212")

        self.ultimo_calculo = tk.StringVar()
        self.expressao = tk.StringVar()

        # Histórico
        tk.Label(
            root,
            textvariable=self.ultimo_calculo,
            bg="#121212",
            fg="#888888",
            anchor="e",
            font=("Segoe UI", 12)
        ).pack(fill="x", padx=20, pady=(15, 0))

        # Visor
        visor = tk.Entry(
            root,
            textvariable=self.expressao,
            font=("Segoe UI", 28, "bold"),
            justify="right",
            bg="#1E1E1E",
            fg="white",
            bd=0,
            insertbackground="white"
        )
        visor.pack(fill="x", padx=20, pady=10, ipady=20)

        self.root.bind("<Return>", lambda e: self.calcular())
        self.root.bind("<Escape>", lambda e: self.limpar())

        frame = tk.Frame(root, bg="#121212")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        botoes = [
            ["sin(", "cos(", "tan(", "√", "C"],
            ["log(", "ln(", "π", "e", "←"],
            ["(", ")", "^", "!", "/"],
            ["7", "8", "9", "*", "%"],
            ["4", "5", "6", "-", "1/x"],
            ["1", "2", "3", "+", "x²"],
            ["0", ".", "±", "="]
        ]

        for linha in range(len(botoes)):
            frame.grid_rowconfigure(linha, weight=1)

        for coluna in range(5):
            frame.grid_columnconfigure(coluna, weight=1)

        for l, linha in enumerate(botoes):
            for c, texto in enumerate(linha):

                if texto == "=":
                    cor = "#00C853"
                elif texto in ["+", "-", "*", "/", "^", "%"]:
                    cor = "#FF9800"
                elif texto in ["C", "←"]:
                    cor = "#D32F2F"
                elif texto in [
                    "sin(", "cos(", "tan(",
                    "log(", "ln(", "√",
                    "π", "e", "!",
                    "1/x", "x²"
                ]:
                    cor = "#2962FF"
                else:
                    cor = "#2D2D2D"

                btn = tk.Button(
                    frame,
                    text=texto,
                    font=("Segoe UI", 16, "bold"),
                    bg=cor,
                    fg="white",
                    relief="flat",
                    bd=0,
                    activebackground="#555555",
                    activeforeground="white",
                    cursor="hand2",
                    command=lambda t=texto: self.clique(t)
                )

                if l == 6 and texto == "=":
                    btn.grid(
                        row=l,
                        column=c,
                        columnspan=2,
                        sticky="nsew",
                        padx=4,
                        pady=4
                    )
                else:
                    btn.grid(
                        row=l,
                        column=c,
                        sticky="nsew",
                        padx=4,
                        pady=4
                    )

    def clique(self, valor):

        if valor == "=":
            self.calcular()
            return

        if valor == "C":
            self.limpar()
            return

        if valor == "←":
            self.expressao.set(self.expressao.get()[:-1])
            return

        if valor == "π":
            self.expressao.set(self.expressao.get() + "pi")
            return

        if valor == "√":
            self.expressao.set(self.expressao.get() + "sqrt(")
            return

        if valor == "x²":
            self.expressao.set(self.expressao.get() + "**2")
            return

        if valor == "1/x":
            self.expressao.set("1/(" + self.expressao.get() + ")")
            return

        if valor == "±":
            atual = self.expressao.get()
            if atual.startswith("-"):
                self.expressao.set(atual[1:])
            else:
                self.expressao.set("-" + atual)
            return

        self.expressao.set(self.expressao.get() + valor)

    def limpar(self):
        self.expressao.set("")

    def calcular(self):
        try:
            expr = self.expressao.get()

            self.ultimo_calculo.set(expr)

            expr = expr.replace("^", "**")

            if expr.endswith("!"):
                numero = int(expr[:-1])
                resultado = math.factorial(numero)

            else:
                ambiente = {
                    "__builtins__": {},
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "sqrt": math.sqrt,
                    "log": math.log10,
                    "ln": math.log,
                    "pi": math.pi,
                    "e": math.e,
                    "abs": abs
                }

                resultado = eval(expr, ambiente)

            if isinstance(resultado, float):
                resultado = round(resultado, 12)

            self.expressao.set(str(resultado))

        except Exception:
            self.expressao.set("Erro")


if __name__ == "__main__":
    root = tk.Tk()
    CalculadoraCientifica(root)
    root.mainloop()