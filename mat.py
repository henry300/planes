from random import randint
from tkinter import *
from tkinter import ttk
init = Tk()
init.destroy()

class Raam:
    def __init__(self):
        self.raam = Tk()
        self.raam.configure(background="#ececec")
        self.värv = self.raam.cget("background")
        self.raam.title("Helikopterite kuulid")
        self.w = 300
        self.h = 200

    def render_raam(self):
        ws = self.raam.winfo_screenwidth()
        hs = self.raam.winfo_screenheight()
        x = (ws/2) - (self.w/2)
        y = (hs/2) - (self.h/2)
        self.raam.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

class Stopper:
    def __init__(self, raam):
        self.label = ttk.Label(text="", font=("Calibri", 22), foreground = "black")
        self.label.place(x = 10, y = 10)
        self.raam = raam.raam
        self.moreTime = True
        self.n = 30

    def uuenda_stopper(self):
        self.n -= 1
        self.label.configure(text=self.n)
        self.raam.after(1000, self.uuenda_stopper)
        if self.n < 0:
            self.raam.destroy()

class arvamismang:
    def __init__(self, aken, stopper):
        self.raam = aken.raam
        self.tekts1 = ''
        self.tekts2 = ''
        self.nupp1 = ''
        self.nupp2 = ''
        self.input_field = ''
        self.oige = ''
        self.skoor = 0
        self.stopper = stopper
        self.inglise_k = []
        self.eesti_k = []
        self.sona_ekraanile = ''
        self.max_kuulid = 50

    def lõpeta_mäng(self):
        print('tra')

    def mangija_vastus(self):
        mängija_vastus = self.input_field.get()
        try:
            return int(mängija_vastus)
        except:
            return str(mängija_vastus)

    def võrdle(self, event):
        mängija = self.mangija_vastus()

        if mängija == self.oige:
            hindaja = ttk.Label(self.raam, text = "ÕIGE! ", font=("Calibri", 25), foreground = "#00AA00")
            if self.skoor < self.max_kuulid:
                if type(self.oige) == int:
                    self.skoor += 15
                else:
                    self.skoor += 20
        else:
            hindaja = ttk.Label(self.raam, text = "VALE!", font=("Calibri", 25), foreground = "#AA0000")
            if self.skoor == 0:
                pass
            else:
                self.skoor -= 1
        hindaja.place(x = 115, y = 150)
        skoorinäit = ttk.Label(self.raam, text = "  Uued kuulid: " + str(self.skoor) + "  ", font=("Calibri", 15, 'bold'), foreground = "black")
        skoorinäit.place(relx = 0.5, rely = 0.12, anchor = S)
        self.input_field.delete(0, END)
        if type(self.oige) == int:
            self.oige = self.loo_matemaatiline_tehe()
        else:
            self.oige = self.inglise_keelne_tehe()

    def render_welcome_screen(self):
        self.tekst1 = ttk.Label(self.raam, text = "Sinu kuulid said otsa!", justify="center", font=("Calibri", 22))
        self.tekst2 = ttk.Label(self.raam, text = "Jätkamiseks vali ühele ülesannetest \nja vasta nii palju kui jõuad!", justify="center", font=("Calibri", 16))
        self.tekst1.place(x = 50, y = 10)
        self.tekst2.place(x = 20, y = 40)
        self.nupp1 = Button(self.raam, text = "Matemaatika", background = "light grey", activebackground = "light green",command = self.alusta_mang_matemaatika)
        self.nupp2 = Button(self.raam, text = "Inglise keel", background = "light grey", activebackground = "light green", command = self.alusta_mang_inglisekeel)
        self.nupp1.place(x = 35, y = 120)
        self.nupp2.place(x = 160, y = 120)

    def remove_welcome_screen(self):
        self.tekst1.destroy()
        self.tekst2.destroy()
        self.nupp1.destroy()
        self.nupp2.destroy()

    def alusta_mang_inglisekeel(self):
        self.remove_welcome_screen()
        self.raam.bind_all("<Return>", self.võrdle)


        self.input_field = ttk.Entry(self.raam)
        self.input_field.place(x = 50, y = 115, width = 200)
        #võtab faili ja teeb sellest listi
        f= open("projekti_sonad.txt")
        for rida in f:
            try:
                sonad = rida.split("\t")
                self.inglise_k.append(sonad[0].strip().lower())
                self.eesti_k.append(sonad[1].strip().lower())
            except:
                pass
        f.close()
        self.oige = self.inglise_keelne_tehe()
        self.stopper.uuenda_stopper()

    def alusta_mang_matemaatika(self):
        self.remove_welcome_screen()
        self.raam.bind_all("<Return>", self.võrdle)

        self.input_field = ttk.Entry(self.raam)
        self.input_field.place(x = 50, y = 115, width = 200)
        self.oige = self.loo_matemaatiline_tehe()
        self.stopper.uuenda_stopper()

    def inglise_keelne_tehe(self):
        suvaline_arv = randint(0, len(self.eesti_k)-1)

        try:
            self.sona_ekraanile.destroy()
        except:
            pass
        self.sona_ekraanile = ttk.Label(self.raam, text = self.eesti_k[suvaline_arv], font=("Calibri", 16))
        self.sona_ekraanile.place(relx = 0.5, rely = 0.3, anchor = CENTER)
        tolge = self.inglise_k[suvaline_arv]
        return tolge

    def loo_matemaatiline_tehe(self):
        # genereerib suvalise matemaatilise tehte
        tehe = randint(0,3)
        arv1 = randint(1,20)
        arv2 = randint(1,15)
        lõputehe = ""
        vastus = ""
        if tehe == 3:
            vastus = self.huvitavad_tehted()
        elif arv1 % arv2 == 0:
            lõputehe = (str(arv1)+" / "+str(arv2))
            vastus = arv1/arv2
        elif arv2 % arv1 == 0:
            lõputehe = (str(arv2)+" / "+str(arv1))
            vastus = arv2/arv1
        elif tehe == 0:
            lõputehe = (str(arv1)+" + "+str(arv2))
            vastus = arv1 + arv2
        elif tehe == 1:
            lõputehe = (str(arv1)+" - "+str(arv2))
            vastus = arv1 - arv2
        elif tehe == 2:
            lõputehe = (str(arv1)+" x "+str(arv2))
            vastus = arv1 * arv2

        # lasen tehted raamile kirjutada
        tühikud = "      "
        if lõputehe != "":
            tehe_ekraanile = ttk.Label(self.raam, text = tühikud + lõputehe + tühikud, font=("Calibri", 22))
            tehe_ekraanile.place(relx = 0.5, rely = 0.35, anchor = CENTER)
        return int(vastus)

    def huvitavad_tehted(self):
        tühikud = "        "
        suvaline = randint(0,14)
        huvitavad = ["sin π","cos π","tan 0","cot π","2sin(π/6)", "2cos(π/3)","sin 2π","cos 2π","sin (3π/2)", "cos(3π/2)", "tan (π/4)","sin(30°+60°)","cos(60°+30°)","2sin 30°",
                     "2cos 60°"]
        huvitavad_vastused  = [0,1,0,0,1,1,0,1,-1,0,1,1,0,1,1]
        huvitav_tehe = ttk.Label(self.raam, text = tühikud + huvitavad[suvaline] + tühikud, font=("Calibri", 22))
        huvitav_tehe.place(relx = 0.5, rely = 0.35, anchor = CENTER)
        return int(huvitavad_vastused[suvaline])

    def start_loop(self):
        self.raam.mainloop()

def arva():
    raam = Raam()
    raam.render_raam()

    stopper = Stopper(raam)
    mang = arvamismang(raam, stopper)
    mang.render_welcome_screen()
    mang.start_loop()
    return mang.skoor


