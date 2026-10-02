import noeud

variable = {"y": 10}

# a1 = noeud.Noeud("1")
# a2 = noeud.Noeud("2")
# a1.ajouter_enfant(noeud.Noeud("3"))
# a2.ajouter_enfant(noeud.Noeud("3"))

# print(a1.enfants)
# print(a2.enfants)

# exp(sin(2+y))
arb = noeud.Noeud("exp") \
    .ajouter_enfant(noeud.Noeud("sin")
        .ajouter_enfant(noeud.Noeud("+")
            .ajouter_enfant(noeud.Noeud("2"))
            .ajouter_enfant(noeud.Noeud("y"))))

arb.affichage_polonais()
print(arb.evaluer(variable))
# arb.tracer("y", [i / 100 for i in range(1, 5000, 1)])

# (((0 / (x * 0 + 1 * x)) / 1) - 0) + exp(0)
arb2 = noeud.Noeud("+") \
    .ajouter_enfant(noeud.Noeud("exp")
        .ajouter_enfant(noeud.Noeud("0"))) \
    .ajouter_enfant(noeud.Noeud("-")
        .ajouter_enfant(noeud.Noeud("/")
            .ajouter_enfant(noeud.Noeud("/"))
                .ajouter_enfant(noeud.Noeud("0"))
                .ajouter_enfant(noeud.Noeud("/")
                    .ajouter_enfant(noeud.Noeud("+")
                        .ajouter_enfant(noeud.Noeud("*")
                            .ajouter_enfant(noeud.Noeud("x"))
                            .ajouter_enfant(noeud.Noeud("0")))
                        .ajouter_enfant(noeud.Noeud("*")
                            .ajouter_enfant(noeud.Noeud("1"))
                            .ajouter_enfant(noeud.Noeud("x")))))
            .ajouter_enfant(noeud.Noeud("1")))
        .ajouter_enfant(noeud.Noeud("0")))
arb2.affichage_polonais()
print("")
arb2.simplifiee()
arb2.affichage_polonais()
