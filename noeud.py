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
    """ Noeud
    Attributs
    --------
    val: int
        Valeur ou étiquette du noeud
    enfants: list[Noeud]
        Liste des enfants de ce noeud
    """
    def __init__(self, val, enfants=None):
        self.val = val
        if enfants == None:
            self.enfants = []
        else:
            self.enfants = enfants

    """ajouter_enfant
    Ajoute un noeud enfant au noeud actuel

    Paramètres
    --------
    enfant: Noeud
        Enfant à ajouter au noeud
    Retourne
    --------
    Noeud, le noeud lui-même après ajout
    """
    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant)
        return self

    """affichage_polonais
    Effectue l'affichage polonais dans le terminal

    Paramètres
    --------
    Aucun

    Retourne
    --------
    Aucun
    """
    def affichage_polonais(self):
        print(self.val, end=" ")
        for e in self.enfants:
            e.affichage_polonais()
        return

    """tracer
    Trace la fonction avec matplotlib sur les X donnés

    Paramètres
    --------
    target_x: str
        Nom dans l'expression de la variable en abscisse
    vx: list[float]
        Liste des valeurs que prendra la variable en abscisse

    Retourne
    --------
    Aucun
    """
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

    """simplifiee
    Tente de simplifier l'expression dans le sous-arbre

    Paramètres
    --------
    Aucun

    Retourne
    --------
    L'arbre lui-même
    """
    def simplifiee(self):
        # On part du bas
        for i in range(len(self.enfants)):
            self.enfants[i] = self.enfants[i].simplifiee()

        op1, op2 = None,None

        if len(self.enfants) > 0:
            op1 = self.enfants[0].eval_float(noexcept=True)

        if len(self.enfants) > 1:
            op2 = self.enfants[1].eval_float(noexcept=True)

        print(f"val={self.val}, enfants={self.enfants}, op1={op1}, op2={op2}")
        debug = self.est_variable()

        # Produits
        if self.val == "*":
            if op1 == 0 or op2 == 0:
                self.val = 0.0
                self.enfants = list()
            if op1 == 1:
                self.val = self.enfants[1].val
                self.enfants = self.enfants[1].enfants
            elif op2 == 1:
                self.val = self.enfants[0].val
                self.enfants = self.enfants[0].enfants

        elif self.val == "/":
            if op1 == 0:
                self.val = 0.0
                self.enfants = list()
            if op2 == 1:
                self.val = self.enfants[0].val
                self.enfants = self.enfants[0].enfants

        elif self.val == "+":
            if op1 == 0:
                self.val = self.enfants[1].val
                self.enfants = self.enfants[1].enfants
            elif op2 == 0:
                self.val = self.enfants[0].val
                self.enfants = self.enfants[0].enfants

        elif self.val == "-":
            if op2 == 0:
                self.val = self.enfants[0].val
                self.enfants = self.enfants[0].enfants

        elif debug == False:
            self.val = self.evaluer({})
            self.enfants = list()

        print(f"val={self.val} enfants={self.enfants}, debug={debug}\n----")

        return self

    """est_variable
    Indique si l'expression contient des inconnues dans le sous-arbre

    Paramètres
    --------
    Aucun

    Retourne
    --------
    True si oui il y a dépendance sur des inconnues, False sinon et None si il n'as pas d'enfants
    """
    def est_variable(self):
        if (self.val not in OPERATOR) and (self.eval_float(noexcept=True) == None):
            return True
        else:
            res = None
            for enfant in self.enfants:
                if res == None:
                    return False
                res = res or enfant.est_variable()
            return res

    """eval_float
    Tente de voir si la valeur directe du noeud est un réel

    Paramètres
    --------
    noexcept: bool
        Si False, lève une erreur si ce n'est pas un réel
        Si True, ne lève pas d'erreur, retournera None

    Lève:
    --------
    ValueError, quand noexcept=False et que la valeur n'est pas un réel

    Retourne
    --------
    La valeur du noeud si c'ets bien un réel. Si noexcept=True retourne None si c'est une variable, fonction ou opérateur.
    """
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

    """evaluer
    Evalue l'expression pour les variables données

    Paramètres
    --------
    var2val: dict[str, float]
        Dictionnaire des nom de variables et leur valeur réelles par lesquels les remplacer

    Lève
    --------
    ValueError: Si il un élement dans l'arbre est ni un opérateur ou fonction connue (voir OPERATOR), ni une variable dont la valeur a été spécifiée (voir paramètres) ou ni réel valide

    Retourne
    --------
    L'expression évalué pour les variables données
    """
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