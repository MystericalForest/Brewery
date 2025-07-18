import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def plot_csv(csv_file, x_column=None, y_column=None):
    """
    Indlæser en CSV-fil og laver en graf.
    
    Args:
        csv_file (str): Sti til CSV-filen
        x_column (str, optional): Navn på kolonnen til x-aksen. Hvis None, bruges indeks.
        y_column (str, optional): Navn på kolonnen til y-aksen. Hvis None, plottes alle kolonner.
    """
    # Tjek om filen eksisterer
    if not os.path.exists(csv_file):
        print(f"Fejl: Filen '{csv_file}' findes ikke.")
        return
    
    try:
        # Indlæs CSV-filen
        df = pd.read_csv(csv_file)
        
        # Vis kolonnenavne, hvis nødvendigt
        if x_column is None or (y_column is None and len(df.columns) > 1):
            print(f"Tilgængelige kolonner i '{csv_file}':")
            for i, col in enumerate(df.columns):
                print(f"  {i}: {col}")
        
        # Opret figur
        plt.figure(figsize=(10, 6))
        
        # Håndter forskellige plot-scenarier
        if x_column is not None and x_column not in df.columns:
            print(f"Fejl: Kolonne '{x_column}' findes ikke i CSV-filen.")
            return
            
        if y_column is not None and y_column not in df.columns:
            print(f"Fejl: Kolonne '{y_column}' findes ikke i CSV-filen.")
            return
            
        # Plot baseret på input-parametre
        if y_column is not None:
            # Plot én specifik y-kolonne
            if x_column is not None:
                # Plot y mod x
                plt.plot(df[x_column], df[y_column], marker='o')
                plt.xlabel(x_column)
                plt.ylabel(y_column)
                plt.title(f"{y_column} vs {x_column}")
            else:
                # Plot y mod indeks
                plt.plot(df[y_column], marker='o')
                plt.xlabel("Indeks")
                plt.ylabel(y_column)
                plt.title(f"{y_column}")
        else:
            # Plot alle kolonner
            if x_column is not None:
                # Plot alle kolonner mod x
                for column in df.columns:
                    if column != x_column:
                        plt.plot(df[x_column], df[column], marker='o', label=column)
                plt.xlabel(x_column)
                plt.ylabel("Værdi")
                plt.title(f"Alle kolonner vs {x_column}")
            else:
                # Plot alle kolonner mod indeks
                for column in df.columns:
                    plt.plot(df[column], marker='o', label=column)
                plt.xlabel("Indeks")
                plt.ylabel("Værdi")
                plt.title("Alle kolonner")
            
            # Tilføj legend hvis vi plotter flere kolonner
            plt.legend()
        
        # Tilføj gitter og vis plot
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Fejl ved indlæsning eller plotting af CSV-fil: {e}")

if __name__ == "__main__":
    # Kommandolinje-interface
    if len(sys.argv) == 1:
        print("Brug: python csv_grapher.py <csv_fil> [x_kolonne] [y_kolonne]")
    elif len(sys.argv) == 2:
        plot_csv(sys.argv[1])
    elif len(sys.argv) == 3:
        plot_csv(sys.argv[1], sys.argv[2])
    else:  # len(sys.argv) >= 4
        plot_csv(sys.argv[1], sys.argv[2], sys.argv[3])