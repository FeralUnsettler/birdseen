import streamlit as st
import requests
from PIL import Image
import io

# Função para obter os dados da API
def get_data(page_index):
    url = f"https://www.wikiaves.com.br/getRegistrosJSON.php?p={page_index}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    st.title("Visualizador de Dados da Wikiaves")

    # Barra lateral para entrada do índice da página
    page_index = st.sidebar.number_input("Digite o índice da página:", value=1, min_value=1)

    st.write("Aguarde enquanto os dados estão sendo carregados...")

    # Obter dados da API
    url = f"https://www.wikiaves.com.br/getRegistrosJSON.php?p={page_index}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        st.write("Erro ao carregar os dados.")
        return

    if data:
        # Configurar galeria 5x4
        num_rows = 5
        num_cols = 4
        images_per_page = num_rows * num_cols
        num_images = min(len(data['registros']['itens']), images_per_page)
        row_index = 0
        col_index = 0

        # Criar layout da galeria
        gallery = st.empty()
        gallery_columns = []

        for i, item in enumerate(data['registros']['itens'].values()):
            # Processar a imagem
            image_url = item['link'].replace('#_', '_')  # Trocar #_ por _
            image_response = requests.get(image_url)
            image = Image.open(io.BytesIO(image_response.content))
            image.thumbnail((200, 200))  # Redimensionar imagem para uma miniatura

            # Criar card com imagem e informações
            card = f"""
                <div style="padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin: 5px;">
                    <img src="{image_url}" style="width: 100%; border-radius: 5px;">
                    <p>ID: {item['id']}</p>
                    <p>Espécie: {item['sp']['nome']}</p>
                    <p>Autor: {item['autor']}</p>
                    <p>Data: {item['data']}</p>
                </div>
            """
            gallery_columns.append(card)

            col_index += 1
            if col_index == num_cols or i == num_images - 1:
                gallery.markdown("<div style='display: flex;'>".join(gallery_columns), unsafe_allow_html=True)
                gallery_columns = []
                col_index = 0
                row_index += 1
                if row_index == num_rows:
                    break

    else:
        st.write("Nenhum dado disponível.")

if __name__ == "__main__":
    main()
