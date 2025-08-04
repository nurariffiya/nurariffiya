import streamlit as st
import pandas as pd
import mysql.connector

# Fungsi koneksi ke database MySQL
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="coffee_db"
    )

def read_menu_kopi():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_kalori")
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_menu_kopi(menu, kopi_g, susu_g, evaporasi_g, sauce_caramel_g, cafein_mg, calories, kategori_kalori):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO menu_kalori (menu, `kopi (g)`, `susu (g)`, `evaporasi (g)`, `sauce_caramel (g)`, `cafein (mg)`, calories, kategori_kalori)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (menu, kopi_g, susu_g, evaporasi_g, sauce_caramel_g, cafein_mg, calories, kategori_kalori)
    cursor.execute(query, values)
    conn.commit()
    conn.close()

def update_menu_kopi(id, menu, kopi_g, susu_g, evaporasi_g, sauce_caramel_g, cafein_mg, calories, kategori_kalori):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
        UPDATE menu_kalori
        SET menu=%s, `kopi (g)`=%s, `susu (g)`=%s, `evaporasi (g)`=%s, `sauce_caramel (g)`=%s, `cafein (mg)`=%s, calories=%s, kategori_kalori=%s
        WHERE id=%s
    """
    values = (menu, kopi_g, susu_g, evaporasi_g, sauce_caramel_g, cafein_mg, calories, kategori_kalori, id)
    cursor.execute(query, values)
    conn.commit()
    conn.close()

def delete_menu_kopi(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu_kalori WHERE id = %s", (id,))
    conn.commit()
    conn.close()

def menu_kalori_page():
    st.title("Menu Kopi Berdasarkan Komposisi Bahan dan Kalori")

    # Menampilkan menu kopi yang ada di database
    st.subheader("Menu Kopi yang Tersedia")
    menu_data = read_menu_kopi()
    menu_df = pd.DataFrame(menu_data, columns=["ID", "Menu", "Kopi (g)", "Susu (g)", "Evaporasi (g)", "Sauce Caramel (g)", "Cafein (mg)", "Kalori", "Kategori Kalori"])
    st.dataframe(menu_df)

    ### ✅ Form untuk menambah menu kopi baru
    st.subheader("Tambah Menu Kopi Baru")
    if "add_form_submitted" not in st.session_state:
        st.session_state.add_form_submitted = False

    with st.form("add_menu_form", clear_on_submit=True):
        menu = st.text_input("Menu Kopi")
        kopi_g = st.number_input("Jumlah Kopi (g)", min_value=0)
        susu_g = st.number_input("Jumlah Susu (g)", min_value=0)
        evaporasi_g = st.number_input("Jumlah Evaporasi (g)", min_value=0)
        sauce_caramel_g = st.number_input("Jumlah Sauce Caramel (g)", min_value=0)
        cafein_mg = st.number_input("Jumlah Cafein (mg)", min_value=0)
        calories = st.number_input("Jumlah Kalori", min_value=0)
        kategori_kalori = st.selectbox("Kategori Kalori", ["Rendah", "Tinggi"])

        submit_button = st.form_submit_button("Tambah Menu Kopi")
        if submit_button:
            create_menu_kopi(menu, kopi_g, susu_g, evaporasi_g, sauce_caramel_g, cafein_mg, calories, kategori_kalori)
            st.session_state.add_form_submitted = True

    if st.session_state.add_form_submitted:
        st.success("Menu kopi berhasil ditambahkan!")
        st.session_state.add_form_submitted = False

    ### ✅ Form untuk mengedit menu kopi dengan dropdown
    st.subheader("Edit Menu Kopi")
    if menu_data:
        menu_options = [f"{item[0]} - {item[1]}" for item in menu_data]
        selected_menu_edit = st.selectbox("Pilih Menu Kopi yang akan Diedit", menu_options, key="select_edit")
        menu_id_to_edit = int(selected_menu_edit.split(" - ")[0])
        menu_to_edit = next((item for item in menu_data if item[0] == menu_id_to_edit), None)

        if menu_to_edit:
            with st.form("edit_menu_form"):
                menu = st.text_input("Menu Kopi", value=menu_to_edit[1])
                kopi_g = st.number_input("Jumlah Kopi (g)", value=menu_to_edit[2], min_value=0)
                susu_g = st.number_input("Jumlah Susu (g)", value=menu_to_edit[3], min_value=0)
                evaporasi_g = st.number_input("Jumlah Evaporasi (g)", value=menu_to_edit[4], min_value=0)
                sauce_caramel_g = st.number_input("Jumlah Sauce Caramel (g)", value=menu_to_edit[5], min_value=0)
                cafein_mg = st.number_input("Jumlah Cafein (mg)", value=menu_to_edit[6], min_value=0)
                calories = st.number_input("Jumlah Kalori", value=menu_to_edit[7], min_value=0)
                kategori_kalori = st.selectbox("Kategori Kalori", ["Rendah", "Tinggi"], index=["Rendah", "Tinggi"].index(menu_to_edit[8]))

                update_button = st.form_submit_button("Update Menu Kopi")
                if update_button:
                    update_menu_kopi(menu_id_to_edit, menu, kopi_g, susu_g, evaporasi_g, sauce_caramel_g, cafein_mg, calories, kategori_kalori)
                    st.success("Menu kopi berhasil diperbarui!")

    ### ✅ Form untuk menghapus menu kopi dengan dropdown
    st.subheader("Hapus Menu Kopi")
    if menu_data:
        menu_options_del = [f"{item[0]} - {item[1]}" for item in menu_data]
        selected_menu_del = st.selectbox("Pilih Menu Kopi yang akan Dihapus", menu_options_del, key="select_delete")
        menu_id_to_delete = int(selected_menu_del.split(" - ")[0])

        delete_button = st.button("Hapus Menu Kopi")
        if delete_button:
            delete_menu_kopi(menu_id_to_delete)
            st.success("Menu kopi berhasil dihapus!")

# Jalankan halaman menu kalori
menu_kalori_page()
