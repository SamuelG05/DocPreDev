import sys
import fdb
import customtkinter as ctk
from tkinter import messagebox

# Verifica argumentos e define caminho padrão se necessário
if len(sys.argv) >= 3:
    host = sys.argv[1]
    caminho_db = sys.argv[2]
else:
    host = "localhost"
    caminho_db = r"C:\Facil\Retaguarda\DB\DB.FDB"

dsn = f"{host}:{caminho_db}"

# Buscar nome da empresa
def obter_nome_empresa():
    try:
        con = fdb.connect(dsn=dsn, user="SYSDBA", password="masterkey")
        cur = con.cursor()
        cur.execute("SELECT FIRST 1 EMPRESA_NOME FROM EMPRESAS")
        row = cur.fetchone()
        con.close()
        return row[0] if row else "EMPRESA NÃO ENCONTRADA"
    except:
        return "ERRO AO OBTER EMPRESA"

# Função de busca principal
def buscar_dados(event=None):
    try:
        pre_id = entry_id.get().strip()
        if not pre_id.isdigit():
            messagebox.showerror("Erro", "Digite um número de pré-devolução válido.")
            return

        con = fdb.connect(dsn=dsn, user="SYSDBA", password="masterkey")
        cur = con.cursor()
        cur.execute("""
            SELECT 
                p.PREDEVOLUCAO_DOCUMENTO,
                p.PREDEVOLUCAO_EMISSAO,
                c.CLIENTE_NOME
            FROM PREDEVOLUCAO p
            LEFT JOIN CLIENTES c ON c.CLIENTES_ID = p.CLIENTES_ID
            WHERE p.PREDEVOLUCAO_ID = ?
        """, (int(pre_id),))
        row = cur.fetchone()
        con.close()

        if row:
            doc, emissao, cliente = row
            texto = f"Documento/Venda: {doc or 'N/A'}\nData de Emissão: {emissao.strftime('%d/%m/%Y') if emissao else 'N/A'}\nCliente: {cliente or 'N/A'}"
            resultado_label.configure(text=texto)
        else:
            resultado_label.configure(text="Pré-devolução não encontrada.")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Interface
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Localizador de Documento da Pré-Devolução")
app.geometry("450x320")

# Widgets principais
ctk.CTkLabel(app, text="Digite o número da Pré-Devolução:", font=("Arial", 13)).pack(pady=15)

entry_id = ctk.CTkEntry(app, width=200, font=("Arial", 12))
entry_id.pack(pady=5)
entry_id.bind("<Return>", buscar_dados)

ctk.CTkButton(app, text="Buscar Documento(Enter)", command=buscar_dados).pack(pady=10)

resultado_label = ctk.CTkLabel(app, text="", font=("Arial", 12), justify="left")
resultado_label.pack(pady=15)

# Rodapé
empresa_nome = obter_nome_empresa()

ctk.CTkLabel(app, text=empresa_nome, font=("Arial", 13, "bold"), text_color="white").pack(pady=(30, 0))
ctk.CTkLabel(app, text="DESENVOLVIDO POR SAMUEL OLIVEIRA - FÁCIL SISTEMAS TURMALINA", font=("Arial", 10), text_color="#AFAFAF").pack(pady=(5, 10))

app.mainloop()
