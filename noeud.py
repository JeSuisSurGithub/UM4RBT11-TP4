import math
import matplotlib.pyplot as plt

OPERATOR = {
    "+": 2,
    "-": 2,
    "*": 2,
    "/": 2,

    "exp": 1,
    "log": 1,
    "sin": 1,
    "cos": 1
}

class Noeud:
    def __init__(self, val, enfants=None):
        self.val = val
        if enfants == None:
            self.enfants = []
        else:
            self.enfants = enfants


    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant)
        return self

    def affichage_polonais(self):
        print(self.val, end=" ")
        for e in self.enfants:
            e.affichage_polonais()
        return


    def tracer(self, target_x, vx):
        vy = []
        var2val = {target_x: None}
        for x in vx:
            var2val[target_x] = x
            vy.append(self.evaluer(var2val))

        title = f"evaluer_{id(self)}"
        plt.figure()
        plt.title(title)
        plt.grid()
        plt.plot(vx, vy)
        # plt.savefig(title)
        plt.show()

    def simplifiee(self):
        # On part du bas
        for enfant in self.enfants:
            enfant.simplifiee()

        op1, op2 = None,None
        if len(self.enfants) > 0:
            op1 = self.enfants[0].eval_float(noexcept=True)
        if len(self.enfants) > 1:
            op2 = self.enfants[1].eval_float(noexcept=True)

        # Produits
        if self.val == "*":
            if op1 == 0 or op2 == 0:
                self.val = 0.0
                self.enfants = list()
            if op1 == 1:
                self.val = self.enfants[1].val
                self.enfants = self.enfants[1].enfants
            elif op1 == 1:
                self.val = self.enfants[0].val
                self.enfants = self.enfants[0].enfants

        if self.val == "/":
            if op1 == 0:
                self.val = 0.0
                self.enfants = list()
            if op1 == 1:
                self.val = self.enfants[0].val
                self.enfants = self.enfants[0].enfants

        if self.val == "+":
            if op1 == 0:
                self.val = self.enfants[1].val
                self.enfants = self.enfants[1].enfants
            elif op2 == 0:
                self.val = self.enfants[0].val
                self.enfants = self.enfants[0].enfants

        if self.val == "-":
            if op2 == 0:
                self.val = self.enfants[0].val
                self.enfants = self.enfants[0].enfants

        if self.est_variable() == False:
            self.val = self.evaluer()
            self.enfants = list()

        return self

    def est_variable(self):
        if (self.val not in OPERATOR) and (self.eval_float(noexcept=True) == None):
            return True
        else:
            for enfant in self.enfants:
                return enfant.est_variable()

    def eval_float(self, noexcept=False):
        try:
            x = float(self.val)
            if len(self.enfants) != 0:
                print("Expression mal formée un noeud valeur possède des enfants")
            return x
        except ValueError:
            if noexcept == False:
                raise ValueError(f"Valeur de noeud n'est pas un réel ({self.val})")
            else:
                return None

    def evaluer(self, var2val):
        if self.val in OPERATOR:
            if (OPERATOR[self.val] != len(self.enfants)):
                print(f"Expression mal formée nombre incorrect d'enfants pour {self.val}, attendu {OPERATOR[self.val]} et reçu {len(self.enfants)}")

            op1 = self.enfants[0].evaluer(var2val)

            if self.val == "exp":
                return math.exp(op1)
            elif self.val == "log":
                return math.log(op1)
            elif self.val == "sin":
                return math.sin(op1)
            elif self.val == "cos":
                return math.cos(op1)

            op2 = self.enfants[1].evaluer(var2val)

            if self.val == "+":
                return op1 + op2
            elif self.val == "-":
                return op1 - op2
            elif self.val == "*":
                return op1 * op2
            elif self.val == "/":
                if op2 == 0:
                    raise ValueError("Division par zéro")
                return op1 / op2

        elif self.val in var2val:
            return var2val[self.val]
        else:
            return self.eval_float()