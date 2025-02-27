import math
import tkinter as tk
from tkinter import ttk, messagebox

class DiffusionCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Diffusion Coefficient Calculator")
        self.root.geometry("600x700")
        
        self.create_widgets()
        self.set_default_values()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Input parameters frame
        input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding=10)
        input_frame.pack(fill='both', expand=True, pady=5)
        
        # Parameter entries with units
        self.params = [
            ("Mole fraction of component A (x_A):", "-", "0.25"),
            ("Temperature (T) [K]:", "K", "313.13"),
            ("Adjustable parameter a_AB:", "-", "-10.7575"),
            ("Adjustable parameter a_BA:", "-", "194.5302"),
            ("Volume parameter r_A:", "-", "1.4311"),
            ("Volume parameter r_B:", "-", "0.92"),
            ("Surface area parameter q_A:", "-", "1.432"),
            ("Surface area parameter q_B:", "-", "1.4"),
            ("D⁰_AB [cm²/s]:", "cm²/s", "2.10e-5"),
            ("D⁰_BA [cm²/s]:", "cm²/s", "2.67e-5"),
            ("Experimental D_AB [cm²/s]:", "cm²/s", "1.33e-5")
        ]
        
        self.entries = {}
        for i, (label, unit, default) in enumerate(self.params):
            row = ttk.Frame(input_frame)
            row.grid(row=i, column=0, sticky='ew', pady=2)
            
            ttk.Label(row, text=label, width=30, anchor='w').pack(side='left')
            entry = ttk.Entry(row)
            entry.insert(0, default)
            entry.pack(side='left', fill='x', expand=True)
            ttk.Label(row, text=unit, width=5).pack(side='left')
            
            self.entries[label] = entry
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Help", command=self.show_help).pack(side='left', padx=5)
        
        # Results frame
        self.result_frame = ttk.LabelFrame(main_frame, text="Results", padding=10)
        self.result_frame.pack(fill='both', expand=True)
        
        self.result_text = tk.Text(self.result_frame, height=10, width=70)
        self.result_text.pack()
        
    def set_default_values(self):
        for label, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, self.params[[p[0] for p in self.params].index(label)][2])
    
    def get_float(self, label):
        try:
            return float(self.entries[label].get())
        except ValueError:
            messagebox.showerror("Input Error", f"Invalid value for {label.split(':')[0]}")
            return None
    
    def calculate(self):
        try:
            # Get input values
            x_A = self.get_float("Mole fraction of component A (x_A):")
            T = self.get_float("Temperature (T) [K]:")
            a_AB = self.get_float("Adjustable parameter a_AB:")
            a_BA = self.get_float("Adjustable parameter a_BA:")
            r_A = self.get_float("Volume parameter r_A:")
            r_B = self.get_float("Volume parameter r_B:")
            q_A = self.get_float("Surface area parameter q_A:")
            q_B = self.get_float("Surface area parameter q_B:")
            D0_AB = self.get_float("D⁰_AB [cm²/s]:")
            D0_BA = self.get_float("D⁰_BA [cm²/s]:")
            exp_D_AB = self.get_float("Experimental D_AB [cm²/s]:")
            
            if None in (x_A, T, a_AB, a_BA, r_A, r_B, q_A, q_B, D0_AB, D0_BA, exp_D_AB):
                return
            
            x_B = 1 - x_A
            
            # Intermediate calculations
            sum_xr = x_A*r_A + x_B*r_B
            phi_A = (x_A * r_A) / sum_xr
            phi_B = (x_B * r_B) / sum_xr
            
            sum_xq = x_A*q_A + x_B*q_B
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
            term2 = 2 * (x_A * math.log(x_A/phi_A) + x_B * math.log(x_B/phi_B))
            term3 = 2 * x_A * x_B * ((phi_A/x_A)*(1 - lambda_A/lambda_B) + (phi_B/x_B)*(1 - lambda_B/lambda_A))
            term4 = x_B * q_A * ((1 - theta_BA**2)*math.log(tau_BA) + (1 - theta_BB**2)*tau_AB*math.log(tau_AB))
            term5 = x_A * q_B * ((1 - theta_AB**2)*math.log(tau_AB) + (1 - theta_AA**2)*tau_BA*math.log(tau_BA))
            
            ln_DAB = term1 + term2 + term3 + term4 + term5
            DAB = math.exp(ln_DAB)
            error = ((DAB - exp_D_AB) / exp_D_AB) * 100
            
            # Display results
            self.result_text.delete(1.0, tk.END)
            result = f"""=== Final Results ===
Calculated D_AB: {DAB:.3e} cm²/s
Experimental D_AB: {exp_D_AB:.3e} cm²/s
Percentage Error: {error:.2f}%

=== Intermediate Values ===
Phi Values:
  φ_A = {phi_A:.4f}
  φ_B = {phi_B:.4f}

Theta Values:
  θ_A = {theta_A:.4f}
  θ_B = {theta_B:.4f}

Tau Values:
  τ_AB = {tau_AB:.4f}
  τ_BA = {tau_BA:.4f}

Lambda Values:
  λ_A = {lambda_A:.4f}
  λ_B = {lambda_B:.4f}

Theta Interaction Parameters:
  θ_BA = {theta_BA:.4f}
  θ_AB = {theta_AB:.4f}
  θ_AA = {theta_AA:.4f}
  θ_BB = {theta_BB:.4f}"""
            
            self.result_text.insert(tk.END, result)
            
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")
    
    def reset(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.set_default_values()
        self.result_text.delete(1.0, tk.END)
    
    def show_help(self):
        help_text = """Hsu and Chen Method Calculator

Input Parameters:
1. Mole fraction of component A (x_A): Range 0-1
2. Temperature (T): In Kelvin
3. a_AB, a_BA: Adjustable interaction parameters
4. r_A, r_B: Volume parameters
5. q_A, q_B: Surface area parameters
6. D⁰_AB, D⁰_BA: Diffusion coefficients at infinite dilution
7. Experimental D_AB: Reference value for error calculation

All parameters should be entered as floating-point numbers."""
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiffusionCalculator(root)
    root.mainloop()
