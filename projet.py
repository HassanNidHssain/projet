# Si le calcul original utilisait 0,025 au lieu de 0,25, cela produirait un résultat
# plus proche de l'erreur de 1,6 % annoncée. Ce code utilise la valeur correcte
# (x_A = 0,25), ce qui donne un calcul plus précis mais une erreur différente (-3,3 %).
# Pour reproduire l'erreur de 1,6 %, remplacez (phi_A / x_A) par (phi_A / 0,025)
# dans le calcul de term2_part.
import math
import ipywidgets as widgets
from IPython.display import display

# Fonction pour calculer D_AB
def calculate_dab(x_A, T):
    try:
        # Paramètres fixes (affichés mais non modifiables)
        a_AB = -10.7575
        a_BA = 194.5302
        r_A = 1.4311
        r_B = 0.92
        q_A = 1.432
        q_B = 1.4
        D0_AB = 2.10e-5
        D0_BA = 2.67e-5
        exp_D_AB = 1.33e-5

        x_B = 1 - x_A

        # Calculs intermédiaires
        sum_xr = x_A * r_A + x_B * r_B
        phi_A = (x_A * r_A) / sum_xr
        phi_B = (x_B * r_B) / sum_xr

        sum_xq = x_A * q_A + x_B * q_B
        theta_A = (x_A * q_A) / sum_xq
        theta_B = (x_B * q_B) / sum_xq

        tau_AB = math.exp(-a_AB / T)
        tau_BA = math.exp(-a_BA / T)

        lambda_A = r_A ** (1/3)
        lambda_B = r_B ** (1/3)

        # Theta_ji calculations (with assumed τ_AA = τ_BB = 1)
        tau_AA = 1.0
        tau_BB = 1.0
        theta_BA = (theta_B * tau_BA) / (theta_A * tau_AA + theta_B * tau_BA)
        theta_AB = (theta_A * tau_AB) / (theta_A * tau_AB + theta_B * tau_BB)
        theta_AA = (theta_A * tau_AA) / (theta_A * tau_AA + theta_B * tau_BA)
        theta_BB = (theta_B * tau_BB) / (theta_A * tau_AB + theta_B * tau_BB)

        # Calculate all terms
        term1 = x_B * math.log(D0_AB) + x_A * math.log(D0_BA)
        term2 = 2 * (x_A * math.log(x_A / phi_A) + x_B * math.log(x_B / phi_B))
        term3 = 2 * x_A * x_B * ((phi_A / x_A) * (1 - lambda_A / lambda_B) + (phi_B / x_B) * (1 - lambda_B / lambda_A))
        term4 = x_B * q_A * ((1 - theta_BA**2) * math.log(tau_BA) + (1 - theta_BB**2) * tau_AB * math.log(tau_AB))
        term5 = x_A * q_B * ((1 - theta_AB**2) * math.log(tau_AB) + (1 - theta_AA**2) * tau_BA * math.log(tau_BA))

        ln_DAB = term1 + term2 + term3 + term4 + term5
        DAB = math.exp(ln_DAB)
        error = ((DAB - exp_D_AB) / exp_D_AB) * 100

        # Afficher les résultats
        print(f"=== Résultats ===")
        print(f"Calculated D_AB: {DAB:.3e} cm²/s")
        print(f"Experimental D_AB: {exp_D_AB:.3e} cm²/s")
        print(f"Percentage Error: {error:.2f}%")

    except Exception as e:
        print(f"Erreur : {str(e)}")

# Créer des widgets pour x_A et T
x_A = widgets.FloatText(value=0.25, description='x_A:', step=0.01)
T = widgets.FloatText(value=313.13, description='T (K):', step=0.1)

# Afficher les autres paramètres (non modifiables)
params_frame = widgets.VBox([
    widgets.Label(value="=== Autres Paramètres ==="),
    widgets.FloatText(value=-10.7575, description='a_AB:', disabled=True),
    widgets.FloatText(value=194.5302, description='a_BA:', disabled=True),
    widgets.FloatText(value=1.4311, description='r_A:', disabled=True),
    widgets.FloatText(value=0.92, description='r_B:', disabled=True),
    widgets.FloatText(value=1.432, description='q_A:', disabled=True),
    widgets.FloatText(value=1.4, description='q_B:', disabled=True),
    widgets.FloatText(value=2.10e-5, description='D⁰_AB:', disabled=True),
    widgets.FloatText(value=2.67e-5, description='D⁰_BA:', disabled=True),
    widgets.FloatText(value=1.33e-5, description='Exp D_AB:', disabled=True)
])

# Bouton pour lancer le calcul
calculate_button = widgets.Button(description="Calculer")

# Fonction pour gérer le clic sur le bouton
def on_calculate_button_clicked(b):
    calculate_dab(x_A.value, T.value)

# Associer la fonction au bouton
calculate_button.on_click(on_calculate_button_clicked)

# Afficher tous les widgets
display(widgets.VBox([x_A, T, params_frame, calculate_button]))
