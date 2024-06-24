from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
import pandas as pd
from decimal import Decimal

def handle_uploaded_file(f):
    # Lendo a planilha original
    df = pd.read_csv(f)

    # Colunas de saída
    output_columns = ["ID_CONDOMINIO", "ID_UNIDADE", "VENCIMENTO", "DATA_DE_COMPETENCIA", "CONTA_BANCARIA", "NOSSO_NUMERO", "TOKEN-FACILITADOR", "TOKEN-CONTA",
                      "RECEITA_APROPRIACAO1[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO1[COMPLEMENTO]", "RECEITA_APROPRIACAO1[VALOR]",
                      "RECEITA_APROPRIACAO2[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO2[COMPLEMENTO]", "RECEITA_APROPRIACAO2[VALOR]",
                      "RECEITA_APROPRIACAO3[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO3[COMPLEMENTO]", "RECEITA_APROPRIACAO3[VALOR]",
                      "RECEITA_APROPRIACAO4[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO4[COMPLEMENTO]", "RECEITA_APROPRIACAO4[VALOR]",
                      "RECEITA_APROPRIACAO5[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO5[COMPLEMENTO]", "RECEITA_APROPRIACAO5[VALOR]",
                      "RECEITA_APROPRIACAO6[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO6[COMPLEMENTO]", "RECEITA_APROPRIACAO6[VALOR]",
                      "RECEITA_APROPRIACAO7[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO7[COMPLEMENTO]", "RECEITA_APROPRIACAO7[VALOR]",
                      "RECEITA_APROPRIACAO8[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO8[COMPLEMENTO]", "RECEITA_APROPRIACAO8[VALOR]",
                      "RECEITA_APROPRIACAO9[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO9[COMPLEMENTO]", "RECEITA_APROPRIACAO9[VALOR]",
                      "RECEITA_APROPRIACAO10[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO10[COMPLEMENTO]", "RECEITA_APROPRIACAO10[VALOR]",
                      "RECEITA_APROPRIACAO11[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO11[COMPLEMENTO]", "RECEITA_APROPRIACAO11[VALOR]",
                      "RECEITA_APROPRIACAO12[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO12[COMPLEMENTO]", "RECEITA_APROPRIACAO12[VALOR]",
                      "RECEITA_APROPRIACAO13[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO13[COMPLEMENTO]", "RECEITA_APROPRIACAO13[VALOR]",
                      "RECEITA_APROPRIACAO14[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO14[COMPLEMENTO]", "RECEITA_APROPRIACAO14[VALOR]",
                      "RECEITA_APROPRIACAO15[CONTA_CATEGORIA]", "RECEITA_APROPRIACAO15[COMPLEMENTO]", "RECEITA_APROPRIACAO15[VALOR]",
                      "TAXA_DE_JUROS", "TAXA_DE_MULTA", "TAXA_DE_DESCONTO", "COBRANCA_EXTRAORDINARIA"]

    # Criando um DataFrame para o resultado final
    result = pd.DataFrame(columns=output_columns)

    # Agrupando os dados pelo "NOSSO_NUMERO"
    grouped = df.groupby("NOSSO_NUMERO")

    # Criando uma lista para armazenar novas linhas
    new_rows = []

    # Preenchendo o DataFrame resultante com os dados agrupados
    for _, group in grouped:
        new_row = {}
        new_row["ID_CONDOMINIO"] = group.iloc[0]["ID_CONDOMINIO"]
        new_row["ID_UNIDADE"] = group.iloc[0]["ID_UNIDADE"]
        new_row["VENCIMENTO"] = group.iloc[0]["VENCIMENTO"]
        new_row["DATA_DE_COMPETENCIA"] = group.iloc[0]["DATA_DE_COMPETENCIA"]
        new_row["CONTA_BANCARIA"] = group.iloc[0]["CONTA_BANCARIA"]
        new_row["NOSSO_NUMERO"] = group.iloc[0]["NOSSO_NUMERO"]
        new_row["TOKEN-FACILITADOR"] = group.iloc[0]["TOKEN-FACILITADOR"]
        new_row["TOKEN-CONTA"] = group.iloc[0]["TOKEN-CONTA"]

        # Adicionando uma nova linha à lista
        new_rows.append(new_row)

        # Adicionando receitas apropriadas, pois são várias colunas
        for i, (idx, row) in enumerate(group.iterrows()):
            new_row[f"RECEITA_APROPRIACAO{i+1}[CONTA_CATEGORIA]"] = row["CONTA_CATEGORIA"]
            new_row[f"RECEITA_APROPRIACAO{i+1}[COMPLEMENTO]"] = row["COMPLEMENTO"]
            new_row[f"RECEITA_APROPRIACAO{i+1}[VALOR]"] = row["VALOR"]

        try:
            group["TAXA_DE_JUROS"] = pd.to_numeric(group["TAXA_DE_JUROS"], errors='coerce')
            new_row["TAXA_DE_JUROS"] = Decimal(group["TAXA_DE_JUROS"].round(2).sum())

            group["TAXA_DE_MULTA"] = pd.to_numeric(group["TAXA_DE_MULTA"], errors='coerce')
            new_row["TAXA_DE_MULTA"] = Decimal(group["TAXA_DE_MULTA"].round(2).sum())

            group["TAXA_DE_DESCONTO"] = pd.to_numeric(group["TAXA_DE_DESCONTO"], errors='coerce')
            new_row["TAXA_DE_DESCONTO"] = Decimal(group["TAXA_DE_DESCONTO"].round(2).sum())
        except Exception as e:
            print(f"Erro na conversão ou arredodamento nas colunas TAXA_DE_JUROS: {e}")
            new_row["TAXA_DE_JUROS"] = Decimal(0)
            new_row["TAXA_DE_MULTA"] = Decimal(0)
            new_row["TAXA_DE_DESCONTO"] = Decimal(0)

        new_row["TAXA_DE_JUROS"] = str(group["TAXA_DE_JUROS"].round(2).sum()).replace('.', ',')
        new_row["TAXA_DE_MULTA"] = str(group["TAXA_DE_MULTA"].round(2).sum()).replace('.', ',')
        new_row["TAXA_DE_DESCONTO"] = str(group["TAXA_DE_DESCONTO"].round(2).sum()).replace('.', ',')
        # Colocando como "0,00" conforme o exemplo fornecido
        new_row["COBRANCA_EXTRAORDINARIA"] = "0,00"

    # Criando um novo DataFrame a partir da lista de novas linhas e concatenando com o DataFrame de 'result'
    result = pd.concat([result, pd.DataFrame(new_rows)], ignore_index=True)

    return result

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            final_df = handle_uploaded_file(request.FILES['file'])

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="final.csv"'
            final_df.to_csv(path_or_buf=response, index=False)
            return response
    else:
        form = UploadFileForm()
    return render(request, 'convert/upload.html', {'form': form})
