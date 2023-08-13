import tkinter as tk
from tkinter import ttk  # Import themed widgets for better appearance
from pymongo import MongoClient
import pyperclip

from parse_file import upload_lua_file
from database_gestion import get_all_classes, get_main_spe_by_class, get_best_documents

# Interface graphique simple pour choisir le fichier et l'uploader
def create_gui():
    classes = get_all_classes()

    root = tk.Tk()
    root.title("Chercheur de nouveaux membres")

    # Create frames for each row
    top_frame = ttk.Frame(root)
    top_frame.grid(row=0, column=0, padx=10, pady=10)

    middle_frame = ttk.Frame(root)
    middle_frame.grid(row=1, column=0, padx=10, pady=10)

    bottom_frame = ttk.Frame(root)
    bottom_frame.grid(row=2, column=0, padx=10, pady=10)

    # Use a ttk themed style for the widgets
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12))
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TCombobox", font=("Helvetica", 12))

    # Dropdown menu to select the 'Classe' value
    selected_classe = tk.StringVar(root)
    selected_classe.set(classes[0])
    classe_label = ttk.Label(top_frame, text="Classe")
    classe_label.grid(row=0, column=0, padx=10, pady=10)
    classe_menu = ttk.Combobox(top_frame, textvariable=selected_classe, values=classes, state="readonly")
    classe_menu.grid(row=0, column=1, padx=10, pady=10)

    # Dropdown menu to select the 'Main_spe' value
    selected_main_spe = tk.StringVar(root)
    main_spe_values = get_main_spe_by_class(classes[0])
    selected_main_spe.set(main_spe_values[0]) if main_spe_values else selected_main_spe.set('')
    main_spe_label = ttk.Label(top_frame, text="Spécialisation")
    main_spe_label.grid(row=0, column=2, padx=10, pady=10)
    main_spe_menu = ttk.Combobox(top_frame, textvariable=selected_main_spe, values=main_spe_values, state="readonly")
    main_spe_menu.grid(row=0, column=3, padx=10, pady=10)

    # Function to update 'Main_spe' dropdown menu based on selected 'Classe'
    def update_main_spe_dropdown(*args):
        main_spe_values = get_main_spe_by_class(selected_classe.get())
        selected_main_spe.set(main_spe_values[0])  # Clear the previous selection
        main_spe_menu["values"] = main_spe_values

    # Bind the update_main_spe_dropdown function to changes in the 'Classe' dropdown menu
    selected_classe.trace("w", update_main_spe_dropdown)

    # Function to copy all the names displayed on the screen to the clipboard
    def copy_names():
        update_result_text()

    # Create the "Copy Names" button
    copy_button = ttk.Button(middle_frame, text="Copy Names", command=copy_names)
    copy_button.grid(row=0, column=0, padx=10, pady=10)

    # Dropdown menu to select the 'lvl_spe' threshold
    lvl_spe_values = list(range(10, 100, 10))  # [10, 20, ..., 90]
    selected_lvl_spe = tk.IntVar(root)
    lvl_spe_label = ttk.Label(middle_frame, text="Above:")
    lvl_spe_label.grid(row=0, column=1, padx=10, pady=10)
    lvl_spe_menu = ttk.OptionMenu(middle_frame, selected_lvl_spe, *lvl_spe_values)
    lvl_spe_menu.grid(row=0, column=2, padx=10, pady=10)

    # Text box to display the best documents in the middle frame
    result_text = tk.Text(middle_frame, height=10, width=50, font=("Helvetica", 12))
    result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Function to update the result text box based on selected 'Classe' and 'Main_spe'
    def update_result_text(*args):
        selected_class = selected_classe.get()
        selected_main_spe_value = selected_main_spe.get()
        best_documents = get_best_documents(selected_class, selected_main_spe_value)

        # Clear the existing content of the text box
        result_text.delete('1.0', tk.END)

        # Update the text box with the best documents
        if best_documents:
            result_text.insert(tk.END, "20 Meilleurs joueurs sans guilde:\n\n")
            for idx, doc in enumerate(best_documents, 1):
                result_text.insert(tk.END, f"{idx}. {doc['Nom du joueur']}, "
                                            f"Best Perf. Avg: {doc['lvl_spe']}\n")
        else:
            result_text.insert(tk.END, "No documents found for the selected criteria.")

        # Clear the clipboard before copying new names
        pyperclip.copy("")

        # Copy the names to the clipboard, filtered by the selected lvl_spe threshold
        names_text = " ".join(doc['Nom du joueur'] for doc in best_documents if doc['lvl_spe'] >= selected_lvl_spe.get())
        pyperclip.copy(names_text)


    # Call the update_result_text function initially and whenever the 'Classe' or 'Main_spe' changes
    selected_classe.trace("w", update_result_text)
    selected_main_spe.trace("w", update_result_text)

    # Call the update_result_text function initially to display results from the start
    update_result_text()

    # Bouton pour uploader le fichier in the bottom frame
    upload_button = tk.Button(bottom_frame, text="Uploader un fichier .lua", command=upload_lua_file)
    upload_button.grid(row=0, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()