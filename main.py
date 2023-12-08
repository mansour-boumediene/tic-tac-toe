from tkinter import *

root = Tk()
root.geometry("500x500")
root.title("Tic Tac Toe")
root.configure(bg="blue")

frame1 = Frame(root)
frame1.pack()

frame2 = Frame(root)
frame2.pack()

canvas = Canvas(root, width=200, height=100)
canvas.pack()

turn = "X"
game_over = False


def verifier_victoire(symbole):

    for i in range(3):
        if (frame2.grid_slaves(row=i, column=0)[0]["text"] == symbole and
                frame2.grid_slaves(row=i, column=1)[0]["text"] == symbole and
                frame2.grid_slaves(row=i, column=2)[0]["text"] == symbole):
            return True
        if (frame2.grid_slaves(row=0, column=i)[0]["text"] == symbole and
                frame2.grid_slaves(row=1, column=i)[0]["text"] == symbole and
                frame2.grid_slaves(row=2, column=i)[0]["text"] == symbole):
            return True
    if (frame2.grid_slaves(row=0, column=0)[0]["text"] == symbole and
            frame2.grid_slaves(row=1, column=1)[0]["text"] == symbole and
            frame2.grid_slaves(row=2, column=2)[0]["text"] == symbole):
        return True
    if (frame2.grid_slaves(row=0, column=2)[0]["text"] == symbole and
            frame2.grid_slaves(row=1, column=1)[0]["text"] == symbole and
            frame2.grid_slaves(row=2, column=0)[0]["text"] == symbole):
        return True
    return False


def recommencer_partie():
    global game_over
    for btn in frame2.winfo_children():
        btn["text"] = " "
    canvas.delete("all")
    game_over = False


def jouer(event):
    global turn, game_over
    button = event.widget
    if not game_over and button["text"] == " ":
        if turn == "X":
            button["text"] = "X"
            turn = "O"
        else:
            button["text"] = "O"
            turn = "X"

        if verifier_victoire("X"):
            canvas.create_text(100, 25, text="Le joueur X a gagné!", fill="green", font=("Arial", 12, "bold"))
            canvas.create_text(100, 50, text="Recommencer la partie", fill="blue", font=("Arial", 10), tags="restart")
            canvas.tag_bind("restart", "<Button-1>", lambda event: recommencer_partie())
            game_over = True
        elif verifier_victoire("O"):
            canvas.create_text(100, 25, text="Le joueur O a gagné!", fill="green", font=("Arial", 12, "bold"))
            canvas.create_text(100, 50, text="Recommencer la partie", fill="blue", font=("Arial", 10), tags="restart")
            canvas.tag_bind("restart", "<Button-1>", lambda event: recommencer_partie())
            game_over = True
        elif " " not in [btn["text"] for btn in frame2.winfo_children()]:
            canvas.create_text(100, 25, text="Match nul!", fill="orange", font=("Arial", 12, "bold"))
            canvas.create_text(100, 50, text="Recommencer la partie", fill="blue", font=("Arial", 10), tags="restart")
            canvas.tag_bind("restart", "<Button-1>", lambda event: recommencer_partie())
            game_over = True


for i in range(3):
    for j in range(3):
        btn = Button(frame2, text=" ", width=8, height=10)
        btn.grid(row=i, column=j)
        btn.bind("<Button-1>", jouer)

root.mainloop()