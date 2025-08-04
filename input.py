import streamlit as st
import pandas as pd

# Inisialisasi session_state untuk menyimpan data jika belum ada
if 'data_kopi' not in st.session_state:
    st.session_state['data_kopi'] = pd.DataFrame(columns=['Menu Kopi', 'Kopi (g)', 'Susu (g)', 'Evaporasi (g)', 'Sauce Caramel (g)', 'Kalori'])

# Inisialisasi session_state input field jika belum ada
if 'menu_kopi' not in st.session_state:
    st.session_state['menu_kopi'] = ''
if 'kopi' not in st.session_state:
    st.session_state['kopi'] = 0
if 'susu' not in st.session_state:
    st.session_state['susu'] = 0
if 'evaporasi' not in st.session_state:
    st.session_state['evaporasi'] = 0
if 'sauce_caramel' not in st.session_state:
    st.session_state['sauce_caramel'] = 0
if 'kalori' not in st.session_state:
    st.session_state['kalori'] = 0

st.title("Penginputan Data Kopi")

# Form input data kopi
with st.form("input_kopi"):
    menu_kopi = st.text_input("Menu Kopi", value=st.session_state['menu_kopi'])
    
    st.write("Masukkan Komposisi Bahan (gram):")
    kopi = st.number_input("Kopi (g)", min_value=0, step=1, value=st.session_state['kopi'])
    susu = st.number_input("Susu (g)", min_value=0, step=1, value=st.session_state['susu'])
    evaporasi = st.number_input("Evaporasi (g)", min_value=0, step=1, value=st.session_state['evaporasi'])
    sauce_caramel = st.number_input("Sauce Caramel (g)", min_value=0, step=1, value=st.session_state['sauce_caramel'])
    
    kalori = st.number_input("Kalori", min_value=0, step=1, value=st.session_state['kalori'])

    # Tombol submit
    submitted = st.form_submit_button("Simpan Data")

    if submitted:
        # Tambahkan data ke DataFrame di session_state
        new_data = pd.DataFrame({
            'Menu Kopi': [menu_kopi],
            'Kopi (g)': [kopi],
            'Susu (g)': [susu],
            'Evaporasi (g)': [evaporasi],
            'Sauce Caramel (g)': [sauce_caramel],
            'Kalori': [kalori]
        })
        st.session_state['data_kopi'] = pd.concat([st.session_state['data_kopi'], new_data], ignore_index=True)
        st.success(f"Data kopi '{menu_kopi}' berhasil disimpan!")

        # Reset input field
        st.session_state['menu_kopi'] = ''
        st.session_state['kopi'] = 0
        st.session_state['susu'] = 0
        st.session_state['evaporasi'] = 0
        st.session_state['sauce_caramel'] = 0
        st.session_state['kalori'] = 0

# Tampilkan data kopi yang sudah diinput
st.subheader("Data Kopi yang Sudah Diinput")
st.dataframe(st.session_state['data_kopi'])

# Upload file CSV
st.subheader("Upload File CSV Data Kopi")
uploaded_file = st.file_uploader("Upload file CSV di sini", type=['csv'])

if uploaded_file is not None:
    try:
        df_uploaded = pd.read_csv(uploaded_file)
        st.write("Data dari file CSV:")
        st.dataframe(df_uploaded)
    except Exception as e:
        st.error(f"Terjadi error saat membaca file: {e}")
